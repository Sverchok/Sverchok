import numpy as np

import bpy

from svrx.typing import IntValue, FloatValue, PointValue, ColorValue, ObjectValue, Int
from svrx.nodes.node_base import stateful, node_func
from svrx.nodes.classes import NodeBase


class NodeFrameInfo(NodeBase):

    def draw_buttons(self, context, layout):
        row = layout.row()
        scene = context.scene
        screen = context.screen
        """
        box = row.box()
        box.prop(scene, "frame_start")
        box.prop(scene, "frame_end")
        """
        row.prop(scene, "frame_current", text="")
        if not screen.is_animation_playing:
            row.operator("screen.animation_play", text="", icon='PLAY')
        else:
            row.operator("screen.animation_play", text="", icon='PAUSE')


class ValueNodeCommon:
    def __init__(self, node=None):
        if node and node.outputs:
            self.value = node.outputs[0].default_value
        else:
            self.value = None


@node_func(bl_idname="SvRxNodeFrameChange", cls_bases=(NodeFrameInfo,))
def frame_change() -> (Int("Current"), Int("Frame Start"), Int("Frame End")):
    scene = bpy.context.scene
    current = scene.frame_current
    start = scene.frame_start
    end = scene.frame_end
    return np.atleast_1d(current), np.atleast_1d(start), np.atleast_1d(end)


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
        return np.array(self.value)


@stateful
class ColorValue(ValueNodeCommon):
    bl_idname = "SvRxNodeColorValue"
    label = "Color input"

    def __call__(self) -> ColorValue("c"):
        return np.array(self.value)


@stateful
class ObjectValue(ValueNodeCommon):
    bl_idname = "SvRxNodeObjectValue"
    label = "Object input"

    def __call__(self) -> ObjectValue("o"):
        return bpy.data.objects.get(self.value)
