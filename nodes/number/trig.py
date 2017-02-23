import numpy as np

from svrx.nodes.node_base import node_func
from svrx.nodes.classes import NodeMathBase
from svrx.typing import Number, Float


# pylint: disable=C0326
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


@node_func(bl_idname="SvRxNodeTrig",
           multi_label="Trigonometey",
           id=0, cls_bases=(NodeMathBase,))
def sine(x: Number = 0.0) -> Number:
    return np.sin(x)


@node_func(id=1)
def cosine(x: Number = 0.0) -> Number:
    return np.cos(x)


@node_func(id=2)
def sincos(x: Number = 0.0) -> (Number("sin"), Number("cos")):
    return np.sin(x), np.cos(x)


@node_func(id=3)
def degrees(x: Number = 0.0) -> Number:
    return np.degrees(x)


@node_func(id=4)
def radians(x: Number = 0.0) -> Number:
    return np.radians(x)


@node_func(id=20)
def tangent(x: Number = 0.0) -> Number:
    return np.tan(x)


@node_func(id=30)
def arcsine(x: Number = 0.0) -> Number:
    return np.asin(x)


@node_func(id=31)
def arcosine(x: Number = 0.0) -> Number:
    return np.acos(x)


@node_func(id=32)
def arctangent(x: Number = 0.0) -> Number:
    return np.atan(x)


@node_func(id=40)
def asinh(x: Number = 0.0) -> Number:
    return np.asinh(x)


@node_func(id=41)
def acosh(x: Number = 0.0) -> Number:
    return np.acosh(x)


@node_func(id=42)
def atanh(x: Number = 0.0) -> Number:
    return np.atanh(x)


@node_func(id=50)
def sinh(x: Number = 0.0) -> Number:
    return np.sinh(x)


@node_func(id=51)
def cosh(x: Number = 0.0) -> Number:
    return np.cosh(x)


@node_func(id=52)
def tanh(x: Number = 0.0) -> Number:
    return np.tanh(x)


#  Constants times input n


@node_func(id=60)
def pi(n: Number = 2.0) -> Number:
    return np.pi * n


@node_func(id=61)
def tau(n: Number = 1.0) -> Number:
    return np.pi * n * 2


PHI = ((1 + 5 ** 0.5) / 2)


@node_func(id=62)
def phi(n: Number = 1.0) -> Number:
    return PHI * n
