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

import collections
from itertools import chain

import svrx
from svrx.core.data_tree import SvDataTree
from svrx.core.type_conversion import needs_conversion, get_conversion
from svrx.nodes.node_base import Stateful


class SvTreeDB:
    """
    Data storage loookup for sockets
    """
    def __init__(self):
        self.data_trees = {}

    def print(self, ng):
        for link in ng.links:
            self.get(link.from_socket).print()

    def get(self, socket):
        ng_id = socket.id_data.name

        if ng_id not in self.data_trees:
            self.data_trees[ng_id] = {}
        ng_trees = self.data_trees[ng_id]
        if socket not in ng_trees:
            ng_trees[socket] = SvDataTree(socket=socket)
        return ng_trees[socket]

    def clean(self, ng):
        ng_id = ng.name
        self.data_trees[ng_id] = {}

data_trees = SvTreeDB()


class VirtualNode:
    """
    Used to represent node that don't have real conterpart in the layout
    """
    bl_idname = "VirtualNode"

    def __init__(self, func, ng):
        self.func = func
        self.id_data = ng
        self.inputs = []
        for _, name, default in func.inputs_template:
            self.inputs.append(VirtualSocket(self, name=name, default=default))
        self.outputs = [VirtualSocket(self) for _ in func.returns]
        self.name = "VirtualNode<{}>".format(func.label)

    def compile(self):
        return self.func

class VirtualLink:
    bl_idname = "VirtualLink"
    def __init__(self, from_socket, to_socket):
        self.from_socket = from_socket
        self.from_node = from_socket.node
        self.to_node = to_socket.node
        self.to_socket = to_socket

        if isinstance(from_socket, VirtualSocket):
            from_socket.is_linked = True

        if isinstance(to_socket, VirtualSocket):
            to_socket.is_linked = True
            to_socket.other = from_socket

class VirtualSocket:
    def __init__(self, node, name=None, default=None):
        self.name = name or "VirtualSocket"
        self.node = node
        self.id_data = node.id_data
        self.default_value = default
        self.is_linked = False

def topo_sort(links, starts):
    """
    links = {node: [node0, node1, ..., nodeN]}
    starts, nodes to start from
    return a topologiclly sorted list
    """
    weights = collections.defaultdict(lambda: -1)

    def visit(node, weight):
        weights[node] = max(weight, weights[node])
        for from_node in links[node]:
            visit(from_node, weight + 1)

    for start in starts:
        visit(start, 0)
    return sorted(weights.keys(), key=lambda n: -weights[n])


def filter_reroute(ng):
    links = []
    for l in ng.links:
        if not l.is_valid:
            return []
        if l.to_node.bl_idname == 'NodeReroute':
            continue
        if l.from_node.bl_idname == 'NodeReroute':
            links.append(VirtualLink(l.to_socket.other, l.to_socket))
        else:
            links.append(l)

    return links


def verify_links(links, nodes, socket_links):
    skip = set()
    for i in range(len(links)):
        l = links[i]
        if l.from_node not in nodes:
             nodes[l.from_node] = l.from_node.compile()
        if l.to_node not in nodes:
             nodes[l.to_node] = l.to_node.compile()
        to_func = nodes[l.to_node]
        from_func = nodes[l.from_node]
        from_type = from_func.returns[l.from_socket.index][0]

        to_type = None
        socket_index = l.to_socket.index
        for index, _, s_type in to_func.parameters:
            if index == socket_index:
                to_type = s_type
        print(from_type, to_type)
        if needs_conversion(from_type, to_type):
            print("found in converion_table")
            skip.add(i)
            func, to_index, from_index = get_conversion(from_type, to_type)
            node = VirtualNode(func, l.id_data)
            nodes[node] = func
            for idx in to_index:
                links.append(VirtualLink(l.from_socket, node.inputs[idx]))
            links.append(VirtualLink(node.outputs[from_index], l.to_socket))

    real_links = collections.defaultdict(list)

    for idx, l in enumerate(links):
        if idx in skip:
            continue
        real_links[l.to_node].append(l.from_node)
        socket_links[l.to_socket] = l.from_socket

    return real_links


def DAG(ng, nodes, socket_links):
    """
    preprocess the node layout in suitable way
    for topo_sort, removing reroutes and verifying
    type info
    """

    # needs to preprocess certain things
    # 1. reroutes, done
    # 2. type inf, done
    # 3. wifi node replacement

    links = filter_reroute(ng)

    real_links = verify_links(links, nodes, socket_links)

    from_nodes = set(node for node in chain(*real_links.values()))
    starts = {node for node in real_links.keys() if node not in from_nodes}

    nodes = starts.union(from_nodes)
    node_list = topo_sort(real_links, starts)
    print([n.name for n in node_list])
    return node_list


def recurse_levels(f, in_levels, out_levels, in_trees, out_trees):
    """
    does the exec for each node by recursively matching input trees
    and building output tree
    """

    if all(t.level == l for t, l in zip(in_trees, in_levels)):
        """
        All tree levels a correct, build arguments for node func
        call it and store results
        """
        args = []
        for tree in in_trees:
            if tree.level == 0:
                args.append(tree.data)
            else:
                args.append(list(tree))
        results = f(*args)
        if len(out_trees) > 1:
            if any(l > 0 for l in out_levels):
                results = zip(*results)
            for out_tree, l, result in zip(out_trees, out_levels, results):
                if out_tree:
                    out_tree.assign(l, result)
        elif len(out_trees) == 1 and out_trees[0]:  # results is a single socket
            out_trees[0].assign(out_levels[0], results)
        else:  # no output
            pass
    else:
        inner_trees = []
        max_length = 1
        for tree, l in zip(in_trees, in_levels):
            if tree.level != l:
                inner_trees.append(tree.children)
                max_length = max(len(tree.children), max_length)
            else:
                inner_trees.append(None)

        for i in range(max_length):
            args = []
            for tree, inner_tree in zip(in_trees, inner_trees):
                if inner_tree is None:
                    args.append(tree)
                else:
                    if i < len(inner_tree):
                        args.append(inner_tree[i])
                    else:
                        args.append(inner_tree[-1])

            outs = []
            for ot in out_trees:
                if ot:
                    outs.append(ot.add_child())
                else:
                    outs.append(None)

            recurse_levels(f, in_levels, out_levels, args, outs)


def exec_node_group(node_group):
    print("exec tree")
    data_trees.clean(node_group)
    nodes = {}
    socket_links = {}
    for node in DAG(node_group, nodes, socket_links):
        #print("exec node", node.name)
        func = nodes[node]
        if isinstance(func, Stateful):
            func.start()

        out_trees = []
        in_trees = []
        in_levels = []

        for param, level, data_type in func.parameters:
            in_levels.append(level)
            #  int refers to socket index, str to a property name on the node
            if isinstance(param, int):
                socket = node.inputs[param]
                if socket.is_linked:
                    other = socket_links[socket]
                    tree = data_trees.get(other)
                else:
                    tree = SvDataTree(socket)
            else:  # prop parameter
                tree = SvDataTree(node=node, prop=param)
            in_trees.append(tree)

        for socket in node.outputs:
            if socket.is_linked:
                out_trees.append(data_trees.get(socket))
            else:
                out_trees.append(None)

        recurse_levels(func, in_levels , [l for _, l in func.returns], in_trees, out_trees)
        if isinstance(func, Stateful):
            func.stop()
        #print("finished with node", node.name)
        for ot in out_trees:
            if ot:
                ot.set_level()
                #ot.print()
