import bpy
import bmesh
import time
from svrx.nodes.node_base import stateful
from svrx.typing import Vertices, Required, Faces, Edges, StringP, IntP, Matrix, BMesh, Anytype, BoolP
from svrx.util.mesh import bmesh_from_pydata
from svrx.util import bgl_callback 
# pylint: disable=C0326


def node_id(self):
    if not self.n_id:
        self.n_id = str(hash(self) ^ hash(time.monotonic()))
    return self.n_id

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
class SvRxStethoscope(Mesh_out_common):

    bl_idname = "SvRxStethoscope"
    label = "Stethoscope"

    properties = {
        'activate': BoolP(name='activate', default=True), 
        'n_id': bpy.props.StringProperty(default='')
    }

    def start(self):
        self.data = []

    def stop(self):
        n_id = node_id(self)
        bgl_callback.callback_disable(n_id)
        if self.activate:

            a = self.location[:]
            b = self.width[:]
            b[0] += 20
            x, y = int(a[0] + b[0]), int(a[1] + b[1])
            
            draw_data = {
                'tree_name': self.id_data.name[:],
                'custom_function': simple_grid_xy,
                'loc': (x, y),
                'args': (None, None)
            }
            bgl_callback.callback_enable(n_id, draw_data)


    def __call__(self, data: Anytype = Required):
        self.data.append(data)




