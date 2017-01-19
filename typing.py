from typing import List
from bpy.props import FloatProperty, IntProperty, StringProperty, FloatVectorProperty

class SvBaseType:
    pass

# Everytype must have a corresponding socket
# Types aren't actually concrete types yet, they are just for
# auto generating nodes based on introspection


class Number(SvBaseType):
    bl_idname = "SvRxFloatSocket"


class Int(Number):
    bl_idname = "SvRxIntSocket"


class Float(Number):
    bl_idname = "SvRxFloatSocket"


class Vertices(Number):
    bl_idname = "SvRxVertexSocket"


class Vector(Number):
    bl_idname = "SvRxVertexSocket"


class Edges(SvBaseType):
    bl_idname = "SvRxTopoSocket"


class Faces(SvBaseType):
    bl_idname = "SvRxTopoSocket"


class TopoData(Edges, Faces):
    bl_idname = "SvRxTopoSocket"


class String(SvBaseType):
    bl_idname = "SvRxStringSocket"


class Object(SvBaseType):
    bl_idname = "SvRxObjectSocket"


# Property types
class SvBaseTypeP:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def add(self, key, value):
        self.kwargs[key] = value

    def get_prop(self):
        return self.prop_func(**self.kwargs)


class FloatP(SvBaseTypeP):
    prop_func = FloatProperty


class IntP(SvBaseTypeP):
    prop_func = IntProperty


class VectorP(SvBaseTypeP):
    prop_func = FloatVectorProperty


class StringP(SvBaseTypeP):
    prop_func = StringProperty


# Value Types, used for outputs

class ValueBase:
    pass


class IntValue:
    pass


class FloatValue:
    pass
