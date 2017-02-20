
import numpy as np
import bpy


from svrx.typing import Anytype, Int, Vertices, BoolP

from svrx.nodes.node_base import node_func
from svrx.nodes.classes import MultiInputNode

from svrx.util.function import make_compatible

@node_func(bl_idname="SvRxNodeListJoin")
def join(data: [Anytype] = None) -> Anytype("Data"):
    return np.concatenate(data)


"""
class MergeNode(MultiInputNode):
    socket_type = bpy.props.StringProperty(default=Vertices.bl_idname)
    socket_base_name = bpy.props.StringProperty(default="Vert data {}")
"""
#@node_func(bl_idname="SvRxNodeListMerge", cls_bases = (MergeNode,))
#def merge(*vert_data: Vertices) -> Vertices:
#    return np.concatenate(vert_data)


@node_func(bl_idname="SvRxNodeListMerge")
def merge(a: Vertices = None,
          b: Vertices = None,
          mix: BoolP(description="interleave") = False) -> Vertices:
    if a is None:
        return b
    if b is None:
        return a
    if mix:
        a, b = make_compatible(a, b, broadcast=False)
        new_l = len(a) + len(b)
        out = np.empty((new_l, 4))
        out[::2] = a
        out[1::2] = b
        return out


    else:
        return np.concatenate((a, b))
