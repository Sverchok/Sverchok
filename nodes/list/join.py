from svrx.typing import Anytype, Int

from svrx.nodes.node_base import node_func

import numpy as np



@node_func(bl_idname="SvRxNodeListJoin")
def join(data: [Anytype] = None) -> Anytype("Data"):
    return np.concatenate(data)
