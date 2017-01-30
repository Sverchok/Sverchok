
from functools import wraps
import numpy as np

from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int

local_name = 'SvRxNodeTrig'

'''over view

-  SINE
-  COSINE
-  SIN(x), COS(x)
-  DEGREES
-  RADIANS
-  TANGENT
-  ARCSINE
-  ARCCOSINE
-  ARCTANGENT
  ACOSH
  ASINH
  ATANH
  COSH
  SINH
  TANH
  ----- divider ----
  PI * N, where N defaults to 1.0
  PHI * N
  TAU * N

'''

#  Constants wrapper
def constant(func):
    @wraps(func)
    def inner():
        return np.array([func()])
    return inner


@node_func(bl_idname=local_name, multi_label="TRIG", id=0)
def sine(x: Number = 0.0) -> Number:
    return sin(x)

@node_func(bl_idname=local_name, id=1)
def cosine(x: Number = 0.0) -> Number:
    return cos(x)

@node_func(bl_idname=local_name, id=2)
def sincos(x: Number = 0.0) -> Number, Number:
    return sin(s), cos(x)

@node_func(bl_idname=local_name, id=3)
def degrees(x: Number = 0.0) -> Number:
    return degrees(s)

@node_func(bl_idname=local_name, id=4)
def radians(x: Number = 0.0) -> Number:
    return radians(s)

@node_func(bl_idname=local_name, id=20)
def tangent(x: Number = 0.0) -> Number:
    return tan(x)

@node_func(bl_idname=local_name, id=30)
def arcsine(x: Number = 0.0) -> Number:
    return asin(x)

@node_func(bl_idname=local_name, id=40)
def arccosine(x: Number = 0.0) -> Number:
    return acos(x)

@node_func(bl_idname=local_name, id=50)
def arctangent(x: Number = 0.0) -> Number:
    return atan(x)


# @node_func(bl_idname=local_name, multi_label="TRIG", id=0)
# def sine(x: Number = 0.0, y: Number = 0.0) -> Number:
#     return sin(x)



@node_func(bl_idname=local_name, id=60)
@constant
def pi() -> Float:
    return np.pi

@node_func(bl_idname=local_name, id=61)
@constant
def tau() -> Float:
    return np.pi*2
