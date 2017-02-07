import numpy as np

from svrx.typing import Vector, Float, Int, Vertices
from svrx.nodes.node_base import node_func

from svrx.util.function import make_compatible

X_AXIS = (1, 0, 0)
Y_AXIS = (0, 1, 0)
Z_AXIS = (0, 0, 1)
ZEROS = (0, 0, 0)

""" missing
- Angle Rad, 
- Angle Deg, 
- Project, 
- Reflect, 
- Componentwise-multiplication, 

"""

# pylint: disable=C0326
# pylint: disable=W0622 

@node_func(bl_idname="SvRxVectorMathNode", multi_label="Vector Math", id=0)
def add(u: Vertices = ZEROS, v: Vertices = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    return u + v

@node_func(id=6)
def sub(u: Vertices = ZEROS, v: Vertices = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    return u - v

@node_func(id=12)
def cross(u: Vertices = ZEROS, v: Vertices = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    return np.cross(u, v)

@node_func(id=18)
def scale(u: Vertices = ZEROS, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    return u * s

@node_func(id=22)
def scale_reciprocal(u: Vertices = ZEROS, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    return u * (1 / s)

@node_func(id=26)
def length(u: Vertices = ZEROS ) -> Float:
    return np.sqrt(u * u)

@node_func(id=32)
def dot(u: Vertices = ZEROS, v: Vertices = ZEROS ) -> Float:
    return u.dot(v)  # .. not sure

@node_func(id=38)
def opposite(u: Vertices = ZEROS ) -> Vertices:
    return -u

@node_func(id=44)
def distance(u: Vertices = ZEROS, v: Vertices = ZEROS ) -> Float:
    # speed!?  http://stackoverflow.com/a/9184560/1243487
    u, v = make_compatible(u, v)
    x = u - v
    return np.sqrt(x * x)

@node_func(id=48)
def round(u: Vertices = ZEROS, n: Int = 7 ) -> Vertices:
    return np.round_(u, n)

@node_func(id=50)
def normalize(u: Vertices = ZEROS) -> Vertices:
    # placeholder
    # new_u = np.empty(np.shape(u))
    # for idx, v in enumerate(u):
    #     new_u[idx] = v / np.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    # return new_u

    A = np.power(u, 2)
    B = np.sum(A, axis=1)
    C = np.sqrt(B)
    D = u / C[:, None]
    return D


"""
class SvrxVectorMathNode:

    mode = EnumProperty(items=func_list)

    @property
    def function(self):
        return func_dict[self.mode]
"""
