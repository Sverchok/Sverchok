import numpy as np

import bmesh

from svrx.typing import Float, Int, Vector, BMesh, Required, Vertices
from svrx.nodes.node_base import node_func
from svrx.util.geom import generator
from svrx.util.function import std_wrap


@node_func(bl_idname='SvRxNodeBMeshInfo', multi_label='Bm info', id=0)
def face_info(bm: BMesh = Required
             ) -> (Float("Area"), Vertices("Center median")):
    faces = np.array([f.calc_area() for f in bm.faces])
    center = np.zeros((len(bm.faces), 4))
    center[:, :3] = np.array([f.calc_center_median() for f in bm.faces])
    return faces, center

@node_func(id=1)
@std_wrap
def volum(bm: BMesh = Required) -> Float("Volume"):
    return bm.calc_volume()
