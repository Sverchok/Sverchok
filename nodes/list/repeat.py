import numpy as np
from svrx.nodes.classes import NodeMathBase
from svrx.nodes.node_base import node_func
from svrx.typing import Number, Int
from svrx.util.function import generator


@node_func(bl_idname='SvRxNodeListRepeat', multi_label="Repeat", id=0, cls_bases=(NodeMathBase,))
@generator
def np_repeat(Values: Number(iterable=False) = 0.0, Repeat: Int = 2) -> [Number]:
    return np.repeat(Values, Repeat)


@node_func(id=1)
@generator
def np_tile(Values: Number(iterable=False) = 0.0, Repeat: Int = 2) -> [Number]:
    return np.tile(Values, Repeat)
