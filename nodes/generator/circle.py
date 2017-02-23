
from svrx.nodes.node_base import node_func
from svrx.typing import Int, Float, Vertices, Edges, Faces

from svrx.util.geom import circle
from svrx.util.function import generator


@node_func(bl_idname="SvRxNodeCircle", label="Circle")
@generator
def circle_(nr_verts: Int = 24,
            radius: Float = 1.0
            ) -> ([Vertices],
                  [Edges],
                  [Faces]):
    return circle(radius, 0, nr_verts)
