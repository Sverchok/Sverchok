from svrx.nodes.node_base import node_func
from svrx.typing import Float, Vertices

import numpy as np

@node_func(bl_idname="SvRxNodeVectorIn")
def vector_in(x: Float = 0.0,
              y: Float = 0.0,
              z: Float = 0.0,
              w: Float = 1.0
              ) -> Vertices:
    """create vertices from inputs"""
    data = (x, y, z, w)
    counts = [len(x) for x in data]
    verts = np.empty((max(counts), 4))
    for i, count in zip(range(4), counts):
        verts[:count, i] = data[i]
        verts[count:, i] = data[i][-1]
    return verts
