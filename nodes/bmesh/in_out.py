import bmesh

from svrx.typing import Float, Int, Vector, BMesh, Required, Vertices, Edges, Faces
from svrx.nodes.node_base import node_func
from svrx.util.mesh import bmesh_from_pydata, rxdata_from_bm


@node_func(bl_idname="SvRxBMeshIn")
def bmesh_in(verts: Vertices = Required,
             edges: Edges = None,
             faces: Faces = None) -> BMesh:
    return bmesh_from_pydata(vertices, edges, faces)

@node_func(bl_idname="SvRxBMeshOut")
def bmesh_out(bm: BMesh = Required) -> (Vertices, Edges, Faces):
    return rxdata_from_bm(bm)
