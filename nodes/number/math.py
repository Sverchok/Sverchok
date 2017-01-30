
from functools import wraps
import numpy as np

from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int

@node_func(bl_idname='SvRxNodeMath', multi_label="MATH", id=0)
def add(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x + y

@node_func(bl_idname='SvRxNodeMath', id=1)
def negate(x: Number = 0.0) -> Number:
    return -x

#  Constants

def constant(func):
    @wraps(func)
    def inner():
        return np.array([func()])
    return inner


@node_func(bl_idname='SvRxNodeMath', id=60)
@constant
def pi() -> Float:
    return np.pi

@node_func(bl_idname='SvRxNodeMath', id=61)
@constant
def e() -> Float:
    return np.e
