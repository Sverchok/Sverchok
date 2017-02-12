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


import os
import functools

def mesh_objects_path():
    return os.path.join(os.path.dirname(__file__), 'mesh_objects')

def named_mesh_path(name):
    return os.path.join(mesh_objects_path(), name)

def get_sn_template_path():
    return os.path.join(os.path.dirname(__file__), 'snrx_templates')



@functools.lru_cache(maxsize=16)
def obj_to_pydata_lite(path):
    """Loads external .obj files in a very simple format. Cached
    """
    verts, edges, faces = [], [], []
    add_vert = verts.append
    add_face = faces.append
    with open(path) as ofile:
        for line in ofile:
            if line.startswith('v'):
                add_vert([float(i) for i in line[2:].strip().split(' ')])
            if line.startswith('f'):
                add_face([int(i)-1 for i in line[2:].strip().split(' ')])

    return verts, edges, faces

def uncached_obj_to_pydata_lite(path):
    """
    Bypasses the data cache for when are working with and changing the file.
    """
    return obj_to_pydata_lite.__wrapped__(path)

_text_file_lookup = {}

def text_remap(text_file, reverse=False):
    if not reverse:
        remap_name = make_valid_identifier(text_file)
        _text_file_lookup[remap_name] = text_file
        return  remap_name
    return _text_file_lookup.get(text_file)

def make_valid_identifier(name):
    """Create a valid python identifier from name for use a a part of class name"""
    if not name[0].isalpha():
        name = "SvRx" + name
    return "".join(ch for ch in name if ch.isalnum() or ch == "_")
