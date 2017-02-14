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

import time

import bpy
from bpy.props import BoolProperty

from svrx.core.execution import exec_node_group, DAG
from svrx.util import bgl_callback


class SverchokReduxTree(bpy.types.NodeTree):
    """
    Sverchok Redux visual programming language
    """
    bl_idname = 'SvRxTree'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'NODE'

    def turn_graphics_off(self, context):
        bgl_callback.callback_disable("timings:" + self.name)

    has_changed = BoolProperty(default=False)
    do_timings_text = BoolProperty(default=False)
    do_timings_graphics = BoolProperty(default=False, update=turn_graphics_off)


    def update(self):
        self.has_changed = True

    def execute(self):
        start = time.perf_counter()
        self.has_changed = False
        exec_node_group(self)
        self.has_changed = False
        stop = time.perf_counter()
        print(self.name, "{:f}".format(stop-start))

    def update_list(self):
        return DAG(self)
