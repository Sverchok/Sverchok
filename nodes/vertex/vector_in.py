import numpy as np
Float = float
Vertices = [float]

def vector_in(x: Float = 0.0,
              y: Float = 0.0,
              z: Float = 0.0,
              w: Float = 1.0
              ) -> Vertices:
    """create vertices from inputs"""
    inputs = (x, y, z, w)
    counts = list(map(len, inputs))
    verts = np.empty((max(counts), 4))
    for i, count in zip(range(4), counts):
        verts[i, :count] = inputs[i]
        verts[i, count:] = inputs[i][-1]
    return verts
