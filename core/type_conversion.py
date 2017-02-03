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

from svrx.typing import Vertices, Vector, Point, Matrix, Number

converion_table = {}

def needs_conversion(from_type, to_type):
    return (from_type, to_type) in converion_table

def get_conversion(from_type, to_type):
    return converion_table[(from_type, to_type)]



def register():
    """
    done at register time to be able to use loaded nodes

    also this should be more clever and use the type hierarchy which
    should also be reworked
    """
    from svrx.nodes.matrix.create import create_matrix
    from svrx.nodes.vertex.vector_in import vector_in
    converion_table[(Vertices, Matrix)] = (create_matrix, (0,), 0)
    converion_table[(Number, Vector)] = (vector_in, (0, 1, 2), 0)
