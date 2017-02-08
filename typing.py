import numpy as np

from bpy.props import BoolProperty, EnumProperty ,FloatProperty, IntProperty, StringProperty, FloatVectorProperty


class SvRxBaseType:
    def __init__(self, name=None):
        if name is None:
            self.name = type(self).__name__
        else:
            self.name = name

    def get_settings(self):
        return {}


# Everytype must have a corresponding socket
# Types aren't actually concrete types, they are just for
# auto generating nodes based on introspection

Required = object()


class Anytype(SvRxBaseType):
    bl_idname = "SvRxAnySocket"


class Number(SvRxBaseType):
    bl_idname = "SvRxFloatSocket"


class Int(Number):
    @property
    def bl_idname(self):
        if self.max is not None or self.min is not None:
            return "SvRxIntLimitSocket"
        else:
            return "SvRxIntSocket"

    def __init__(self, name=None, min=None, max=None):
        super().__init__(name)
        self.min = min
        self.max = max

    def get_settings(self):
        settings = {}
        if self.max is not None:
            settings['default_value_high'] = self.max
        if self.min is not None:
            settings['default_value_low'] = self.min
        return settings


class Bool(Int):
    pass

class Float(Number):
    @property
    def bl_idname(self):
        if self.max is not None or self.min is not None:
            return "SvRxFloatLimitSocket"
        else:
            return "SvRxFloatSocket"

    def __init__(self, name=None, min=None, max=None):
        super().__init__(name)
        self.min = min
        self.max = max

class Number4f(SvRxBaseType):
    pass

class Color(Number4f):
    bl_idname = "SvRxColorSocket"

class Vertices(Number4f):
    bl_idname = "SvRxVertexSocket"

class Vector(Number4f):
    bl_idname = "SvRxVectorSocket"

class Point(Number4f):
    bl_idname = "SvRxPointSocket"



class Edges(SvRxBaseType):
    bl_idname = "SvRxTopoSocket"


class Faces(SvRxBaseType):
    bl_idname = "SvRxTopoSocket"


class TopoData(Edges, Faces):
    bl_idname = "SvRxTopoSocket"


class String(SvRxBaseType):
    bl_idname = "SvRxStringSocket"


class Object(SvRxBaseType):
    bl_idname = "SvRxObjectSocket"


class Matrix(SvRxBaseType):
    bl_idname = "SvRxMatrixSocket"
    identity = np.identity(4)



class Mesh(SvRxBaseType):
    bl_idname = "SvRxMeshSocket"


class BMesh(Mesh):
    bl_idname = "SvRxMeshSocket"


class SMesh(Mesh):
    bl_idname = "SvRxMeshSocket"




# Property types

def exec_node(self, context):
    self.id_data.update()


class SvRxBaseTypeP:
    def __init__(self, **kwargs):
        self.kwargs = {}
        self.kwargs['update'] = exec_node
        self.kwargs.update(kwargs)


    def add(self, key, value):
        self.kwargs[key] = value

    def get_prop(self):
        return self.prop_func(**self.kwargs)


class FloatP(SvRxBaseTypeP):
    prop_func = FloatProperty


class IntP(SvRxBaseTypeP):
    prop_func = IntProperty


class VectorP(SvRxBaseTypeP):
    prop_func = FloatVectorProperty


class StringP(SvRxBaseTypeP):
    prop_func = StringProperty


class EnumP(SvRxBaseTypeP):
    prop_func = EnumProperty


class BoolP(SvRxBaseTypeP):
    prop_func = BoolProperty


# Value Types, used for outputs

class ValueBase:
    bl_idname = "SvRxValueIntSocket"


class IntValue(Int):
    bl_idname = "SvRxValueIntSocket"


class FloatValue(Float):
    bl_idname = "SvRxValueFloatSocket"


class PointValue(Number4f):
    bl_idname = "SvRxValuePointSocket"


class ColorValue(Number4f):
    bl_idname = "SvRxValueColorSocket"


class ObjectValue(Object):
    bl_idname = "SvRxValueObjectSocket"



bases = [Number, Number4f, Mesh, Object, String, Matrix, Anytype]
_lookup = {}

def get_classes(cls):
    for sub_cls in cls.__subclasses__():
        yield sub_cls
        yield from get_classes(sub_cls)

for base in bases:
    _lookup[base] = base
    for class_ in get_classes(base):
        _lookup[class_] = base
