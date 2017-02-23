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
    final_step = np.copysign(step, stop)
    return np.arange(start, stop + final_step, final_step)

@node_func(id=1)
@generator
def count(start: Int = 0, step: Int = 1, count: Int = 10) -> [Int]:
    return np.arange(start, np.copysign(count * step, step), step)
