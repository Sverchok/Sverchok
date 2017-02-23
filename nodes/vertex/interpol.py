import numpy as np

from svrx.typing import Vertices, Float, Int, Required, FloatP

from svrx.util.geom import CubicSpline, LinearSpline
from svrx.util.function import generator
from svrx.nodes.node_base import node_func


@node_func(bl_idname="SvRxVertexInterpol", multi_label="Interpolation", id=0)
def cubic_spline(verts: Vertices = Required,
                 t: Float = 0.5,
                 h: FloatP = 0.001,
                 ) -> (Vertices, Vertices("Tanget")):
    spl = CubicSpline(verts[:, :3])
    points_out = np.ones((len(t), 4), dtype=np.float64)
    tangents_out = np.zeros((len(t), 4), dtype=np.float64)
    points_out[:, :3] = spl.eval(t)
    tangents_out[:, :3] = spl.tangent(t, h)
    return points_out, tangents_out


@node_func(id=2)
@generator
def cubic_spline_count(verts: Vertices(iterable=False) = Required,
                       count: Int = 10,
                       h: FloatP = 0.0001
                       ) -> ([Vertices], [Vertices("Tanget")]):
    return cubic_spline(verts, np.linspace(0.0, 1.0, count), h)


@node_func(bl_idname='SvRxVertexInterpol', id=1)
def linear_spline(verts: Vertices = Required,
                  t: Float = 0.5,
                  ) -> Vertices:
    spl = LinearSpline(verts[:, :3])
    points_out = np.ones((len(t), 4), dtype=np.float64)
    points_out[:, :3] = spl.eval(t)
    return points_out


"""
# sketches below

@node_func(bl_idname='SvRxVertexInterpol', id=2)
def surface_patch(verts : [Vertices] = Required,
                  u: Int = 10,
                  v: Int = 10
                  ) -> (
                  Vertices,
                  Vertices("Normal"),
                  Vertices("U tanget"),
                  Vertices("V tangent")):
    u_splines = []
    v_splines = []
    u_t = np.linspace(0, 1, u[0])
    v_t = np.linspace(0, 1, v[0])

    for vert in verts:
        u_splines.append(CubicSpline(verts))

    np.empty((u[0], 3))
    for u_spl in u_splines:
        u_spl.eval(u_t)
"""
