from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, Vertices, Edges, Faces

import numpy as np
from svrx.util.function import generator
from svrx.util.smesh import SvPolygon
from svrx.util.topology import torus_edges, torus_faces


def make_torus(R, r, N1, N2):
    z = np.zeros((N2, 4))
    t_r = np.linspace(0, np.pi *2 * (N2-1/N2), N2)
    z[:,2] = np.cos(t_r) *r
    scale = np.sin(t_r) *r + R
    t_R = np.linspace(0, np.pi * 2 * (N1 - 1 / N1), N1)
    circle = np.array([np.cos(t_R), np.sin(t_R), np.zeros(N1), np.ones(N1)]).T
    torus = np.empty((N2, N1, 4))
    torus[:] = z[:, np.newaxis, :] + circle
    torus[:,:,:2] *= scale[:,np.newaxis,np.newaxis]
    torus.shape = (-1, 4)
    return torus

@node_func(bl_idname="SvRxNodeGenTorus", multi_label="Torus", id=0)
@generator
def torus(
    R: Float = 2.0, r: Float = 0.6,
    N1: Int = 22, N2: Int = 15) -> ([Vertices], [Edges], [Faces]):
    return make_torus(R, r, N1, N2), torus_edges(N2, N1), torus_faces(N2, N1)
