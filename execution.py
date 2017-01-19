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


class Node:

    def __init__(self, node):
        self.name = node.name


class NodeTree:

    def __init__(self, ng):
        self.name = ng.name

    def __iter__(self):
        end_nodes = magic_func()
        visited = set()
        node_stack = list(end_nodes)
        while node_stack:
            node = node_stack.pop()
            if all(n in seed for n in get_deps(node)):
                yield node
            else:
                node_stack.push(node)
                for n in get_deps:
                    if n not in visited:
                        node_stack.push(n)
