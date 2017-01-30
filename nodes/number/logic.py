from svrx.nodes.node_base import node_func
from svrx.typing import Number, Bool

@node_func(bl_idname='SvRxNodeLogic', multi_label='Logic', id=0)
def equal(x: Number = 0, y: Number: 0) -> Bool:
    return x == y

@node_func(bl_idname='SvRxNodeLogic', id=1)
def not_equal(x: Number = 0, y: Number: 0) -> Bool:
    return x != y

@node_func(bl_idname='SvRxNodeLogic', id=2)
def less_than(x: Number = 0, y: Number: 0) -> Bool:
    return x > y

@node_func(bl_idname='SvRxNodeLogic', id=2)
def bigger_than(x: Number = 0, y: Number: 0) -> Bool:
    return x > y
