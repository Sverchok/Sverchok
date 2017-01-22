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
from itertools import chain, filterfalse
import collections

import numpy as np


class SvDataTree:
    def __init__(self, socket=None, node=None, prop=None):
        self.data = None
        self.children = []
        if socket:
            self.name = socket.node.name + ": " + socket.name
        elif node and prop:
            self.name = node.name + "." + prop
            self.data = getattr(node, prop)
        else:
            pass

        if not socket.is_linked:
            self.data = np.array([socket.default_value])

    @property
    def is_leaf(self):
        return self.data is not None

    def __repr__(self):
        if self.is_leaf:
            return "SvDataTree<{}>".format(self.data)
        else:
            return "SvDataTree<children={}>".format(len(self.children))

    def print(self, level=0):
        if self.name:
            print(self.name)
        if self.is_leaf:
            print(level * "    ", self.data)
        else:
            for child in self.children:
                child.print(level + 1)

    def __iter__(self):
        if self.is_leaf:
            yield self.data
        else:
            for v in chain(map(iter, self.children)):
                yield from v

    def set_level(self, level=0):
        self.level = level
        if self.is_leaf:
            return level
        else:
            for child in self.children:
                child.set_level(level + 1)

    def get_level(self):
        if self.is_leaf:
            return 1
        else:
            return 1 + self.children[0].get_level()
