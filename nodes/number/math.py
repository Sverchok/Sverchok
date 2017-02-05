import numpy as np

from svrx.nodes.node_base import node_func
from svrx.nodes.classes import NodeMathBase

from svrx.typing import Number, Float, Int
from svrx.util.function import constant

# pylint: disable=C0326
# pylint: disable=W0622

@node_func(bl_idname='SvRxNodeMath', multi_label="Math", id=0, cls_bases=(NodeMathBase,))
def add(x: Number = 0.0, y: Number = 1.0) -> Number:
    return x + y

@node_func(id=1)
def sub(x: Number = 0.0, y: Number = 1.0) -> Number:
    return x - y

@node_func(id=2)
def mul(x: Number = 0.0, y: Number = 2.0) -> Number:
    return x * y

@node_func(id=3)
def div(x: Number = 1.0, y: Number = 2.0) -> Number:
    return x / y

@node_func(id=4)
def sqrt(x: Number = 1.0) -> Number:
    return np.sqrt(x)

@node_func(id=5)
def copy_sign(x: Number = 1.0, y: Number = -1.0) -> Number:
    return np.copysign(x, y)

@node_func(id=6)
def absolute(x: Number = -1.0) -> Number:
    return np.absolute(x)

@node_func(id=9)
def reciprocal(x: Number = 1.0) -> Number:
    return 1 / x

@node_func(id=10)
def negate(x: Number = 0.0) -> Number:
    return -x

@node_func(id=15)
def as_int(x: Number = 0.0) -> Int:
    return x.astype(int)

@node_func(id=17)
def round_n(x: Number = 0.0, y: Int = 0) -> Float:
    return x.round(y)

@node_func(id=20)
def ceil(x: Number = 1.0) -> Float:
    return np.ceil(x)

@node_func(id=21)
def ceil(x: Number = 1.5) -> Float:
    return np.floor(x)

@node_func(id=22)
def pow(x: Number = 1.0, y: Int = 2) -> Number:
    return np.power(x, y)

@node_func(id=24)
def exp(x: Number = 1.0) -> Number:
    return np.exp(x)

# each element individually compared returns smallest
@node_func(id=26)
def minimum(x1: Number = 1.0, x2: Number = -1.0) -> Number:
    return np.minimum(x1, x2)

# each element individually compared returns largest
@node_func(id=27)
def maximum(x1: Number = 1.0, x2: Number = -1.0) -> Number:
    return np.maximum(x1, x2)




@node_func(id=61)
@constant
def e() -> Float:
    return np.e
