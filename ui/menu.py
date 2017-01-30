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
import svrx.nodes.node_base

from collections import OrderedDict, defaultdict

from nodeitems_utils import NodeCategory, NodeItem
import nodeitems_utils


class SvRxNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SvRxTree'


def make_node_cats():

    node_cats = OrderedDict()
    node_funcs = svrx.nodes.node_base._node_funcs
    node_classes = svrx.nodes.node_base._node_classes
    cats = set(func.category for func in node_funcs.values())
    cats = cats.union(cls.category for cls in node_classes.values())

    for cat in sorted(cats):
        nodes = [func.cls for func in node_funcs.values() if func.category == cat]
        nodes += [cls.node_cls for cls in node_classes.values() if cls.category == cat]
        node_cat = sorted([(node.bl_idname, node.bl_label) for node in nodes],
                          key=lambda x: x[1])
        node_cats[cat.title()] = node_cat

    return node_cats


def make_categories():
    node_cats = make_node_cats()

    node_categories = []
    node_count = 0
    for category, nodes in node_cats.items():
        name_big = "SVRX_" + category
        node_categories.append(SvRxNodeCategory(
            name_big, category,
            # bl_idname, name
            items=[NodeItem(*data) for data in nodes]))
        node_count += len(nodes)

    return node_categories, node_count


def reload_menu():
    menu, node_count = make_categories()
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
    nodeitems_utils.register_node_categories("SVRX", menu)


def register():
    menu, node_count = make_categories()
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
    nodeitems_utils.register_node_categories("SVRX", menu)


def unregister():
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
