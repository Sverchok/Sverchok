import numpy as np
from svrx.nodes.node_base import node_func
from svrx.util.transforms import translation_matrix
from svrx.util.geom import vectorize

from svrx.typing import Vector, Float, Matrix, List


trans_mat = vectorize(translation_matrix)


@node_func(bl_idname="SvRxNodeCreateMatrix")
def create_matrix(location: Vector = (0.0, 0.0, 0.0),
                  scale: Vector = (1.0, 1.0, 1.0),
                  rotation: Vector = (0.0, 0.0, 1.0),
                  angle: Float = 0.0
                  ) -> List[Matrix]:

    return list(trans_mat(location))
