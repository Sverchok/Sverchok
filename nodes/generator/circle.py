from svrx.typing import Int, Float, Vertices, Edges, Faces

import svrx.util.geom

@node_func
def circle(
          count: Int, radius: Float = 1.0
          ) -> (
          Vertices,
          Edges,
          Faces
          ):
    return geom.circle(count, radius)
