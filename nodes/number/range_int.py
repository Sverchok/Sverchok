import numpy as np

from svrx.nodes.node_base import node_func
from svrx.util.geom import generator
from svrx.typing import Int

# pylint: disable=C0326
# pylint: disable=W0622
# pylint: disable=W0621

@node_func(bl_idname='SvRxNumberRangeInt', multi_label="Range Int", id=0)
@generator
def range(start: Int = 0, step: Int = 1, stop: Int = 10) -> [Int]:
    if start == stop:
        return []
    step = max(step, 1)
    if stop < start:
        step *= -1
    return np.arange(start, stop, step)

@node_func(id=1)
@generator
def count(start: Int = 0, step: Int = 1, count: Int(min=0) = 10) -> [Int]:
    count = max(count, 0)
    if count == 0:
        return []
    stop = (count*step) + start
    return np.arange(start, stop, step)

