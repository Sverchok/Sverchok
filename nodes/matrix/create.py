import numpy as np
from svrx.nodes.node_base import node_func
from svrx.util.transforms import translation_matrix, concatenate_matrices, rotation_matrix, scale_matrix
from svrx.util.geom import vectorize

from svrx.typing import Vector, Float, Matrix


@vectorize
def mat_create(trans, scale, rotation, angle):
    t = translation_matrix(trans)
    s = np.identity(4)
    for i in range(3):
        s[i,i] = scale[i]
    r = rotation_matrix(np.radians(angle), rotation)
    mat = concatenate_matrices(t, s, r)
    return mat


@node_func(bl_idname="SvRxNodeCreateMatrix")
def create_matrix(location: Vector = (0.0, 0.0, 0.0, 1.0),
                  scale: Vector = (1.0, 1.0, 1.0, 0.0),
                  rotation: Vector = (0.0, 0.0, 1.0, 0.0),
                  angle: Float = 0.0
                  ) -> [Matrix]:

    return list(mat_create(location, scale, rotation, angle))
