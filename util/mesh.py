# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# pylint: disable=W0141

from itertools import chain, islice, accumulate

import numpy as np

import bmesh

from svrx.util.smesh import SvPolygon, SMesh, SvVertices, SvEdges


def bmesh_from_pydata(verts, edges=None, faces=None, normal_update=False):
    ''' verts is necessary, edges/faces are optional
        normal_update, will update verts/edges/faces normals at the end
    '''

    bm = bmesh.new()
    add_vert = bm.verts.new

    for co in verts:
        add_vert(co)

    bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    if not faces is None:
        add_face = bm.faces.new
        for face in faces:
            add_face(tuple(bm.verts[i] for i in face))

        bm.faces.index_update()

    if not edges is None:
        add_edge = bm.edges.new
        for edge in edges:
            edge_seq = tuple(bm.verts[i] for i in edge)
            try:
                add_edge(edge_seq)
            except ValueError:
                # edge exists!
                pass

        bm.edges.index_update()

    if normal_update:
        bm.normal_update()
    return bm


def rxdata_from_bm(bm):
    vert_count = len(bm.verts)
    vertices = np.ones((vert_count, 4), dtype=np.float64)
    for idx, v in enumerate(bm.verts):
        vertices[idx,:3] = v.co
    edges = np.array([(e.verts[0].index, e.verts[1].index) for e in bm.edges], dtype=np.uint32)
    faces = SvPolygon.from_pydata([[i.index for i in p.verts] for p in bm.faces])
    return vertices, edges, faces

def rxdata_from_pydata(verts, edges=None, faces=None):
    # v = SvVertices.from_pydata(verts)
    # e = SvEdges.from_pydata(edges)
    # f = SvPolygon.from_pydata(faces)
    # return v, e, f
    return SMesh.from_pydata(verts, edges, faces).as_rxdata


def rxdata_to_mesh(mesh, rx, validate=True):

    num_new_verts = len(rx.vertices) - len(mesh.vertices)
    num_new_edges = len(rx.edges) - len(mesh.edges)
    num_new_faces = len(rx.faces) - len(mesh.polygons)
    face_lengths = tuple(map(len, rx.faces))
    old_face_lengths = tuple(map(len, (p.vertices for p in mesh.polygons)))
    num_new_face_lengths = sum(face_lengths) - sum(old_face_lengths)

    if any(n < 0 for n in [num_new_verts, num_new_edges, num_new_faces]):

        # replace mesh with empty and build.
        bm = bmesh.new()
        bm.to_mesh(mesh)
        bm.free()

        mesh.vertices.add(len(rx.vertices))
        mesh.edges.add(len(rx.edges))
        mesh.loops.add(sum(face_lengths))
        mesh.polygons.add(len(rx.faces))

    if all(n == 0 for n in [num_new_verts, num_new_edges, num_new_faces]):
        ### other sick logic.
        # not clear yet, polygon count can be the same but the loops might need to be updated?
        ...
    else:
        mesh.vertices.add(num_new_verts)
        mesh.edges.add(num_new_edges)
        mesh.loops.add(num_new_face_lengths)
        mesh.polygons.add(num_new_faces)


    mesh.vertices.foreach_set("co", rx.vertices.flatten().astype(dtype=np.float32))
    mesh.edges.foreach_set("vertices", rx.edges.flatten().astype(dtype=np.uint32))

    vertex_indices = rx.faces.flatten().astype(dtype=np.uint32)

    loop_starts = np.cumsum(face_lengths, axis=0, dtype=np.uint32)   (insert 0 )
    np.roll(loop_starts, 1)
    loop_starts[0] = 0

    mesh.polygons.foreach_set("loop_total", face_lengths)
    mesh.polygons.foreach_set("loop_start", loop_starts)
    mesh.polygons.foreach_set("vertices", vertex_indices)

    # if no edges - calculate them
    if rx.faces and (not rx.edges):
        mesh.update(calc_edges=True)

    if validate:
        mesh.validate()