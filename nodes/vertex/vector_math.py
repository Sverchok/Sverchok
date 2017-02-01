import numpy as np

from svrx.typing import Vector, Float, Vertices
from svrx.nodes.node_base import node_func

from svrx.util.function import make_compatible

X_AXIS = (1, 0, 0)
Y_AXIS = (0, 1, 0)
Z_AXIS = (0, 0, 1)
ZERO = (1, 0, 0)


@node_func(bl_idname="SvRxVectorMathNode", multi_label="Vector Math", id=0)
def add(u: Vector = ZERO,
        v: Vector = ZERO
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
    return np.sqrt(u * u)


def dot(u: Vertices = (0.0, 0.0, 0.0),
        v: Vertices = (0.0, 0.0, 0.0)
        ) -> Float:
    return u.dot(v)


def opposite(u: Vertices = (0.0, 0.0, 0.0)) -> Vertices:
    return -u


def distance(u: Vertices = (0.0, 0.0, 0.0), v: Vertices = (0.0, 0.0, 0.0) ) -> Float:
    # speed!?  http://stackoverflow.com/a/9184560/1243487
    u, v = make_compatible(u, v)
    x = u - v
    return np.sqrt(x * x)
