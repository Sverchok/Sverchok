
import numpy as np

from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int
from svrx.util.function import constant, draw_label


@node_func(bl_idname='SvRxNodeMath', multi_label="Math", id=0, draw_label=draw_label)
def add(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x + y

@node_func(bl_idname='SvRxNodeMath', id=1)
def sub(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x - y

@node_func(bl_idname='SvRxNodeMath', id=2)
def mul(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x * y

@node_func(bl_idname='SvRxNodeMath', id=3)
def div(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x / y

@node_func(bl_idname='SvRxNodeMath', id=4)
def sqrt(x: Number = 1.0) -> Number:
    return x ** .5


@node_func(bl_idname='SvRxNodeMath', id=10)
def negate(x: Number = 0.0) -> Number:
    return -x

@node_func(bl_idname='SvRxNodeMath', id=11)
def add_1(x: Number = 0.0) -> Number:
    return x + 1

@node_func(bl_idname='SvRxNodeMath', id=12)
def sub_1(x: Number = 0.0) -> Number:
    return x - 1

@node_func(bl_idname='SvRxNodeMath', id=13)
def div_2(x: Number = 0.0) -> Number:
    return x / 2

@node_func(bl_idname='SvRxNodeMath', id=14)
def mul_2(x: Number = 0.0) -> Number:
    return x * 2

@node_func(bl_idname='SvRxNodeMath', id=15)
def as_int(x: Number = 0.0) -> Int:
    return x.astype(int)

@node_func(bl_idname='SvRxNodeMath', id=16)
def round(x: Number = 0.0, y: Int = 0) -> Float:
    return x.round(y)



@node_func(bl_idname='SvRxNodeMath', id=60)
@constant
def pi() -> Float:
    return np.pi

@node_func(bl_idname='SvRxNodeMath', id=61)
@constant
def e() -> Float:
    return np.e
