import numpy as np

from svrx.typing import Vertices, Edges, Faces, Required
from svrx.nodes.node_base import node_func


@node_func(bl_idname="SvRxGeneratorTopology", multi_label="Topology", id=0)
def line(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    edges = np.array([np.arange(0, count - 1), np.arange(1, count)]).T
    return verts, edges, None

"""
@node_func(bl_idname="SvRxGeneratorTopology", id=1)
def cirle(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    return np.array([np.arange(0, count), np.arange(1, count + 1) % count])


@node_func(bl_idname="SvRxGeneratorTopology", id=2)
def plane(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    pass


@node_func(bl_idname="SvRxGeneratorTopology", id=3)
def cylinder(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    pass


@node_func(bl_idname="SvRxGeneratorTopology", id=4)
def torus(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    pass
"""
