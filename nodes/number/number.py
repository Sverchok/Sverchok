import numpy as np

from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, List
from svrx.util.geom import vectorize

np_linspace = vectorize(np.linspace)
np_arange = vectorize(np.arange)


@node_func(bl_idname="SvRxNumberLinspace")
def linspace(start: Float = 0.0,
             stop: Float = 1.0,
             count: Int = 10
             ) -> [Float]:
    print("np_l enter", start, stop, count)
    return list(np_linspace(start, stop, count))


@node_func(bl_idname="SvRxNumberArange")
def arange(start: Int = 0,
           stop: Int = 10,
           step: Int = 1) -> [Int]:
    return list(np_arange(start, stop, step))


@node_func(bl_idname="SvRxTestAdd")
def add(x: Float = 0.0, y: Float = 0.0) -> Float:
    return x + y
