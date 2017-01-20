# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from bpy.props import (FloatProperty,
                       IntProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       StringProperty)


class SocketBase:
    default_value = None
    color = (1, 0, 0, 1)  # red to show unset colors

    def draw(self, context, layout, node, text):
        if self.default_value and not self.is_linked:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return self.color


class SocketNumber(SocketBase):
    color = (0.0, 0.8, 0.0, 1.0)


class IntSocket(bpy.types.NodeSocket, SocketNumber):
    bl_idname = "SvRxIntSocket"
    bl_label = "Int Socket"

    default_value = IntProperty()


class FloatSocket(bpy.types.NodeSocket, SocketNumber):
    bl_idname = "SvRxFloatSocket"
    bl_label = "Float Socket"

    default_value = FloatProperty()


class SocketVector(SocketBase):
    color = (0.9, 0.6, 0.2, 1.0)


class VertexSocket(bpy.types.NodeSocket, SocketVector):
    bl_idname = "SvRxVertexSocket"
    bl_label = "Vertex Socket"


class MatrixSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = "SvRxMatrixSocket"
    bl_label = "Matrix Socket"

    color = (.2, .8, .8, 1.0)


class VectorSocket(bpy.types.NodeSocket, SocketVector):
    bl_idname = "SvRxVectorSocket"
    bl_label = "Vector Socket"

    default_value = FloatVectorProperty(size=4)

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.template_component_menu(self, "default_value", name=text)
        else:
            super().draw(context, layout, node, text)


class ValueIntSocket(bpy.types.NodeSocket, SocketNumber):
    default_value = IntProperty()

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            pass
