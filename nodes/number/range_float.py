import numpy as np

from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, BoolP
from svrx.util.geom import generator


@node_func(bl_idname="SvRxNodeNumberFloat", multi_label='Range Float', id=0)
@generator
def space(start: Float = 0.0,
          stop: Float = 1.0,
          count: Int = 10,
          endpoint: BoolP(name='End point',
                          description='Last point is stop') = True
          ) -> [Float]:
    return np.linspace(start, stop, count, endpoint=endpoint)


@node_func(id=1)
@generator
def range(start: Float = 0.0,
          stop: Float = 1.0,
          step: Float = 0.1,
          ) -> [Float]:
    return np.arange(start, stop, step)


@node_func(id=2)
@generator
def step(start: Float = 0.0,
         step: Float = 1.0,
         count: Int = 10,
         ) -> [Float]:
    return np.arange(start, step * count + start, step)
