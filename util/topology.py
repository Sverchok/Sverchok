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
import numpy as np
from svrx.util.smesh import SvPolygon


def plane_edges(x, y):
    edges = np.empty((x * (y - 1) + (x - 1) * y, 2 ), dtype=np.uint32)
    u_dir = np.arange(0, x - 1) + np.arange(0, x * y, x)[:,np.newaxis]
    v_dir = np.arange(0, x * (y - 1), x) + np.arange(0, x)[:,np.newaxis]
    u_dir.shape = -1
    v_dir.shape = -1
    split = v_dir.shape[0]
    edges[split:, 0] = u_dir
    edges[:split, 0] = v_dir
    edges[split:, 1] = u_dir + 1
    edges[:split, 1] = v_dir + x
    return edges

def plane_faces(x, y):
    faces = np.empty(((x - 1) * (y - 1), 4), dtype=np.uint32)
    faces[:, 3] = (np.arange(y, x * y, y) + np.arange(0 , y - 1)[:,np.newaxis]).flatten()
    faces[:, 2] = faces[:, 3] + 1
    faces[:, 0] = (np.arange(0, x * y -y, y) + np.arange(0, y - 1)[:,np.newaxis]).flatten()
    faces[:, 1] = faces[:, 0] + 1
    faces.shape = -1
    l_total = np.empty((x - 1) * (y - 1), dtype=np.uint32)
    l_total[:] = 4
    l_start = np.arange(0, (x - 1) * (y - 1) * 4, 4, dtype=np.uint32)
    return SvPolygon(l_start, l_total, faces)


def cylinder_edges(x, y):
    edges = np.empty((2*x*y-y, 2), dtype=np.uint32)
    edges[:x*y, 0] = np.arange(x * y)
    edges[:x*y, 1] = np.arange(1, x * y + 1)
    edges[range(y - 1, x * y, y), 1] -= y
    edges[x * y:, 0] = np.arange(0, x * y - y)
    edges[x * y:, 1] = np.arange(y, x * y)
    return edges


def cylinder_faces(x, y, caps=False):
    if caps:
        out = np.empty((x * y - y) * 4 + 2 * y, dtype=np.uint32)
        out[:y] = np.arange(0, y)[::-1]
        out[y: 2*y] = np.arange(y * (x - 1), y * x)
        p = out[2 * y:]
        p.shape = (-1, 4)
    else:
        p = np.empty((x*y-y, 4), dtype=np.uint32)
    skips = range(y - 1, x*y -y, y)
    p[:, 0] = np.arange(0, x * y - y)
    p[:, 1] = np.arange(1, x * y - y + 1)
    p[skips, 1] -= y
    p[:, 2] = np.arange(y + 1, x * y + 1)
    p[skips, 2] -= y
    p[:, 3] = np.arange(y, x * y)
    if caps:
        l_total = np.empty(x * y - y + 2, dtype=np.uint32)
        l_start = np.empty(x * y - y + 2, dtype=np.uint32)
        l_total[:2] = y
        l_total[2:] = 4
        l_start[:1] = 0
        l_start[1:] = l_total[:-1].cumsum()
        out.shape = -1
        return SvPolygon(l_start, l_total, out)
    else:
        l_total = np.empty(x * y - y, dtype=np.uint32)
        l_total[:] = 4
        l_start = np.arange(0, (x * y - y) * 4, 4, dtype=np.uint32)
        p.shape = (x * y -y ) * 4
        return SvPolygon(l_start, l_total, p)





def torus_edges(x, y):
    edges = np.empty((2*x*y, 2), dtype=np.uint32)
    edges[:x*y, 0] = np.arange(x * y)
    edges[:x*y, 1] = np.arange(1, x * y + 1)
    edges[range(y - 1, x * y, y), 1] -= y
    edges[x * y:, 0] = np.arange(0, x * y)
    edges[x * y:, 1] = np.roll(np.arange(0, x * y), -y)
    return edges

def torus_faces(x, y):
    faces = np.empty((x * y, 4), dtype=np.uint32)
    tmp = np.arange(0, x * y)
    faces[:, 0] = tmp
    faces[:, 1] = np.roll(tmp, -y)
    tmp += 1
    tmp.shape = (x, y)
    tmp[:, y - 1] -= y
    tmp.shape = -1
    faces[:, 3] = tmp
    faces[:, 2] = np.roll(tmp, -y)
    faces.shape = -1
    l_total = np.empty(x * y, dtype=np.uint32)
    l_total[:] = 4
    l_start = np.arange(0, (x * y) * 4, 4, dtype=np.uint32)
    return SvPolygon(l_start, l_total, faces)
