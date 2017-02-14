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


class SvRxPanelDebug(bpy.types.Panel):
    bl_idname = "SvRxPanelDebug"
    bl_label = "SvRx Debug"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Sverchok Redux'
    use_pin = True

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.edit_tree.bl_idname == 'SvRxTree'
        except:
            return False

    def draw(self, context):
        layout = self.layout
        ng = context.space_data.edit_tree
        layout.label("Timings")
        layout.prop(ng, "do_timings_text")
        layout.prop(ng, "do_timings_graphics")
