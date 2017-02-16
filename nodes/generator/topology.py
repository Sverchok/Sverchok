import numpy as np

from svrx.typing import Vertices, Edges, Faces, Required
from svrx.nodes.node_base import node_func
from svrx.util.smesh import SvPolygon


@node_func(bl_idname="SvRxGeneratorTopology", multi_label="Topology", id=0)
def line(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    edges = np.array([np.arange(0, count - 1), np.arange(1, count)]).T
    return verts, edges, None


@node_func(id=1)
def cirle(verts: Vertices = Required) -> (Vertices, Edges, Faces):
    count = len(verts)
    edges = np.array([np.arange(0, count), np.arange(1, count + 1) % count], dtype=np.uint32).T
    faces = SvPolygon.from_pydata([np.arange(0, count)])

    return verts, edges, faces


@node_func(id=2)
def plane(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    y = len(verts)
    x = len(verts[0])
    edges = np.array(plane_edges(x,     y), dtype=np.uint32)
    faces = SvPolygon.from_pydata(plane_faces(x, y))
    return vertices, edges, faces


@node_func(id=3)
def cylinder(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    height = len(verts)
    vert_count = len(verts[0])
    edges = cyl_edges(height, vert_count)
    faces = cyl_faces(height, vert_count, False)
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


"""

@node_func( id=4)
def torus(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    pass
"""



# helper from sverchok, should be rewritten into numpy form.


def plane_edges(x, y):
    edges = []
    for i in range(y):
        for j in range(x-1):
            edges.append((x*i+j, x*i+j+1))
    for i in range(x):
        for j in range(y-1):
            edges.append((x*j+i, x*j+i+x))
    return edges

def plane_faces(x, y):
    polygons = []
    for i in range(x-1):
        for j in range(y-1):
            polygons.append((x*j+i, x*j+i+1, x*j+i+x+1, x*j+i+x))

    return polygons


def cyl_edges(x, y):
    edges = np.empty((2*x*y-y, 2), dtype=np.uint32)
    edges[:x*y, 0] = np.arange(x * y)
    edges[:x*y, 1] = np.arange(1, x * y + 1)
    edges[range(y - 1, x * y, y), 1] -= y
    edges[x * y:, 0] = np.arange(0, x * y - y)
    edges[x * y:, 1] = np.arange(y, x * y)
    return edges

def cyl_faces(x, y, cap=False):
    """
    caps not implemented yet
    """
    p = np.empty((x*y-y, 4), dtype=np.uint32)
    skips = range(y - 1, x*y -y, y)
    p[:, 0] = np.arange(0, x * y - y)
    p[:, 1] = np.arange(1, x * y - y + 1)
    p[skips, 1] -= y
    p[:, 2] = np.arange(y + 1, x * y + 1)
    p[skips, 2] -= y
    p[:, 3] = np.arange(y, x * y)
    l_total = np.empty(x * y - y, dtype=np.uint32)
    l_total[:] = 4
    l_start = np.arange(0, (x * y - y) * 4, 4, dtype=np.uint32)
    p.shape = (x * y -y ) * 4
    return SvPolygon(l_start, l_total, p)
