

import numpy as np

from svrx.typing import Vertices, Float


def add(u: Vertices = (0.0, 0.0, 0.0),
        v: Vertices = (0.0, 0.0, 0.0)
        ) -> Vertices:
    u, v = make_compatible(u, v)
    return u + v


def sub(u: Vertices = (0.0, 0.0, 0.0),
        v: Vertices = (0.0, 0.0, 0.0)
        ) -> Vertices:
    u, v = make_compatible(u, v)
    return u - v


def cross(u: Vertices = (0.0, 0.0, 0.0),
          v: Vertices = (0.0, 0.0, 0.0)
          ) -> Vertices:
    u, v = make_compatible(u, v)
    return np.cross(u, v)


def scale(u: Vertices = (0.0, 0.0, 0.0),
          s: Float = 1.0
          ) -> Vertices:
    u, s = make_compatible(u, s)
    return u * s


def length(u: Vertices = (0.0, 0.0, 0.0)
           ) -> Float:
    return np.linalg.norm(u, axis=0)


def dot(u: Vertices = (0.0, 0.0, 0.0),
        v: Vertices = (0.0, 0.0, 0.0)
        ) -> Float:
    return u.dot(v)

func_list = {
    "Cross":  (1, cross),
    "Add":    (2, add),
    "Scale":  (3, sub),
    "Length": (4, length),
    "Dot":    (5, dot),
}

"""
class SvrxVectorMathNode:

    mode = EnumProperty(items=func_list)

    @property
    def function(self):
        return func_dict[self.mode]
"""
