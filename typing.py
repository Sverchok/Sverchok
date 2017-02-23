import numpy as np

from bpy.props import (BoolProperty, EnumProperty,
                       FloatProperty, IntProperty,
                       StringProperty, FloatVectorProperty)


class SvRxBaseType:
    iterable = False

    def __init__(self, name=None, iterable=None):
        if name is None:
            self.default_name = type(self).__name__
            self.name = None
        else:
            self.name = name

        if iterable is not None:
            # basiclly only allow chaning to False for types
            # than can be resonable iterated
            self.iterable = iterable

    def get_settings(self):
        return {}


# Everytype must have a corresponding socket
# Types aren't actually concrete types, they are just for
# auto generating nodes based on introspection

# specal value kept

class Required:
    pass


class Anytype(SvRxBaseType):
    bl_idname = "SvRxSocketAny"


class Number(SvRxBaseType):
    bl_idname = "SvRxSocketFloat"
    iterable = True

    def __init__(self, name=None, iterable=None, min=None, max=None):
        super().__init__(name, iterable)
        self.min = min
        self.max = max

    def get_settings(self):
        settings = {}
        if self.max is not None:
            settings['default_value_high'] = self.max
        if self.min is not None:
            settings['default_value_low'] = self.min
        return settings


class Int(Number):
    @property
    def bl_idname(self):
        if self.max is not None or self.min is not None:
            return "SvRxSocketIntLimit"
        else:
            return "SvRxSocketInt"


class Bool(Int):
    pass


class Float(Number):
    @property
    def bl_idname(self):
        if self.max is not None or self.min is not None:
            return "SvRxSocketFloatLimit"
        else:
            return "SvRxSocketFloat"


class Number4f(SvRxBaseType):
    iterable = True


class Color(Number4f):
    bl_idname = "SvRxSocketColor"


class Vertices(Number4f):
    bl_idname = "SvRxSocketVertex"


class Vector(Number4f):
    bl_idname = "SvRxSocketVector"


class Point(Number4f):
    bl_idname = "SvRxSocketPoint"


class Edges(SvRxBaseType):
    bl_idname = "SvRxSocketTopo"


class Faces(SvRxBaseType):
    bl_idname = "SvRxSocketTopo"


class TopoData(Edges, Faces):
    bl_idname = "SvRxSocketTopo"


class String(SvRxBaseType):
    bl_idname = "SvRxSocketString"


class Object(SvRxBaseType):
    bl_idname = "SvRxSocketObject"
    iterable = False


class Matrix(SvRxBaseType):
    bl_idname = "SvRxSocketMatrix"
    identity = np.identity(4)
    iterable = False


class Mesh(SvRxBaseType):
    bl_idname = "SvRxSocketMesh"
    iterable = False


class BMesh(Mesh):
    bl_idname = "SvRxSocketMesh"
    iterable = False


class SMesh(Mesh):
    bl_idname = "SvRxSocketMesh"
    iterable = False


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
    bl_idname = "SvRxSocketValueInt"


class IntValue(Int):
    bl_idname = "SvRxSocketValueInt"


class FloatValue(Float):
    bl_idname = "SvRxSocketValueFloat"


class PointValue(Number4f):
    bl_idname = "SvRxSocketValuePoint"


class ColorValue(Number4f):
    bl_idname = "SvRxSocketValueColor"


class ObjectValue(Object):
    bl_idname = "SvRxSocketValueObject"


bases = [Number, Number4f, Mesh, Object, String, Matrix, Anytype, Faces, Edges]
_lookup = {}


def get_classes(cls):
    for sub_cls in cls.__subclasses__():
        yield sub_cls
        yield from get_classes(sub_cls)


for base in bases:
    _lookup[base] = base
    for class_ in get_classes(base):
        _lookup[class_] = base
