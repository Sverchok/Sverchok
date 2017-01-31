import numpy as np

from svrx.typing import Vertices, Float, Int, Required, FloatP

from svrx.util.geom import CubicSpline, LinearSpline
from svrx.nodes.node_base import node_func
# sketches below
"""
@node_func(bl_idname="SvRxVertexInterpol", multi_label="Interpolation", id=0)
def cubic_spline(verts: Vertices = Required,
                 t: Float = 0.5,
                 h: FloatP = 0.001,
                ) -> (Vertices, Vertices("Tanget")):
    spl = CubicSpline(verts)
    return spl.eval(t), spl.tangent(t, h)

@node_func(bl_idname='SvRxVertexInterpol', id=1)
def liner_spline(verts: Vertices = Required,
                 t: Float = 0.5
                 ) -> Vertices:
    spl = LinearSpline(verts)
    return spl.eval(t)


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
