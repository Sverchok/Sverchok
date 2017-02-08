import numpy as np

from svrx.typing import Vector, Float, Int, Vertices
from svrx.nodes.node_base import node_func

from svrx.util.function import make_compatible

X_AXIS = (1, 0, 0, 1)
Y_AXIS = (0, 1, 0, 1)
Z_AXIS = (0, 0, 1, 1)
ZEROS = (0, 0, 0, 1)

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
def add(u: Vector = ZEROS, v: Vector = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    max_len = max(u.shape[0], v.shape[0])
    out = np.zeros((max_len, 4))
    out[:,:3] = u[:,:3] + v[:,:3]
    out[:, 3] = max(u[0,3], v[0,3])
    return out

@node_func(id=6)
def sub(u: Vector = ZEROS, v: Vector = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    max_len = max(u.shape[0], v.shape[0])
    out = np.zeros((max_len, 4))
    out[:,:3] = u[:,:3] - v[:,:3]
    out[:, 3] = max(u[0,3], v[0,3])
    return out

@node_func(id=12)
def cross(u: Vector = ZEROS, v: Vector = ZEROS ) -> Vertices:
    u, v = make_compatible(u, v)
    u, v = make_compatible(u, v)
    max_len = max(u.shape[0], v.shape[0])
    out = np.zeros((max_len, 4))
    out[:,:3] = np.cross(u[:,:3], v[:,:3])
    return out

@node_func(id=18)
def scale(u: Vector = ZEROS, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    out = u.copy()
    out[:, :3] = u[:, :3] * s
    return out

@node_func(id=22)
def scale_reciprocal(u: Vector = ZEROS, s: Float = 1.0 ) -> Vertices:
    u, s = make_compatible(u, s)
    out = u.copy()
    out[:, :3] = u[:, :3] * (1 / s)
    return out

@node_func(id=26)
def length(u: Vector = ZEROS ) -> Float:
    tmp = u[:, :3]
    return np.sqrt((tmp * tmp).sum(axis=1))

@node_func(id=32)
def dot(u: Vector = ZEROS, v: Vector = ZEROS ) -> Float:
    u, v = make_compatible(u, v)
    return np.sum(u[:, :3] * v[:, :3], axis=1)  # .. not sure

@node_func(id=38)
def opposite(u: Vector = ZEROS ) -> Vertices:
    out = u.copy()
    out[:, :3] = -u[:, :3]
    return out

@node_func(id=44)
def distance(u: Vector = ZEROS, v: Vector = ZEROS ) -> Float:
    # speed!?  http://stackoverflow.com/a/9184560/1243487
    u, v = make_compatible(u, v)
    x = u[:, :3] - v[:, :3]
    return np.sqrt((x * x).sum(axis=1))

@node_func(id=48)
def round(u: Vector = ZEROS, n: Int = 7 ) -> Vertices:
    out = u.copy()
    out[:, :3] =  np.round(u[:, :3], n)
    return out

@node_func(id=50)
def normalize(u: Vector = ZEROS) -> Vertices:
    # placeholder
    # new_u = np.empty(np.shape(u))
    # for idx, v in enumerate(u):
    #     new_u[idx] = v / np.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    # return new_u
    out = u.copy()
    mag = length(u)
    out[:, :3] /= mag[:, np.newaxis]
    return out
