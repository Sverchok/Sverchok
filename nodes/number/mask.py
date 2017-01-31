
import numpy as np

from svrx.typing import Bool, Number, Required
from svrx.nodes.node_base import node_func


def array_as_cycle(a, shape):
    if a.shape == shape:
        return a
    new_a = np.empty(shape, dtype=a.dtype)
    for i in range(shape[0]):
        new_a[i] = a[i % len(a)]
    return new_a

@node_func(bl_idname="SvRxNodeMask")
def mask(mask: Bool = True, data: Number = Required
         ) -> (
         Bool("Mask"),
         Number("Data True"),
         Number("Data False")):
    real_mask = array_as_cycle(mask, data.shape)
    return real_mask, data[real_mask], data[np.logical_not(real_mask)]


@node_func(bl_idname='SvRxNodeMaskJoin')
def mask_join(mask: Bool = True,
              data_true: Number = Required,
              data_false: Number = Required
              ) -> Number("data"):
    data = np.empty(mask.shape, dtype=data_true.dtype)
    data[mask] = data_true
    data[np.logical_not(mask)] = data_false
    return data
