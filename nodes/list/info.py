from svrx.typing import Anytype, Int, Float

from svrx.nodes.node_base import node_func
from svrx.util.function import std_wrap

import numpy as np



@node_func(bl_idname="SvRxNodeListInfo", multi_label="List info", id=0)
@std_wrap
def length(data: Anytype = None) -> Int("Length"):
    if data.size > 1:
        return data.shape[0]
    else:
        return data.size

@node_func(bl_idname="SvRxNodeListInfo", id=1)
@std_wrap
def min_(data: Anytype = None) -> Float("Min"):
    return data.min()


@node_func(bl_idname="SvRxNodeListInfo", id=2)
@std_wrap
def max_(data: Anytype = None) -> Float("Max"):
    return data.max()

@node_func(bl_idname="SvRxNodeListInfo", id=3)
@std_wrap
def sum_(data: Anytype = None) -> Float("Sum"):
    return data.sum()

@node_func(bl_idname="SvRxNodeListInfo", id=4)
@std_wrap
def mean_(data: Anytype = None) -> Float("Mean"):
    return data.mean()
