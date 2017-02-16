import math
import numpy as np
import mathutils
from svrx.nodes.node_base import node_func
from svrx.util.transforms import translation_matrix, concatenate_matrices, scale_matrix
from svrx.util.geom import generator


from svrx.typing import Vector, Float, Matrix


@node_func(bl_idname="SvRxNodeCreateMatrix")
@generator
def create_matrix(location: Vector = (0.0, 0.0, 0.0, 1.0),
                  scale: Vector = (1.0, 1.0, 1.0, 0.0),
                  rotation: Vector = (0.0, 0.0, 1.0, 0.0),
                  angle: Float = 0.0
                  ) -> [Matrix]:

    #t = translation_matrix(location)
    s = np.identity(4)
    for i in range(3):
        s[i,i] = scale[i]
        s[i, 3] = location[i]
    r = rotation_matrix(math.radians(angle), rotation)
    return s.dot(r)


def rotation_matrix(theta, axis):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    Adapted from
    http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
    """
    axis = axis[:3]
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac), 0],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab), 0],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc, 0],
                     [0,         0,         0,           1]])
