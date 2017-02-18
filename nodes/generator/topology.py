import numpy as np

from svrx.typing import Vertices, Edges, Faces, Required
from svrx.nodes.node_base import node_func
from svrx.util.smesh import SvPolygon
from svrx.util.topology import plane_edges, plane_faces, cylinder_edges, cylinder_faces, torus_edges, torus_faces

@node_func(bl_idname="SvRxGeneratorTopology", multi_label="Topology", id=0)
def line(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    edges = np.array([np.arange(0, count - 1), np.arange(1, count)]).T
    return verts, edges, None


@node_func(id=1)
def cirle(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    edges = np.array([np.arange(0, count), np.arange(1, count + 1) % count], dtype=np.uint32).T
    faces = SvPolygon(np.array([0], dtype=np.uint32),
                      np.array([nverts], dtype=np.uint32),
                      np.arange(0, nverts, dtype=np.uint32))
    return verts, edges, faces


@node_func(id=2)
def plane(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    y = len(verts)
    x = len(verts[0])
    edges = plane_edges(x, y)
    faces = plane_faces(x, y)
    return vertices, edges, faces


@node_func(id=3)
def cylinder(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    height = len(verts)
    vert_count = len(verts[0])
    edges = cylinder_edges(height, vert_count)
    faces = cylinder_faces(height, vert_count, False)
    return vertices, edges, faces


@node_func(id=4)
def line_connect(verts : [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    count = len(verts[0])
    obj_count = len(verts)
    e_start = np.arange(0, obj_count * count - count)
    e_stop = np.arange(count, obj_count * count)
    edges = np.array((e_start, e_stop)).T
    return vertices, edges, None


@node_func( id=5)
def torus(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    height = len(verts)
    vert_count = len(verts[0])
    edges = torus_edges(height, vert_count)
    faces = torus_faces(height, vert_count, False)
    return vertices, edges, faces


# helper from sverchok, should be rewritten into numpy form.
