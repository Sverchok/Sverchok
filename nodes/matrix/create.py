import numpy as np
from svrx.nodes.node_base import node_func

from svrx.typing import Vector, Float, Matrix


@node_func(bl_idname="SvRxNodeCreateMatrix")
def create_matrix(location: Vector = (0.0, 0.0, 0.0),
                 scale: Vector = (1.0, 1.0, 1.0),
                 rotation: Vector = (0.0, 0.0, 1.0),
                 angle: Float = 0.0
                 ) -> Matrix:

    pass
