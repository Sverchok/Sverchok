import numpy as np

from svrx.typing import Vertices, Float
from svrx.util.function import make_compatible

# pylint: disable=C0326
null_vector = (0.0, 0.0, 0.0)

def add(u: Vertices = null_vector, v: Vertices = null_vector ) -> Vertices:
    u, v = make_compatible(u, v)
    return u + v


def sub(u: Vertices = null_vector, v: Vertices = null_vector ) -> Vertices:
    u, v = make_compatible(u, v)
    return u - v


def cross(u: Vertices = null_vector, v: Vertices = null_vector ) -> Vertices:
    u, v = make_compatible(u, v)
    return np.cross(u, v)


def scale(u: Vertices = null_vector, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    return u * s


def scale_reciprocal(u: Vertices = null_vector, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    return u * (1 / s)


def length(u: Vertices = null_vector ) -> Float:
    return np.linalg.norm(u, axis=0)


def dot(u: Vertices = null_vector, v: Vertices = null_vector ) -> Float:
    return u.dot(v)  # .. not sure


def opposite(u: Vertices = null_vector ) -> Vertices:
    return -u


def distance(u: Vertices = null_vector, v: Vertices = null_vector ) -> Float:
    # speed!?  http://stackoverflow.com/a/9184560/1243487
    u, v = make_compatible(u, v)
    x = u - v
    return np.sqrt(x * x)


def rx_round(u: Vertices = null_vector, n: Int = 7 ) -> Vertices:
    return np.round_(u, n)



func_list = {
    "Cross":    (1, cross),
    "Add":      (4, add),
    "Sub":      (8, sub),
    "Scale":    (12, scale),
    "1/Scale":  (16, scale_reciprocal),    
    "Length":   (20, length),
    "Dot":      (24, dot),
    "Opposite": (30, opposite),
    "Distance": (40, distance),
    "Round":    (50, rx_round)
}

"""
class SvrxVectorMathNode:

    mode = EnumProperty(items=func_list)

    @property
    def function(self):
        return func_dict[self.mode]
"""
