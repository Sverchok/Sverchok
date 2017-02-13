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
import time

import io

import bpy

timings = []

def get_time():
    return time.perf_counter()

def add_time(name):
    if timings is not None:
        timings.append((name, get_time()))

def start_timing():
    if timings is not None:
        timings.clear()

def time_func(func):
    def inner(*args):
        add_time(func.label)
        res = func(*args)
        add_time(func.label)
        return res
    return inner

def show_timings():

    text = bpy.data.texts.get("SVRX_Timings")
    if not text:
        text = bpy.data.texts.new("SVRX_Timings")

    t_iter = iter(timings)
    output = io.StringIO()
    ng_name, ng_start = next(t_iter)
    _, start = next(t_iter)
    _, stop = next(t_iter)

    res = collections.defaultdict(list)
    nodes = []
    while t_iter:
        name, t = next(t_iter)
        if name.startswith("SvRx"):
            nodes.append(name)
        if name == ng_name:
            ng_stop = t
            break
        res[name].append(t)

    total = ng_stop - ng_start
    print("Total exec time: ", ng_name, '%.3e' % (ng_stop-ng_start), file=output)
    print("DAG build time: ", '%.3e' % (stop - start), '{:.1%}'.format((stop-start)/total), file=output)
    sum_node_calls = 0.0
    print("Nodes:", file=output)
    for key in nodes[::2]:
        ts = res[key]
        if key.startswith("SvRx"):
            t = sum(ts[1::2]) - sum(ts[0::2])
            sum_node_calls +=  t
            names = [(key, 40), ('%.3e' % t,12), ('{:.1%}'.format(t/total), 12 )]
            for n, c in names:
                f = "{0: <"+ str(c) + "}"
                output.write(f.format(n[:c-1]))
            print('',file=output)
    print("Node call time total: " '%.3e' % sum_node_calls, '{:.1%}'.format(sum_node_calls/total), file=output)
    sum_func_calls = 0.0
    print("Functions:", file=output)
    for key, ts in sorted(res.items(), key=lambda x: x[0]):
        if not key.startswith("SvRx"):
            t = sum(ts[1::2]) - sum(ts[0::2])
            sum_func_calls += t
            names = [(key, 30), (len(ts)//2, 8), ('%.3e' % t,12), ('{:.1%}'.format(t/total), 12 )]
            for n, c in names:
                f = "{0: <"+ str(c) + "}"
                output.write(f.format(n))
            print('',file=output)


    print("Functon call total time", '%.3e' % sum_func_calls, '{:.1%}'.format(sum_func_calls/total), file=output)
    text.from_string(output.getvalue())
