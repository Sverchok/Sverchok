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
from bpy.app.handlers import persistent


def svrx_trees():
    for ng in bpy.data.node_groups:
        if ng.bl_idname == 'SvRxTree':
            yield ng


@persistent
def sv_main_handler(scene):
    """
    Main Sverchok handler for updating node tree upon editor changes
    """
    for ng in svrx_trees():
        if ng.has_changed:
            ng.execute()


def register():
    bpy.app.handlers.scene_update_pre.append(sv_main_handler)


def unregister():
    bpy.app.handlers.scene_update_pre.remove(sv_main_handler)
