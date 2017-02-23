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

#
# This file contains helper functions for @node_func functions
# Mostly dealing with np array shapes and function behaviour
#
# The most important one is @geenrator


from functools import wraps
import inspect
import itertools

import numpy as np


def generator(func=None, match=None, limit=None):
    '''
    Will create a yeilding vectorized generator of the
    function it is applied to.
    '''
    def wrapper(func):
        sig = inspect.signature(func)
        func.mask = []
        for name, parameter in sig.parameters.items():
            m = getattr(parameter.annotation, "iterable", False)
            func.mask.append(not m)

        @wraps(func)
        def inner(*args, match=match):
            if match is None:
                match = match_long_repeat
            mask = func.mask
            if mask is None:
                parameters = [np.atleast_1d(arg) for arg in args]
            else:
                parameters = [arg if m else np.atleast_1d(arg) for arg, m in zip(args, mask)]
            out = []
            for param in match(*parameters, limit=limit, mask=mask):
                out.append(func(*param))
            return out
        return inner
    if func:
        return wrapper(func)
    else:
        return wrapper


def match_long_repeat(*parameters, limit=None, mask=None):
    if mask is None:
        counts = [len(p) for p in parameters]
    else:
        counts = [1 if m else len(p) for m, p in zip(mask, parameters)]
    if limit is not None:
        max_len = counts[limit]
    else:
        max_len = max(counts)
    if mask is None:
        for i in range(max_len):
            args = []
            for c, parameter in zip(counts, parameters):
                args.append(parameter[min(c - 1, i)])
            yield args
    else:
        for i in range(max_len):
            args = []
            for c, m, parameter in zip(counts, mask, parameters):
                if m:
                    args.append(parameter)
                else:
                    args.append(parameter[min(c - 1, i)])
            yield args


def match_long_cycle(*parameters, limit=None, mask=None):
    counts = [len(p) for p in parameters]
    if limit is not None:
        max_len = counts[limit]
    else:
        max_len = max(counts)
    args = []
    for c, p in zip(counts, parameters):
        if c < max_len:
            args.append(itertools.cycle(p))
        else:
            args.append(p)
    yield from zip(*args)


def match_short(*parameters, limit=None, mask=None):
    yield from zip(*parameters)


def constant(func):
    """wrap a function func so it can return a single number/value
    that is wrapped into an array.
    """
    @wraps(func)
    def inner(*args):
        return np.atleast_1d(func(*args))
    return inner


def std_wrap(func):
    """wrap a function func so it can return a single number/value
    that is wrapped into an array.
    """
    @wraps(func)
    def inner(*args):
        return np.atleast_1d(func(*args))
    return inner


def compat(func):
    @wraps(func)
    def inner(a, b):
        return func(*make_compatible(a, b))
    return inner


def make_compatible(a, b, broadcast=True):
    if broadcast and is_broadcastable(a, b):
        return a, b
    shape = tuple(max(x, y) for x, y in zip(a.shape, b.shape))
    return array_as(a, shape), array_as(b, shape)


def array_as(a, shape):
    if a.shape == shape:
        return a
    new_a = np.empty(shape, dtype=a.dtype)
    new_a[:len(a)] = a
    new_a[len(a):] = a[-1]
    return new_a


def array_as_cycle(a, shape):
    if a.shape == shape:
        return a
    new_a = np.empty(shape, dtype=a.dtype)
    for i in range(shape[0]):
        new_a[i] = a[i % len(a)]
    return new_a


def is_broadcastable(a, b):
    return all((x == 1 or y == 1 or x == y) for x, y in zip(a.shape[::-1], b.shape[::-1]))
