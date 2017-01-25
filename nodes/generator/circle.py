
from svrx.nodes.node_base import node_func
from svrx.typing import Int, Float, Vertices, Edges, Faces, List

from svrx.util.geom import circles


@node_func(bl_idname="SvRxNodeCircle", label="Circle")
def circle(count: Int = 24,
           radius: Float = 1.0
           ) -> (
           List[Vertices],
           List[Edges],
           List[Faces]
                ):
    return list(circles(count, radius))
