import bmesh

from svrx.typing import Float, Int, Vector, BMesh
from svrx.nodes.node_base import node_func
from svrx.util.function import generator

@node_func(bl_idname='SvRxNodeBmeshGenerate', multi_label="Bmesh Gen", id=0)
def create_monkey() -> BMesh:
    bm = bmesh.new()
    bmesh.ops.create_monkey(bm)
    return bm


def make_icosphere(subdiv, diam):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, diameter=diam, calc_uvs=False)
    return bm

@node_func(id=1)
@generator
def create_icosphere(subdiv: Int(min=0, max=8) = 2, diam: Float = 1.0) -> [BMesh]:
    return make_icosphere(min(subdiv, 8), diam)


@node_func(id=2)
@generator
def create_cube(size: Float = 1.0) -> [BMesh]:
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=size)
    return bm

@node_func(id=3)
@generator
def create_uvsphere(u: Int = 10, v: Int = 10, diameter: Float = 1.0) -> [BMesh]:
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, diameter=diameter)
    return bm
