import numpy as np

from svrx.typing import IntValue, FloatValue, PointValue
from svrx.nodes.node_base import stateful


class ValueNodeCommon:
    def __init__(self, node=None):
        if node and node.outputs:
            self.value = node.outputs[0].default_value
        else:
            self.value = 0


@stateful
class IntNode(ValueNodeCommon):
    bl_idname = "SvRxNodeIntValue"
    label = "Int input"

    def __call__(self) -> IntValue("i"):
        return np.array([self.value])

@stateful
class FloatNode(ValueNodeCommon):
    bl_idname = "SvRxNodeFloatValue"
    label = "Float input"

    def __call__(self) -> FloatValue("f"):
        return np.array([self.value])

@stateful
class PointValue(ValueNodeCommon):
    bl_idname = "SvRxNodePointValue"
    label = "Point input"

    def __call__(self) -> PointValue("p"):
        return np.array([self.value])
