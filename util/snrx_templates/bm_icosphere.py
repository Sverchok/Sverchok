import bmesh
from svrx.util.geom import generator
from svrx.util.mesh import rxdata_from_bm

def make_icosphere(subdiv, diam):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, diameter=diam, calc_uvs=False)
    return rxdata_from_bm(bm)

@node_script
@generator
def sn_icosphere(subdiv: Int(min=0, max=5) = 2, diam: Float = 1.0) -> ([Vertices], [Edges], [Faces]):
    return make_icosphere(min(subdiv, 5), diam)
