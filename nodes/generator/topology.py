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
    print(edges)
    faces = SvPolygon.from_pydata([np.arange(0, count)])

    return verts, edges, faces


@node_func(bl_idname="SvRxGeneratorTopology", id=2)
def plane(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    y = len(verts)
    x = len(verts[0])
    edges = np.array(plane_edges(x, y), dtype=np.uint32)
    faces = SvPolygon.from_pydata(plane_faces(x, y))
    return vertices, edges, faces


@node_func(bl_idname="SvRxGeneratorTopology", id=3)
def cylinder(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    height = len(verts)
    vert_count = len(verts[0])
    edges = np.array(cylinder_edges(height -2, vert_count), dtype=np.uint32)
    faces = SvPolygon.from_pydata(cylinder_faces(height -2, vert_count, False))
    return vertices, edges, faces

"""

@node_func(bl_idname="SvRxGeneratorTopology", id=4)
def torus(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    pass
"""



# helper from sverchok, should be rewritten into numpy form.


def plane_edges(x, y):
    edges = []
    for i in range(y):
        for j in range(x-1):
            edges.append((x*i+j, x*i+j+1))
    return edges

def plane_faces(x, y):
    polygons = []
    for i in range(x-1):
        for j in range(y-1):
            polygons.append((x*j+i, x*j+i+1, x*j+i+x+1, x*j+i+x))
    return polygons


def cylinder_edges(Subd, Vertices):
    listEdg = []
    for i in range(Subd+2):
        for j in range(Vertices-1):
            listEdg.append([j+Vertices*i, j+1+Vertices*i])
        listEdg.append([Vertices-1+Vertices*i, 0+Vertices*i])
    for i in range(Subd+1):
        for j in range(Vertices):
            listEdg.append([j+Vertices*i, j+Vertices+Vertices*i])

    return listEdg


def cylinder_faces(Subd, Vertices, Cap):
    listPlg = []
    for i in range(Subd+1):
        for j in range(Vertices-1):
            listPlg.append([j+Vertices*i, j+1+Vertices*i, j+1+Vertices*i+Vertices, j+Vertices*i+Vertices])
        listPlg.append([Vertices-1+Vertices*i, 0+Vertices*i, 0+Vertices*i+Vertices, Vertices-1+Vertices*i+Vertices])
    if Cap:
        capBot = []
        capTop = []
        for i in range(Vertices):
            capBot.append(i)
            capTop.append(Vertices*(Subd+1)+i)
        capBot.reverse()
        listPlg.append(capBot)
        listPlg.append(capTop)
    return listPlg
