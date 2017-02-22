import numpy as np

from svrx.nodes.node_base import node_func
from svrx.nodes.classes import NodeMathBase

from svrx.typing import Int

# pylint: disable=C0326
# pylint: disable=W0622
# pylint: disable=W0621

@node_func(bl_idname='SvRxNumberRangeInt', multi_label="Range", id=0, cls_bases=(NodeMathBase,))
def range(start: Int = 0, step: Int = 1, stop: Int = 10) -> [Int]:
    return np.arange(start, step, stop)

@node_func(id=1)
def count(start: Int = 0, step: Int = 1, count: Int = 10) -> [Int]:
    return np.arange(start, count*step, step)
