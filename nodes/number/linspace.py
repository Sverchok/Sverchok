import numpy as np

from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, List
from svrx.util.geom import vectorize

np_linspace = vectorize(np.linspace)

@node_func(bl_idname="SvRxNumberLinspace")
def linspace(start: Float = 0.0, stop: Float = 1.0, count: Int = 10
            ) -> List[Float]:
    out = []
    print("np_l enter", start, stop, count)
    for res in np_linspace(start, stop, count):
        print("np_linspace", res)
        out.append(res)
    return out
    return list(np_linspace(start, stop, count))
