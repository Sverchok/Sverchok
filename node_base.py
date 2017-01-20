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
import inspect

class NodeBase:

    def init(self):
        self.adjust_sockets()

    def adjust_sockets(self):

        for socket, socket_data in zip(self.inputs, self.inputs_template):
            socket.replace_socket(socket_data)

        diff = len(self.inputs) - len(self.inputs_template)

        if diff > 0:
            for i in range(diff):
                self.inputs.remove(self.inputs[-1])
        elif diff < 0:
            for bl_id, name, default in self.inputs_template[diff:]:
                s = self.inputs.new()
                s.default_value = default

        for socket, socket_data in zip(self.outputs, self.outputs_template):
            socket.replace_socket(socket_data)

        diff = len(self.outputs) - len(self.outputs_template)

        if diff > 0:
            for i in range(diff):
                self.outputs.remove(self.outputs[-1])
        elif diff < 0:
            for bl_id, name, default in self.outputs_template[diff:]:
                s = self.outputs.new()
                s.default_value = default


class NodeDynSignature(NodeBase):

    @property
    def function(self):
        return self.func_dict[self.mode]

_func_lookup = {}


def node_func(*args, **values):
    def real_node_func(func):
        def annotate(func):
            for key, value in values.items():
                setattr(func, key, value)
        annotate(func)
        print("annotating")
        get_signature(func)
        print("got sig")
        module_name = func.__module__.split(".")[-1]
        print("module:", module_name)
        _func_lookup[module_name] = func
        return func
    if args and callable(args[0]):
        return real_node_func(args[0])
    else:
        print(args, values)
        return real_node_func
