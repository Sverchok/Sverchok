import numpy as np

from svrx.util.function import constant, draw_label

from svrx.nodes.node_base import node_func
from svrx.typing import Number, Bool

@node_func(bl_idname='SvRxNodeLogic', multi_label='Logic', id=0, draw_label=draw_label)
def equal(x: Number = 0, y: Number= 0) -> Bool:
    return x == y

@node_func(bl_idname='SvRxNodeLogic', id=2)
def is_close(x: Number = 0, y: Number= 0) -> Bool:
    return np.isclose(x, y)

@node_func(bl_idname='SvRxNodeLogic', id=3)
def not_equal(x: Number = 0, y: Number = 0) -> Bool:
    return x != y

@node_func(bl_idname='SvRxNodeLogic', id=4)
def less_than(x: Number = 0, y: Number = 0) -> Bool:
    return x < y

@node_func(bl_idname='SvRxNodeLogic', id=5)
def bigger_than(x: Number = 0, y: Number = 0) -> Bool:
    return x > y

@node_func(bl_idname='SvRxNodeLogic', id=6)
def less_eq(x: Number = 0, y: Number = 0) -> Bool:
    return x <= y


@node_func(bl_idname='SvRxNodeLogic', id=7)
def bigger_eq(x: Number = 0, y: Number = 0) -> Bool:
    return x >= y


@node_func(bl_idname='SvRxNodeLogic', id=10)
@constant
def true() -> Bool:
    return False


@node_func(bl_idname='SvRxNodeLogic', id=11)
@constant
def false() -> Bool:
    return False


@node_func(bl_idname='SvRxNodeLogic', id=20)
def and_(a: Bool = True, b: Bool = False) -> Bool:
    return np.logical_and(a, b)


@node_func(bl_idname='SvRxNodeLogic', id=21)
def or_(a: Bool = True, b: Bool = False) -> Bool:
    return np.logical_or(a, b)


"""
TODO
    mode_items = [

        ("IF",              "If",           "", 3),
        ("NOT",             "Not",          "", 4),
        ("NAND",            "Nand",         "", 5),
        ("NOR",             "Nor",          "", 6),
        ("XOR",             "Xor",          "", 7),
        ("XNOR",            "Xnor",         "", 8),
"""
