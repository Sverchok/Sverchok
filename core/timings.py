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
import bgl

from svrx.util import bgl_callback


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

def show_timings(ng):
    if ng.do_timings_text:
        show_timings_text(ng)

    if ng.do_timings_graphics:
        show_timings_graphics(ng)


def show_timings_graphics(ng):
    bgl_callback.callback_disable("timings:" + ng.name)
    t_iter = iter(timings)
    ng_name, base_time = next(t_iter)
    _, dag_start = next(t_iter)
    _, dag_stop = next(t_iter)
    name, t = next(t_iter)
    nodes = []
    res = collections.defaultdict(list)
    current_node = ''
    while name != ng_name:
        if name.startswith("SvRx") and current_node != name:
            current_node = name
            node_start = t
        elif name == current_node:
            current_node = ''
            nodes.append((name, node_start, t))
        else:
            res[current_node].append((name, t))
        name, t  = next(t_iter)
    stop_time = t

    node_boxes = []
    func_boxes = []
    for node, start, stop in nodes:
        y = len(res[node]) * 5
        x = (stop - start) * 10000
        node_boxes.append((node, x, y, (start - base_time) * 10000))
        func_data = res[node]
        for i in range(0, len(func_data), 2):
            func, start = func_data[i]
            _, stop = func_data[i + 1]
            y_f = 6
            x_f = (stop - start) * 10000
            func_boxes.append((func, x_f, y_f, (start - base_time) * 10000))

    base_point = (max(n.location.x for n in ng.nodes) + 200, max(n.location.y for n in ng.nodes))
    draw_data = {
        'tree_name': ng.name,
        'custom_function': water_fall,
        'loc': base_point,
        'args': (node_boxes, func_boxes)

    }
    bgl_callback.callback_enable("timings:" + ng.name, draw_data)


def water_fall(x, y, args):

    if len(args) == 2:
        node_boxes, func_boxes = args
    else:
        return

    def draw_rect(x=0, y=0, w=30, h=10):

        bgl.glBegin(bgl.GL_POLYGON)

        for coord in [(x, y), (x+w, y), (w+x, y-h), (x, y-h)]:
            bgl.glVertex2f(*coord)
        bgl.glEnd()

    node, n_x, n_y, x_offset = node_boxes[-1]
    x_max = n_x + x_offset
    y_offset = 0
    for node, n_x, n_y, x_offset in node_boxes:
        y_offset -= n_y
    y_max = -y_offset
    bgl.glColor4f(0.7, .7, .7, 1.0)

    draw_rect(x, y, x_max , y_max)

    y_offset = 0
    bgl.glColor4f(0.1, .7, .3, 1.0)

    for node, n_x, n_y, x_offset in node_boxes:
        draw_rect(x + x_offset, y + y_offset,  max(n_x, 1.0), n_y)
        y_offset -= n_y
    y_offset = 0
    bgl.glColor4f(0.9, .1, .1, 1.0)
    for node, n_x, n_y, x_offset in func_boxes:
        draw_rect(x + x_offset, y + y_offset - 2, max(n_x, 1.0), n_y)
        y_offset -= (n_y + 4)


def show_timings_text(ng):
    text = bpy.data.texts.get("SVRX_Timings_{}".format(ng.name))
    if not text:
        text = bpy.data.texts.new("SVRX_Timings_{}".format(ng.name))

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
    print("Total exec time: ", ng_name, "{0:.6f}".format(ng_stop-ng_start), file=output)
    print("DAG build time: ",  "{0:.6f}".format(stop - start), '{:.1%}'.format((stop-start)/total), file=output)
    sum_node_calls = 0.0
    print("Nodes:", file=output)
    for key in nodes[::2]:
        ts = res[key]
        if key.startswith("SvRx"):
            t = sum(ts[1::2]) - sum(ts[0::2])
            sum_node_calls +=  t
            names = [(key, 40), ("{0:.6f}".format(t),12), ('{:.1%}'.format(t/total), 12 )]
            for n, c in names:
                f = "{0: <{1}}"
                output.write(f.format(n, c))
            print('',file=output)
    print("Node call time total: ", "{0:.6f}".format(sum_node_calls), '{:.1%}'.format(sum_node_calls/total), file=output)
    sum_func_calls = 0.0
    print("Functions:", file=output)
    for key, ts in sorted(res.items(), key=lambda x: x[0]):
        if not key.startswith("SvRx"):
            t = sum(ts[1::2]) - sum(ts[0::2])
            sum_func_calls += t
            names = [(key, 30), (len(ts)//2, 10), ( "{0:.6f}".format(t), 12), ('{:.1%}'.format(t/total), 12 )]
            for n, c in names:
                f = "{0: <{1}}"
                output.write(f.format(n, c))
            print('',file=output)

    print("Functon call total time",  "{0:.6f}".format(sum_node_calls), '{:.1%}'.format(sum_func_calls/total), file=output)
    text.from_string(output.getvalue())
