
import numpy as np
import bpy


from svrx.typing import Anytype, Int, Vertices

from svrx.nodes.node_base import node_func
from svrx.nodes.classes import MultiInputNode

class MergeNode(MultiInputNode):
    socket_type = bpy.props.StringProperty(default=Vertices.bl_idname)
    socket_base_name = bpy.props.StringProperty(default="Vert data")

@node_func(bl_idname="SvRxNodeListJoin")
def join(data: [Anytype] = None) -> Anytype("Data"):
    return np.concatenate(data)


@node_func(bl_idname="SvRxNodeListMerge", cls_bases = (MergeNode,))
def merge(*vert_data: Vertices) -> Vertices:
    return np.concatenate(vert_data)
