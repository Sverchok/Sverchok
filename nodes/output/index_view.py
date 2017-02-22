import math
from collections import namedtuple

import bgl
import blf

import bpy
import bmesh
import time
from svrx.nodes.node_base import stateful
from svrx.nodes.classes import NodeID, NodeStateful
from svrx.typing import Required, StringP, Anytype, BoolP, VectorP, BMesh, Matrix
from svrx.util import bgl_callback_3dview_2d as bgl_callback

# pylint: disable=C0326
# pylint: disable=C0330

point_dict = {}

def adjust_list(in_list, x, y):
    return [[old_x + x, old_y + y] for (old_x, old_y) in in_list]


def generate_points(width, height):
    amp = 5  # radius fillet

    width += 2
    height += 4
    width = ((width/2) - amp) + 2
    height -= (2*amp)

    pos_list, final_list = [], []

    n_points = 12
    seg_angle = 2 * math.pi / n_points
    for i in range(n_points + 1):
        angle = i * seg_angle
        x = math.cos(angle) * amp
        y = math.sin(angle) * amp
        pos_list.append([x, -y])

    w_list, h_list = [1, -1, -1, 1], [-1, -1, 1, 1]
    slice_list = [[i, i+4] for i in range(0, n_points, 3)]

    for idx, (start, end) in enumerate(slice_list):
        point_array = pos_list[start:end]
        w = width * w_list[idx]
        h = height * h_list[idx]
        final_list += adjust_list(point_array, w, h)

    return final_list


def get_points(index):
    '''
    index:   string representation of the index number
    returns: rounded rect point_list used for background.
    the neat thing about this is if a width has been calculated once, it
    is stored in a dict and used if another polygon is saught with that width.
    '''
    width, height = blf.dimensions(0, index)
    if not (width in point_dict):
        point_dict[width] = generate_points(width, height)

    return point_dict[width]


def draw_index_viz(context, args):

    fx = args.fx
    region = context.region
    region3d = context.space_data.region_3d

    # vars for projection
    perspective_matrix = region3d.perspective_matrix.copy()

    font_id = 0
    text_height = 13
    blf.size(font_id, text_height, 72)  # should check prefs.dpi

    region_mid_width = region.width / 2.0
    region_mid_height = region.height / 2.0


    def draw_index(rgb, rgb2, index, vec):

        vec_4d = perspective_matrix * vec.to_4d()
        if vec_4d.w <= 0.0:
            return

        x = region_mid_width + region_mid_width * (vec_4d.x / vec_4d.w)
        y = region_mid_height + region_mid_height * (vec_4d.y / vec_4d.w)
        index = str(index)

        ''' draw polygon if requested'''
        if fx.draw_bg:
            polyline = get_points(index)

            bgl.glColor4f(*rgb2)
            bgl.glBegin(bgl.GL_POLYGON)
            for pointx, pointy in polyline:
                bgl.glVertex2f(pointx+x, pointy+y)
            bgl.glEnd()

        ''' draw text '''
        txt_width, txt_height = blf.dimensions(0, index)
        bgl.glColor4f(*rgb)
        blf.position(0, x - (txt_width / 2), y - (txt_height / 2), 0)
        blf.draw(0, index)

    def calc_median(vlist):
        a = Vector((0, 0, 0))
        for v in vlist:
            a += v
        return a / len(vlist)

    for obj_index, (bm, matrix) in enumerate(zip(args.data.bms, args.data.mats)):

        final_verts = bm.verts

        # # quickly apply matrix if necessary
        # if matrix:  # and is not identity matrix.
        #     # matrix = data_matrix[obj_index]
        #     final_verts = [matrix * v for v in verts]

        if fx.display_vert_index:
            for idx, v in enumerate(final_verts):
                draw_index(fx.vert_idx_color, fx.vert_bg_color, idx, v.co)

        # if bm.edges and fx.display_edge_index:
        #     for edge_index, (idx1, idx2) in enumerate(e.vertices for e in bm.edges):
                
        #          v1 = Vector(final_verts[idx1])
        #          v2 = Vector(final_verts[idx2])
        #          loc = v1 + ((v2 - v1) / 2)
        #          draw_index(fx.edge_idx_color, fx.edge_bg_color, edge_index, loc)

        # if bm.faces and fx.display_face_index:
        #     for face_index, f in enumerate(data_faces[obj_index]):
        #         verts = [Vector(final_verts[idx]) for idx in f]
        #         median = calc_median(verts)
        #         draw_index(fx.face_idx_color, fx.face_bg_color, face_index, median)



