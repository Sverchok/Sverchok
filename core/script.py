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


import importlib
import importlib.abc
import importlib.util
import sys

import bpy


class SvRxFinder(importlib.abc.MetaPathFinder):

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("svrx.nodes.script."):
            name = fullname.split(".")[-1]
            #text_name = _name_lookup.get(name, "")
            text_name = name
            if text_name in bpy.data.texts:
                return importlib.util.spec_from_loader(fullname, SvRxLoader(text_name))
            else:
                print("couldn't find file")

        elif fullname == "svrx.nodes.script":
            # load Module, right now uses real but empty module, will perhaps change
            pass
        return None




class SvRxLoader(importlib.abc.SourceLoader):

    def __init__(self, text):
        self._text = text

    def get_data(self, path):
        # here we should insert things and preprocss the file to make it valid
        # this will upset line numbers...
        standard_header = """from svrx.nodes.node_base import node_script; from svrx.typing import *"""
        source = "".join((standard_header,
                          bpy.data.texts[self._text].as_string()))
        return source

    def get_filename(self, fullname):
        return "<bpy.data.texts[{}]>".format(self._text)


def register():
    sys.meta_path.append(SvRxFinder())

def unregister():
    for finder in sys.meta_path[:]:
        if isinstance(finder, SvRxFinder):
            sys.meta_path.remove(finder)
