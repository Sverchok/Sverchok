import bpy
import bmesh

from svrx.nodes.node_base import stateful
from svrx.typing import Vertices, Required, Faces, Edges, StringP, IntP, Matrix, BMesh, Anytype
from svrx.util.mesh import bmesh_from_pydata
from svrx.util import bgl_callback 
# pylint: disable=C0326


@stateful
class SvRxStethoscope(Mesh_out_common):

    bl_idname = "SvRxStethoscope"
    label = "Stethoscope"

    properties = {'activate': BoolP(name='activate', default=True)}

    def start(self):
        self.data = []

    def stop(self):
        # n_id  ??
        bgl_callback.callback_disable(n_id)

        if self.activate:

            x, y = [int(j) for j in (self.location + Vector((self.width + 20, 0)))[:]]
            
            draw_data = {
                'tree_name': self.id_data.name[:],
                'custom_function': simple_grid_xy,
                'loc': (x, y),
                'args': (None, None)
            }
            bgl_callback.callback_enable(n_id, draw_data)


    def __call__(self, data: Anytype = Required):
        self.data.append(data)




