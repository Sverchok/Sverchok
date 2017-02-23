import bmesh

from svrx.typing import Float, Int, Vector, BMesh, Required, Vertices, Edges, Faces
from svrx.nodes.node_base import node_func
from svrx.util.mesh import bmesh_from_pydata, rxdata_from_bm


@node_func(bl_idname="SvRxNodeBMeshIn")
def bmesh_in(verts: Vertices = Required,
             edges: Edges = None,
             faces: Faces = None) -> BMesh:
    return bmesh_from_pydata(verts[:,:3].tolist(), edges, faces)

@node_func(bl_idname="SvRxNodeBMeshOut")
def bmesh_out(bm: BMesh = Required) -> (Vertices, Edges, Faces):
    return rxdata_from_bm(bm)
