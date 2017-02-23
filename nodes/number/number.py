import numpy as np

from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int
from svrx.util.function import generator


@node_func(bl_idname="SvRxNumberLinspace")
@generator
def linspace(start: Float = 0.0,
             stop: Float = 1.0,
             count: Int = 10
             ) -> [Float]:
    return np.linspace(start, stop, count)


@node_func(bl_idname="SvRxNumberArange")
@generator
def arange(start: Int = 0,
           stop: Int = 10,
           step: Int = 1) -> [Int]:
    return np.arange(start, stop, step)
