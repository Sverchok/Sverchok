
from functools import wraps
import numpy as np

from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int

local_name = 'SvRxNodeTrig'

'''over view

-  SINE
-  COSINE
-  TANGENT
-  ARCSINE
-  ARCCOSINE
-  ARCTANGENT
-  DEGREES
-  RADIANS
-  ACOSH
-  ASINH
-  ATANH
-  COSH
-  SINH
-  TANH
-  PI * N, where N defaults to 1.0
-  PHI * N
-  TAU * N
-  SIN(x), COS(x)

'''


@node_func(bl_idname=local_name, multi_label="TRIG", id=0)
def add(x: Number = 0.0, y: Number = 0.0) -> Number:
    return x + y

@node_func(bl_idname=local_name, id=1)
def negate(x: Number = 0.0) -> Number:
    return -x

#  Constants

def constant(func):
    @wraps(func)
    def inner():
        return np.array([func()])
    return inner


@node_func(bl_idname=local_name, id=60)
@constant
def pi() -> Float:
    return np.pi

@node_func(bl_idname=local_name, id=61)
@constant
def tau() -> Float:
    return np.pi*2