class NodeIndexView(NodeID, NodeStateful):

    def draw_buttons(self, context, layout):
        view_icon = 'RESTRICT_VIEW_' + ('OFF' if self.activate else 'ON')

        column_all = layout.column()

        row = column_all.row(align=True)
        split = row.split()
        r = split.column()
        r.prop(self, "activate", text="Show", toggle=True, icon=view_icon)
        row.prop(self, "draw_bg", text="Background", toggle=True)

        col = column_all.column(align=True)
        row = col.row(align=True)
        row.prop(self, "display_vert_index", toggle=True, icon='VERTEXSEL', text='')
        row.prop(self, "vert_idx_color", text="")
        if self.draw_bg:
            row.prop(self, "vert_bg_color", text="")

        row = col.row(align=True)
        row.prop(self, "display_edge_index", toggle=True, icon='EDGESEL', text='')
        row.prop(self, "edge_idx_color", text="")
        if self.draw_bg:
            row.prop(self, "edge_bg_color", text="")

        row = col.row(align=True)
        row.prop(self, "display_face_index", toggle=True, icon='FACESEL', text='')
        row.prop(self, "face_idx_color", text="")
        if self.draw_bg:
            row.prop(self, "face_bg_color", text="")


    def free(self):
        bgl_callback.callback_disable(self.node_id)



@stateful
class SvRxIndexView():

    bl_idname = "SvRxIndexView"
    label = "Index View"
    cls_bases = (NodeIndexView,)

    properties = {
        'activate': BoolP(name='activate', default=True),
        'draw_bg': BoolP(name='draw bg', default=False),
        "vert_idx_color": VectorP(size=4, min=0.0, max=1.0, default=(1., 1., 1., 1.), subtype='COLOR'),
        "edge_idx_color": VectorP(size=4, min=0.0, max=1.0, default=(1., 1., .1, 1.), subtype='COLOR'),
        "face_idx_color": VectorP(size=4, min=0.0, max=1.0, default=(1., .8, .8, 1.), subtype='COLOR'),
        "vert_bg_color": VectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "edge_bg_color": VectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "face_bg_color": VectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "display_vert_index": BoolP(name='show_verts', default=True), 
        "display_edge_index": BoolP(name='show_edges', default=True),
        "display_face_index": BoolP(name='show_faces', default=True)
    }

    def __init__(self, node=None):
        if node is not None:
            self.node = node
            self.activate = node.activate
            self.n_id = node.node_id

    def start(self):
        self.bms = []
        self.mats = []


    @property
    def get_fx(self):
        params = [
           "vert_idx_color", "edge_idx_color", "face_idx_color",
           "vert_bg_color", "edge_bg_color", "face_bg_color",
           "display_vert_index", "display_edge_index", "display_face_index",
           "draw_bg"]

        fx = namedtuple('fx', params)
        for param_name in params:
            if param_name.endswith(('index', 'bg')):
                param_value = getattr(self.node, param_name)
            else:
                param_value = getattr(self.node, param_name)[:]
            setattr(fx, param_name, param_value)
        return fx


    @property
    def get_data(self):
        d = lambda: None
        d.bms = self.bms
        d.mats = self.mats
        return d


    @property
    def current_draw_data(self):
        args = namedtuple('args', ['fx', 'data'])
        args.fx = self.get_fx
        args.data = self.get_data
        return {
            'tree_name': self.node.id_data.name[:],
            'custom_function': draw_index_viz,
            'args': args
        }


    def stop(self):
        bgl_callback.callback_disable(self.n_id)
        if self.activate:
            bgl_callback.callback_enable(self.n_id, self.current_draw_data)


    def __call__(self, bm: BMesh = Required, matrix: Matrix = None):
        self.bms.append(bm)
        self.mats.append(matrix)
