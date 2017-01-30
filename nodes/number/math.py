from svrx.nodes.node_base import node_func

from svrx.typing import Number, Float, Int, EnumP


mode_list_tmp = [('ADD', 1), ('SUB', 2)]

mode_list = [(t, t, t, idx) for t, idx in mode_list_tmp]


@node_func(bl_idname='SvRxNodeNumberMath')
def math(x: Number = 0.0, y: Number = 0.0,
        mode: EnumP(items=mode_list, default='ADD') = 'ADD')-> Number:
    f = func_lookup[mode]
    return f(x, y)


def add(x, y):
    return x  + y

def sub(x, y):
    return x - y

func_lookup = {'ADD': add,
               'SUB': sub, }
