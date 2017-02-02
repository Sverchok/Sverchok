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

'''
None of this file is in a working condition. skip this file.

Eventual purpose of this file is to store the convenience functions which
can be used for regular nodes or as part of recipes for script nodes. These
functions will initially be sub optimal quick implementations, then optimized
only for speed, never for aesthetics or line count or cleverness.

'''

import math
import numpy as np
from functools import wraps

import bmesh
import mathutils

from svrx.util.smesh import SvPolygon

def match_long_repeat(parameters):
    counts = [len(p) for p in parameters]
    for i in range(max(counts)):
        args = []
        for c, parameter in zip(counts, parameters):
            args.append(parameter[min(c - 1, i)])
        yield args


def vectorize(func):
    '''
    Will create a yeilding vectorized generator of the
    function it is applied to.
    Note: arguments must be list or similar OR str, float or int
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        split = len(args)
        keys = kwargs.keys()
        parameters = [p for p in args + tuple(kwargs.values())]
        for param in match_long_repeat(parameters):
            kw_args = {k: v for k, v in zip(keys, param[split:])}
            yield func(*param[:split], **kw_args)
    return inner


def circle(radius=1.0, phase=0, nverts=20):
    t = np.linspace(0, np.pi * 2 * (nverts - 1 / nverts), nverts)
    circ = np.array([np.cos(t + phase) * radius, np.sin(t + phase) * radius, np.zeros(nverts), np.ones(nverts)])
    verts = np.transpose(circ)
    edges = np.array([(i, i + 1) for i in range(nverts - 1)] + [(nverts - 1, 0)])
    faces = SvPolygon([tuple(range(nverts))])
    return verts, edges, faces

circles = vectorize(circle)

# ---------- Spline

# spline function modifed from
# from looptools 4.5.2 done by Bart Crouch


# calculates natural cubic splines through all given knots


class CubicSpline:
    def __init__(self, locs, tknots=None, metric='DISTANCE'):
        """    locs is and np.array with shape (n,3) and tknots has shape (n-1,)
        creates a cubic spline thorugh the locations given in locs

        """
        n = len(locs)
        if n < 2:
            return False

        if tknots is None:
            tknots = create_knots(locs, metric)

        self.tknots = tknots

        h = tknots[1:] - tknots[:-1]
        h[h == 0] = 1e-8
        q = np.zeros((n - 1, 3))
        q[1:] = 3 / h[1:, np.newaxis] * (locs[2:] - locs[1:-1]) - 3 / \
            h[:-1, np.newaxis] * (locs[1:-1] - locs[:-2])

        l = np.zeros((n, 3))
        l[0, :] = 1.0
        u = np.zeros((n - 1, 3))
        z = np.zeros((n, 3))

        for i in range(1, n - 1):
            l[i] = 2 * (tknots[i + 1] - tknots[i - 1]) - h[i - 1] * u[i - 1]
            l[i, l[i] == 0] = 1e-8
            u[i] = h[i] / l[i]
            z[i] = (q[i] - h[i - 1] * z[i - 1]) / l[i]
        l[-1, :] = 1.0
        z[-1] = 0.0

        b = np.zeros((n - 1, 3))
        c = np.zeros((n, 3))

        for i in range(n - 2, -1, -1):
            c[i] = z[i] - u[i] * c[i + 1]
        b = (locs[1:] - locs[:-1]) / h[:, np.newaxis] - h[:, np.newaxis] * (c[1:] + 2 * c[:-1]) / 3
        d = (c[1:] - c[:-1]) / (3 * h[:, np.newaxis])

        splines = np.zeros((n - 1, 5, 3))
        splines[:, 0] = locs[:-1]
        splines[:, 1] = b
        splines[:, 2] = c[:-1]
        splines[:, 3] = d
        splines[:, 4] = tknots[:-1, np.newaxis]

        self.splines = splines

    def eval(self, t_in):
        """
        Evaluate the spline at the points in t_in, which must be an array
        with values in [0,1]
        returns and np array with the corresponding points
        """
        splines = self.splines
        tknots = self.tknots
        index = tknots.searchsorted(t_in, side='left') - 1
        index = index.clip(0, len(splines) - 1)
        to_calc = splines[index]
        ax, bx, cx, dx, tx = np.swapaxes(to_calc, 0, 1)
        t_r = t_in[:, np.newaxis] - tx
        out = ax + t_r * (bx + t_r * (cx + t_r * dx))
        return out


    def tangent(self, t_in, h=0.001):
        """
        Calc numerical tangents for spline at t_in
        """
        t_ph = t_in + h
        t_mh = t_in - h
        t_less_than_0 = t_mh < 0.0
        t_great_than_1 = t_ph > 1.0
        t_mh[t_less_than_0] += h
        t_ph[t_great_than_1] -= h
        tanget_ph = self.eval(t_ph)
        tanget_mh = self.eval(t_mh)
        tanget = tanget_ph - tanget_mh
        tanget[t_less_than_0 | t_great_than_1] *= 2
        return tanget


def create_knots(pts, metric="DISTANCE"):
    if metric == "DISTANCE":
        tmp = np.linalg.norm(pts[:-1] - pts[1:], axis=1)
        tknots = np.insert(tmp, 0, 0).cumsum()
        tknots = tknots / tknots[-1]
    elif metric == "MANHATTAN":
        tmp = np.sum(np.absolute(pts[:-1] - pts[1:]), 1)
        tknots = np.insert(tmp, 0, 0).cumsum()
        tknots = tknots / tknots[-1]
    elif metric == "POINTS":
        tknots = np.linspace(0, 1, len(pts))
    elif metric == "CHEBYSHEV":
        tknots = np.max(np.absolute(pts[1:] - pts[:-1]), 1)
        tmp = np.insert(tmp, 0, 0).cumsum()
        tknots = tknots / tknots[-1]

    return tknots


class LinearSpline:
    def __init__(self, pts, tknots=None, metric='DISTANCE'):
        self.pts = np.array(pts).T
        if tknots is None:
            tknots = create_knots(locs, metric)

        self.tknots = tknots

    def eval(self, t_in):
        """
        Eval the liner spline f(t) = x,y,z through the points
        in pts given the knots in tknots at the point in t_in
        """
        ptsT = self.pts
        tknots = self.tknots
        out = np.empty((3, len(t_in)))
        for i in range(3):
            out[i] = np.interp(t_in, tknots, ptsT[i])
        return out.T
