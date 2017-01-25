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

import svrx
from svrx.core.data_tree import SvDataTree


class SvTreeDB:
    def __init__(self):
        self.data_trees = {}

    def print(self, ng):
        for link in ng.links:
            self.get(link.from_socket).print()

    def get(self, socket=None):
        ng_id = socket.id_data.name
        s_id = socket.socket_id
        if ng_id not in self.data_trees:
            self.data_trees[ng_id] = {}
        ng_trees = self.data_trees[ng_id]
        if s_id not in ng_trees:
            ng_trees[s_id] = SvDataTree(socket=socket)
        return ng_trees[s_id]

    def clean(self, ng):
        ng_id = ng.name
        self.data_trees[ng_id] = {}

data_trees = SvTreeDB()


# from itertools, should be somewhere else...

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def DAG(ng):
    links = collections.defaultdict(list)

    # needs to preprocess certain things
    # 1. reroutes
    # 2. wife node replacement

    for l in ng.links:
        if not l.is_valid:
            links = {}
            break
        links[l.to_node].append(l.from_node)

    from_nodes = {l.from_node for l in ng.links}
    start = {l.to_node for l in ng.links if l.to_node not in from_nodes}

    def recurse(node, links):
        print(node.name)
        if node in links:
            for n in links[node]:
                yield from recurse(n, links)
                yield node
        else:
            yield node

    for node in start:
        yield from recurse(node, links)


def recurse_levels(f, in_levels, out_levels, in_trees, out_trees):
    def assign_tree(tree, level, data):
        print("Assign", tree, level, data)
        if tree is None:
            return
        if level == 0:
            tree.data = data
            tree.level = 0
        elif level == 1:
            for d in data:
                tree.add_child(data=d).level = 0
            tree.level = 1
        print("Assign", tree, level, data)

    print(f.label, in_levels, out_levels, in_trees)
    if all(t.level == l for t, l in zip(in_trees, in_levels)):
        args = []
        for tree in in_trees:
            args.append(tree.data)
        results = f(*args)
        if len(out_trees) > 1:
            for out_tree, l, result in zip(out_trees, out_levels, results):
                assign_tree(out_tree, l, result)
        elif len(out_trees) == 1:  # results is a single socket
            print(results)
            assign_tree(out_trees[0], out_levels[0], results)
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
                print(tree, inner_tree)
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
#            for t0, t1 in zip(outs, out_trees):
#                if t0:
#                    t1.level = t0.level + 1



def recurse_exec(f, trees, out_trees, level=0):
    if all(tree.is_leaf for tree in trees):
        args = [tree.data for tree in trees]
        res = f(*args)
        if len(out_trees) > 1:
            for out_tree, r in zip(out_trees, res):
                if out_tree is not None:
                    out_tree.data = r
        elif len(out_trees) == 1:
            for r in res[0]:
                sdt = SvDataTree()
                sdt.data = r
                out_trees[0].children.append(sdt)
        else:  # no output
            pass
    else:
        inner_trees = [[tree] if tree.is_leaf else tree.children for tree in trees]
        for i in range(max(map(len, inner_trees))):
            index = [i if i < len(tree) else len(tree) - 1 for tree in inner_trees]
            args = [inner_trees[j][idx] for j, idx in enumerate(index)]
            for out_tree in out_trees:
                out_tree.children.append(SvDataTree())

            recurse_exec(f, args, [out_tree.children[-1] for out_tree in out_trees], level=(level + 1))


def compile_node(node):
    node_funcs = svrx.nodes.node_base._node_funcs
    func = node_funcs.get(node.bl_idname)
    if func is None:
        raise LookupError
    return func


def exec_node_group(node_group):
    print("exec tree")
    data_trees.clean(node_group)
    for node in unique_everseen(DAG(node_group), key=lambda n: n.name):
        print("exec node", node.name)
        func = compile_node(node)
        out_trees = []
        in_trees = []
        in_levels = []

        for param, level in func.parameters:
            in_levels.append(level)
            if isinstance(param, int):
                socket = node.inputs[param]
                if socket.is_linked:
                    #  here a more intelligent loookup is needed
                    #  to support reroutes and wifi replacement
                    tree = data_trees.get(socket.links[0].from_socket)
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

        recurse_levels(func, in_levels, func.returns, in_trees, out_trees)
        print("finished with node", node.name)
        for ot in out_trees:
            if ot:
                ot.set_level()
                ot.print()
