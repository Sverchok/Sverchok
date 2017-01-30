from svrx.nodes.node_base import node_func
from svrx.typing import Float, Point

import numpy as np

@node_func(bl_idname="SvRxNodeVectorOut")
def vector_out(verts: Point = (0.0, 0.0, 0.0, 1.0)
              ) -> (Float("x"), Float("y"), Float("z"), Float("w")):
    return verts[:, 0], verts[:, 1], verts[:, 2], verts[:, 3]
