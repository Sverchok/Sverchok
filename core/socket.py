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


def exec_socket(self, context):
    self.id_data.update()

def get_other_socket(socket):
    """
    Get next real upstream socket.
    This should be expanded to support wifi nodes also.
    Will return None if there isn't a another socket connect
    so no need to check socket.links
    """

    if not socket.is_linked:
        return None

    if not socket.is_output:
        other = socket.links[0].from_socket
    else:
        other = socket.links[0].to_socket

    if other.node.bl_idname == 'NodeReroute':
        if not socket.is_output:
            return get_other_socket(other.node.inputs[0])
        else:
            return get_other_socket(other.node.outputs[0])
    else:
        return other


class SocketBase:
    default_value = None
    color = (1, 0, 0, 1)  # red to show unset colors

    def draw(self, context, layout, node, text):

        if self.is_output or self.is_linked:
            layout.label(text)
        elif self.is_linked:
            layout.label(text)
        elif self.default_value is not None:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return self.color

    def replace_socket(self, bl_idname=None, name=None, default=None):
        replace_socket(self, new_type=bl_idname, new_name=name, default=default)

    @property
    def socket_id(self):
        return hash(self)

    @property
    def other(self):
        return get_other_socket(self)


def replace_socket(socket, new_type=None, new_name=None, default=None):
    '''
    Replace a socket with a socket of new_type and keep links
    '''

    socket_type = new_type or socket.bl_idname
    socket_name = new_name or socket.name

    ng = socket.id_data
    """
    terminate early leads to bugs
    if socket.bl_idname == socket_type:
        socket.name = new_name
        if default is not None:
            socket.default_value = default
        return
    """
    if socket.is_output:
        outputs = socket.node.outputs
        to_sockets = [l.to_socket for l in socket.links]

        outputs.remove(socket)
        new_socket = outputs.new(socket_type, socket_name)

        for to_socket in to_sockets:
            ng.links.new(new_socket, to_socket)

    else:
        inputs = socket.node.inputs
        from_socket = socket.links[0].from_socket if socket.is_linked else None

        inputs.remove(socket)
        new_socket = inputs.new(socket_type, socket_name)
        if default is not None:
            new_socket.default_value = default
        if from_socket:
            ng.links.new(from_socket, new_socket)

    return new_socket


class SocketNumber(SocketBase):
    color = (0.0, 0.8, 0.0, 1.0)


class IntSocket(bpy.types.NodeSocket, SocketNumber):
    bl_idname = "SvRxIntSocket"
    bl_label = "Int Socket"

    default_value = IntProperty(update=exec_socket)


class FloatSocket(bpy.types.NodeSocket, SocketNumber):
    bl_idname = "SvRxFloatSocket"
    bl_label = "Float Socket"

    default_value = FloatProperty(update=exec_socket)


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

    default_value = FloatVectorProperty(size=3, update=exec_socket)

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.template_component_menu(self, "default_value", name=text)
        else:
            super().draw(context, layout, node, text)


class PointSocket(bpy.types.NodeSocket, SocketVector):
    bl_idname = "SvRxPointSocket"
    bl_label = "Point Socket"

    default_value = FloatVectorProperty(size=4, update=exec_socket)

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.template_component_menu(self, "default_value", name=text)
        else:
            super().draw(context, layout, node, text)

class TopoSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = "SvRxTopoSocket"
    bl_label = "Topo Socket"

    color = (.1, .1, .1, 1)


class AnySocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = "SvRxAnySocket"
    bl_label = "Any Socket"

    color = (.9, .9, .9, 1.0)


class MeshSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = "SvRxMeshSocket"
    bl_label = "Any Socket"

    color = (.1, .1, .1, 1.0)


class ObjectSocket(bpy.types.NodeSocket, SocketBase):
    bl_idname = 'SvRxObjectSocket'
    bl_label = 'Blender Objects'

    color = (.2, .2, .2, 1.0)

    default_value = StringProperty(update=exec_socket)

    def draw(self, context, layout, node, text):
        if not self.is_output:
            if self.is_linked:
                layout.label(text)
            else:
                layout.prop_search(self, 'default_value', bpy.data, 'objects')
        else:
            layout.label(text)

class ValueSocket:
    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            pass

class ValueIntSocket(bpy.types.NodeSocket, ValueSocket, SocketNumber):
    bl_idname = "SvRxValueIntSocket"
    bl_label = "Value Int Socket"

    default_value = IntProperty(update=exec_socket)




class ValueFloatSocket(bpy.types.NodeSocket, ValueSocket, SocketNumber):
    bl_idname = "SvRxValueFloatSocket"
    bl_label = "Value Float Socket"

    default_value = FloatProperty(update=exec_socket)


class ValuePointSocket(bpy.types.NodeSocket, ValueSocket, SocketVector):
    bl_idname = "SvRxValuePointSocket"
    bl_label = "Value Point Socket"

    default_value = FloatVectorProperty(size=4, update=exec_socket)

    def draw(self, context, layout, node, text):
        if self.is_output:
            column = layout.column(align=True)
            for i in range(4):
                row = column.row(align=True)
                row.prop(self, "default_value", index=i, text='XYZW'[i])
