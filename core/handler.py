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

from svrx.core.tree import svrx_trees
from svrx.util import bgl_callback, bgl_callback_3dview
import svrx

@persistent
def sv_main_handler(scene):
    """
    Main Sverchok handler for updating node tree upon editor changes
    """
    reload_event = svrx.reload_event
    svrx.reload_event = False
    for ng in svrx_trees():
        if ng.has_changed or reload_event:
            ng.execute()


@persistent
def sv_file_load(scene):
    """
    To make sure nodes follow signature on node changes on startup
    clean up callbacks
    """

    for callback in (bgl_callback, bgl_callback_3dview):
        callback.callback_disable_all()

    for ng in svrx_trees():
        for node in ng.nodes:
            if node.bl_idname == "SvRxNodeScript":
                node.load_text()
            if hasattr(node, "adjust_sockets"):
                node.adjust_sockets()


@persistent
def frame_change(scene):
    for ng in svrx_trees():
        try:
            ng.execute_animate()
        except:
            pass
    scene.update()


def register():
    bpy.app.handlers.scene_update_pre.append(sv_main_handler)
    bpy.app.handlers.load_post.append(sv_file_load)
    bpy.app.handlers.frame_change_pre.append(frame_change)


def unregister():
    bpy.app.handlers.scene_update_pre.remove(sv_main_handler)
    bpy.app.handlers.load_post.remove(sv_file_load)
    bpy.app.handlers.frame_change_pre.remove(frame_change)
