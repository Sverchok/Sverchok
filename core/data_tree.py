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
        self.name = ""
        self.level = None
        if socket:
            self.name = socket.node.name + ": " + socket.name
            self.level = 0
            if not socket.is_linked:
                self.data = np.array([socket.default_value])
        elif node and prop is not None:
            self.name = node.name + "." + prop
            self.data = getattr(node, prop)
            self.level = 0
        else:
            pass

    def add_child(self, data=None):
        self.children.append(SvDataTree())
        self.children[-1].data = data
        return self.children[-1]

    @property
    def is_leaf(self):
        return self.data is not None

    def __repr__(self):
        if self.is_leaf:
            return "SvDataTree<data={}, level={}>".format(self.data, self.level)
        else:
            return "SvDataTree<children={}, level={},d={}>".format(len(self.children), self.level, self.data)

    def print(self, level=0):
        if self.name:
            print(self.name, self.level)
        else:
            print(self.level)
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

    def set_level(self):
        if self.is_leaf:
            self.level = 0
        else:
            level = 0
            for child in self.children:
                level = max(child.set_level() + 1, level)
            self.level = level
        return self.level

    def get_level(self):
        return self.level

    def assign(self, level, data):
        if level == 0:
            self.data = data
            self.level = 0
        elif level == 1:
            for d in data:
                self.add_child(data=d).level = 0
            self.level = 1
