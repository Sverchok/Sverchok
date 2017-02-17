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
    faces = SvPolygon(np.array([0], dtype=np.uint32),
                      np.array([nverts], dtype=np.uint32),
                      np.arange(0, nverts, dtype=np.uint32))
    return verts, edges, faces


@node_func(id=2)
def plane(verts: [Vertices] = Required) -> (Vertices, Edges, Faces):
    vertices = np.concatenate(verts)
    y = len(verts)
    x = len(verts[0])
    edges = pln_edges(x, y)
    faces = pln_faces(x, y)
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

def pln_edges(x, y):
    edges = np.empty((x * (y - 1) + (x - 1) * y, 2 ), dtype=uint32)
    edges[:(x - 1) * y:, 0] = (np.arange(0, x-1) + np.arange(0, x * y - y, x)[:, np.newaxis]).flatten()
    edges[(x - 1) * y: 0] = (np.arange(0, x*(y-1), x) + np.arange(0, x)[:,np.newaxis]).flatten()
    edges[:(x - 1) * y:, 1] = edges[:(x - 1) * y:, 0] + 1
    edges[(x - 1) * y: 1] = edges[(x - 1) * y: 0] + x
    return edges

def pln_faces(x, y):
    faces = np.empty(((x - 1) * (y - 1), 4), dtype=np.uint32)
    faces[:, 3] = (np.arange(y, x * y, y) + np.arange(0 , y - 1)[:,np.newaxis]).flatten()
    faces[:, 2] = faces[:, 3] + 1
    faces[:, 0] = (np.arange(0, x * y -y, y) + np.arange(0, y - 1)[:,np.newaxis]).flatten()
    faces[:, 1] = faces[:, 0] + 1
    faces.shape = -1
    l_total = np.empty((x - 1) * (y - 1), dtype=np.uint32)
    l_total[:] = 4
    l_start = np.arange(0, (x - 1) * (y - 1) * 4, 4, dtype=np.uint32)
    return SvPolygon(l_start, l_total, faces)


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




def torus_edges(N1, N2):
    '''

        N1 : major sections - number of revolution sections around the torus center
        N2 : minor sections - number of spin sections around the torus tube

    '''
    listEdges = []

    # spin loop EDGES : around the torus tube

    for n1 in range(N1):
        for n2 in range(N2-1):
            listEdges.append([N2*n1 + n2, N2*n1 + n2+1])
        listEdges.append([N2*n1 + N2-1, N2*n1 + 0])

    # revolution loop EDGES : around the torus center

    for n1 in range(N1-1):
        for n2 in range(N2):
            listEdges.append([N2*n1 + n2, N2*(n1+1) + n2])
    for n2 in range(N2):
        listEdges.append([N2*(N1-1) + n2, N2*0 + n2])

    return listEdges


def torus_faces(x, y):
    faces = np.empty((x * y, 4), dtype=np.uint32)
    tmp = np.arange(0, x * y)
    faces[:, 0] = tmp
    faces[:, 1] = np.roll(tmp, -y)
    tmp += 1
    tmp.shape = (x, y)
    tmp[:, y - 1] -= y
    tmp.shape = -1
    faces[:, 3] = tmp
    faces[:, 2] = np.roll(tmp, -y)
    faces.shape = -1
    l_total = np.empty(x * y, dtype=np.uint32)
    l_total[:] = 4
    l_start = np.arange(0, (x * y) * 4, 4, dtype=np.uint32)
    return SvPolygon(l_start, l_total, faces)



def torus_polygons(N1, N2):
    '''
        N1 : major sections - number of revolution sections around the torus center
        N2 : minor sections - number of spin sections around the torus tube

    '''
    listPolys = []
    for n1 in range(N1-1):
        for n2 in range(N2-1):
            listPolys.append([N2*n1 + n2, N2*(n1+1) + n2, N2*(n1+1) + n2+1, N2*n1 + n2+1])
        listPolys.append([N2*n1 + N2-1, N2*(n1+1) + N2-1, N2*(n1+1) + 0, N2*n1 + 0])
    for n2 in range(N2-1):
        listPolys.append([N2*(N1-1) + n2, N2*0 + n2, N2*0 + n2+1, N2*(N1-1) + n2+1])
    listPolys.append([N2*(N1-1) + N2-1, N2*0 + N2-1, N2*0 + 0, N2*(N1-1) + 0])
    return listPolys
