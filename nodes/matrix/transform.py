from svrx.typing import Matrix, Vertices, Required
from svrx.nodes.node_base import node_func

import numpy as np

@node_func(bl_idname="SvRxMatrixTransform")
def transform(vertices: Vertices = Required,
              matrix: Matrix = Matrix.identity
              ) -> Vertices:
    return vertices.dot(matrix.T)
