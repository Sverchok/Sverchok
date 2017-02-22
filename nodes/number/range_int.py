import numpy as np

from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int
from svrx.util.geom import generator



@node_func(bl_idname="SvRxNumberRangeInt")
@generator
def arange(start: Int = 0,
           stop: Int = 10,
           step: Int = 1) -> [Int]:
    return np.arange(start, stop, step)
