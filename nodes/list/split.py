from svrx.typing import Anytype, Int, Required

from svrx.nodes.node_base import node_func

import numpy as np



@node_func(bl_idname="SvRxNodeListSplit")
def split(size: Int = 1, data: Anytype = Required) -> [Anytype("Data")]:
    if size.size == 1:
        s = range(size[0], data.shape[0], size[0])
    else:
        s = size
    return np.split(data, s)
