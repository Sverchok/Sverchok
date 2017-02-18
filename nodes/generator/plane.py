from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, Vertices, Edges, Faces

import numpy as np
from svrx.util.geom import generator
from svrx.util.topology import plane_edges, plane_faces

def plane_verts(t_x, t_y):
    """
    make plane from grid in x coord and y coord
    """
    verts = np.empty((t_y.size, t_x.size, 4))
    x_l, y_l = np.meshgrid(t_x, t_y)
    verts[:,:,0] = x_l
    verts[:,:,1] = y_l
    verts[:,:,2] = 0
    verts[:,:,3] = 1
    verts.shape = (-1, 4)
    return verts

@node_func(bl_idname="SvRxNodeGenPlane", multi_label="Plane", id=0)
@generator
def grid(x: Int = 10,
         y: Int = 10,
         size: Float = 10) -> ([Vertices], [Edges], [Faces]):
    t_x = np.linspace(-size, size, x)
    t_y = np.linspace(-size, size, y)
    return plane_verts(t_x, t_y), plane_edges(x, y), plane_faces(y, x)


@node_func(bl_idname="SvRxNodeGenPlane", multi_label="Plane", id=1)
@generator
def plane(x: Int = 10,
          y: Int = 10,
          step_x: Float = 1.0,
          step_y: Float = 1.0) -> ([Vertices], [Edges], [Faces]):
    t_x = np.linspace(0, (x - 1) * step_x, x)
    t_y = np.linspace(0, (y - 1) * step_y, y)
    return plane_verts(t_x, t_y), plane_edges(x, y), plane_faces(y, x)
