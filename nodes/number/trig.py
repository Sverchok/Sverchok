from functools import wraps
import numpy as np

from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int


# pylint: disable=C0326

local_name = 'SvRxNodeTrig'

'''
-  SINE     / COSINE     / SIN(x), COS(x) 
-  DEGREES  / RADIANS    / TANGENT
-  ARCSINE  / ARCCOSINE  / ARCTANGENT
-  ACOSH    / ASINH      / ATANH
-  COSH     / SINH       / TANH
  ----- divider ----
-  PI * N, where N defaults to 1.0 or 2.0
-  PHI * N
-  TAU * N
'''

#  Constants wrapper
def constant(func):
    @wraps(func)
    def inner():
        return np.array([func()])
    return inner

#  Constants wrapper
def constant_times_n(func):
    @wraps(func)
    def inner(*args):
        return np.array([func(*args)])
    return inner


@node_func(bl_idname=local_name, multi_label="TRIG", id=0)
def sine(x: Number = 0.0) -> Number:
    return np.sin(x)

@node_func(bl_idname=local_name, id=1)
def cosine(x: Number = 0.0) -> Number:
    return np.cos(x)

@node_func(bl_idname=local_name, id=2)
def sincos(x: Number = 0.0) -> ([Number], [Number]):
    return np.sin(x), np.cos(x)

@node_func(bl_idname=local_name, id=3)
def degrees(x: Number = 0.0) -> Number:
    return np.degrees(x)

@node_func(bl_idname=local_name, id=4)
def radians(x: Number = 0.0) -> Number:
    return np.radians(x)

@node_func(bl_idname=local_name, id=20)
def tangent(x: Number = 0.0) -> Number:
    return np.tan(x)

@node_func(bl_idname=local_name, id=30)
def arcsine(x: Number = 0.0) -> Number:
    return np.asin(x)

@node_func(bl_idname=local_name, id=31)
def arcosine(x: Number = 0.0) -> Number:
    return np.acos(x)

@node_func(bl_idname=local_name, id=32)
def arctangent(x: Number = 0.0) -> Number:
    return np.atan(x)

@node_func(bl_idname=local_name, id=40)
def asinh(x: Number = 0.0) -> Number:
    return np.asinh(x)

@node_func(bl_idname=local_name, id=41)
def acosh(x: Number = 0.0) -> Number:
    return np.acosh(x)

@node_func(bl_idname=local_name, id=42)
def atanh(x: Number = 0.0) -> Number:
    return np.atanh(x)

@node_func(bl_idname=local_name, id=50)
def sinh(x: Number = 0.0) -> Number:
    return np.sinh(x)

@node_func(bl_idname=local_name, id=51)
def cosh(x: Number = 0.0) -> Number:
    return np.cosh(x)

@node_func(bl_idname=local_name, id=52)
def tanh(x: Number = 0.0) -> Number:
    return np.tanh(x)

## Constants times input n

@node_func(bl_idname=local_name, id=60)
@constant_times_n
def pi(n: Number = 2.0) -> Number:
    return np.pi * n

@node_func(bl_idname=local_name, id=61)
@constant_times_n
def tau(n: Number = 1.0) -> Number:
    return np.pi * n * 2

@node_func(bl_idname=local_name, id=62)
@constant_times_n
def e(n: Number = 1.0) -> Number:
    return np.e * n



