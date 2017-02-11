from sverchok.nodes.generator.torus import torus_verts, torus_edges, torus_polygons

from svrx.util.geom import generator
from svrx.util.smesh import SMesh

def make_torus(R, r, N1, N2, rPhase, sPhase):
    v = torus_verts(R, r, N1, N2, rPhase, sPhase, False)[0]
    e = torus_edges(N1, N2)
    f = torus_polygons(N1, N2)
    return SMesh.from_pydata(v, e, f).as_rxdata

@node_script
@generator
def sn_torus(
    R: Float = 2.0, r: Float = 0.6, 
    N1: Int = 22, N2: Int = 15, 
    rPhase: Float = 0.0,
    sPhase: Float = 0.0) -> ([Vertices], [Edges], [Faces]):
    return make_torus(R, r, N1, N2, rPhase, sPhase)
