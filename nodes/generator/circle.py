
from svrx.nodes.node_base import node_func
from svrx.typing import Int, Float, Vertices, Edges, Faces

from svrx.util.geom import circles


@node_func(bl_idname="SvRxNodeCircle", label="Circle")
def circle(nr_verts: Int = 24,
           radius: Float = 1.0
           ) -> ([Vertices],
                 [Edges],
                 [Faces]):
    return list(circles(radius, [0], nr_verts))
