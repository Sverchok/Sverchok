#  ***** BEGIN GPL LICENSE BLOCK *****
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
#  along with this program; if not, see <http://www.gnu.org/licenses/>
#  and write to the Free Software Foundation, Inc., 51 Franklin Street,
#  Fifth Floor, Boston, MA  02110-1301, USA..
#
#  The Original Code is Copyright (C) 2015 by Gorodetskiy Nikita  ###
#  All rights reserved.
#
#  Contact:      linusyng@live.com    ###
#
#  The Original Code is: all of this file.
#
#  Contributor(s):
#     Linus Yng (aka Ly29)
#
#  ***** END GPL LICENSE BLOCK *****
#
# -*- coding: utf-8 -*-

import importlib
import pkgutil

bl_info = {
    "name": "SverchokRedux",
    "author":
        "ly29",
    "version": (0, 6, 0, 0),
    "blender": (2, 7, 8),
    "location": "Nodes > Ghost > Add user nodes",
    "description": "Parametric node-based geometry programming",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}


# Recursive auto import,
# http://stackoverflow.com/a/25562415

def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages
    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        print(name)
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


imported_modules = import_submodules(__name__)

reload_event = bool("bpy" in locals())

if reload_event:
    print("SvRx reloading")
    for im in imported_modules.values():
        importlib.reload(im)

# this is used as a marker for reload
import bpy


def register():

    for m in imported_modules.values():
        if hasattr(m, "register"):
            m.register()
    bpy.utils.register_module(__name__)
    if reload_event:
        print("SvRx is reloaded, press update")


def unregister():
    bpy.utils.unregister_module(__name__)

    for m in reversed(list(imported_modules.values())):
        if hasattr(m, "unregister"):
            m.unregister()
