import bmesh

from svrx.typing import Float, Int, Vector, BMesh, Required
from svrx.nodes.node_base import node_func
from svrx.util.function import generator


@node_func(bl_idname='SvRxNodeBmeshModifiers', multi_label='Bmesh modifiers', id=0)
@generator
def wireframe(bm: BMesh = Required, t: Float = 0.01) -> [BMesh]:
    bm = bm.copy()
    bmesh.ops.wireframe(
        bm, faces=bm.faces[:],
        thickness=t,
        offset=True,
        use_replace=True,
        use_boundary=True,
        use_even_offset=True,
        use_relative_offset=True)
    return bm


@node_func(id=1)
@generator
def solidify(bm: BMesh = Required, thickness: Float = 1.0) -> [BMesh]:
    bm = bm.copy()
    geom_in = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.solidify(bm, geom=geom_in, thickness=thickness)
    return bm


@node_func(id=2)
def recalc_normals(bm: BMesh = Required) -> BMesh:
    bm = bm.copy()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


@node_func(id=3)
def update_normals(bm: BMesh = Required) -> BMesh:
    bm = bm.copy()
    bm.normal_update()
    return bm
