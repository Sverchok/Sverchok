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
    rxm = SMesh.from_pydata(verts, edges, faces)
    return rxm.vertices, rxm.edges, rxm.faces