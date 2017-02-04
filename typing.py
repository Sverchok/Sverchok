from typing import List
import numpy as np

from bpy.props import BoolProperty, EnumProperty ,FloatProperty, IntProperty, StringProperty, FloatVectorProperty


class SvRxBaseType:
    def __init__(self, name=None):
        self.name = name


# Everytype must have a corresponding socket
# Types aren't actually concrete types yet, they are just for
# auto generating nodes based on introspection

Required = object()


class Number(SvRxBaseType):
    bl_idname = "SvRxFloatSocket"


class Int(Number):
    bl_idname = "SvRxIntSocket"

class Bool(Int):
    pass

class Float(Number):
    bl_idname = "SvRxFloatSocket"


class Vertices(Number):
    bl_idname = "SvRxVertexSocket"


class Vector(Number):
    bl_idname = "SvRxVectorSocket"

class Point(Number):
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


class Color(SvRxBaseType):
    bl_idname = "SvRxColorSocket"


class Anytype(SvRxBaseType):
    bl_idname = "SvRxAnySocket"


class Mesh(SvRxBaseType):
    bl_idname = "SvRxMeshSocket"


class BMesh(SvRxBaseType):
    bl_idname = "SvRxMeshSocket"


class SMesh(SvRxBaseType):
    bl_idname = "SvRxMeshSocket"

class Color(Number):
    bl_idname = "SvRxColorSocket"


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


class IntValue(SvRxBaseType):
    bl_idname = "SvRxValueIntSocket"


class FloatValue(SvRxBaseType):
    bl_idname = "SvRxValueFloatSocket"


class PointValue(SvRxBaseType):
    bl_idname = "SvRxValuePointSocket"


class ColorValue(SvRxBaseType):
    bl_idname = "SvRxValueColorSocket"


class ObjectValue(SvRxBaseType):
    bl_idname = "SvRxValueObjectSocket"
