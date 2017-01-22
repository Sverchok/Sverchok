from svrx.nodes.node_base import node_func

from svrx.typing import Anytype


@node_func(bl_idname="SvRxDebugPrint")
def debug_print(data: Anytype = None):
    print(data)
