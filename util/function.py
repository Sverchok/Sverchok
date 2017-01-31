from functools import wraps

import numpy as np


def constant(func):
    """wrap a function func so it can return a single number/value
    that is wrapped into an array.
    """
    @wraps(func)
    def inner():
        return np.array([func()])
    return inner


def draw_label(self):
    """
    draws label for mutli mode nodes like math, logic and trigonometey
    """
    if not self.hide:
        return self.label or self.name

    name_or_value = [self.mode.title()]
    for socket in self.inputs:
        if socket.is_linked:
            name_or_value.append(socket.name.title())
        else:
            name_or_value.append(str(socket.default_value))
    return ' '.join(name_or_value)


def compat(func):
    @wraps(func)
    def inner(a, b):
        return func(*make_compatible(a, b))
    return inner

def make_compatible(a, b):
    if is_broadcastable(a, b):
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
