import textwrap
import pprint

import bgl
import blf

import bpy
import bmesh

from svrx.nodes.node_base import stateful
from svrx.nodes.classes import NodeID, NodeStateful
from svrx.typing import Required, StringP, Anytype, BoolP
from svrx.util import bgl_callback
# pylint: disable=C0326


class NodeStethoscope(NodeID, NodeStateful):
    def free(self):
        bgl_callback.callback_disable(self.node_id)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "activate")
        row.prop(self, "shape")

def simple_grid_xy(x, y, args):
    # func = args[0]
    # back_color, grid_color, line_color = args[1]

    def draw_rect(x=0, y=0, w=30, h=10, color=(0.0, 0.0, 0.0, 1.0)):

        bgl.glColor4f(*color)
        bgl.glBegin(bgl.GL_POLYGON)

        for coord in [(x, y), (x+w, y), (w+x, y-h), (x, y-h)]:
            bgl.glVertex2f(*coord)
        bgl.glEnd()

    # draw bg fill
    draw_rect(x=x, y=y, w=140, h=140, color=(0.2, 0.7, 0.4, 1.0))


@stateful
class SvRxStethoscope():

    bl_idname = "SvRxNodeStethoscope"
    label = "Stethoscope"
    cls_bases = (NodeStethoscope,)

    properties = {
        'activate': BoolP(name='Activate', default=True),
        'shape': BoolP(name="Shape", default=True)
    }

    def __init__(self, node=None):
        if node is not None:
            self.node = node
            self.activate = node.activate
            self.shape = node.shape
            self.n_id = node.node_id

    @property
    def xy_offset(self):
        a = self.node.location[:]
        b = int(self.node.width) + 20
        return int(a[0] + b), int(a[1])

    def stop(self):
        bgl_callback.callback_disable(self.n_id)
        if self.activate:
            dt = self.node.inputs[0].data_tree
            lines = ["total depth: {} object count: {}".format(dt.level, dt.count()), ""]
            structure = parse_tree(dt, self.shape)
            lines.extend(pprint.pformat(structure).splitlines())
            draw_data = {
                'tree_name': self.node.id_data.name[:],
                'custom_function': draw_text,
                'loc': self.xy_offset,
                'args': (lines,)
            }
            bgl_callback.callback_enable(self.n_id, draw_data)

    def __call__(self, data: Anytype = Required):
        pass


def draw_text(x, y, args):
    lines = args[0]

    x, y = int(x), int(y)
    color = (0.9, 0.9, 0.9)
    font_id = 0

    text_height = 15
    line_height = 14

    # why does the text look so jagged?  <-- still valid question
    # dpi = bpy.context.user_preferences.system.dpi
    blf.size(font_id, int(text_height), 72)
    ypos = y
    xpos = x
    h = 1.3 * line_height * (len(lines) + 1)
    bgl.glColor3f(0.2,  0.2, 0.2)
    bgl.glColor3f(*color)
    for line in lines:
        blf.position(0, xpos, ypos, 0)
        blf.draw(font_id, line)
        ypos -= int(line_height * 1.3)


def parse_tree(dt, shape=False):
    if dt.level == 0:
        if shape:
            return dt.data.shape
        else:
            return dt.data
    else:
        out = []
        for child in dt.children:
            out.append(parse_tree(child, shape))
        return out
