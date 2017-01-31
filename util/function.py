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
