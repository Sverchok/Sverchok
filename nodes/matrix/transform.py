from svrx.typing import Matrix, Vertices, Required
from svrx.nodes.node_base import node_func

import numpy as np


@node_func(bl_idname="SvRxNodeMatrixTransform")
def transform(vertices: Vertices = Required,
              matrix: Matrix = Matrix.identity
              ) -> Vertices:
    if matrix is None:
        return vertices
    else:
        return vertices.dot(matrix.T)
