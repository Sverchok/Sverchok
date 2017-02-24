
import bgl
import blf

import bpy
import bmesh
import time


from svrx.nodes.node_base import stateful
from svrx.nodes.classes import NodeID, NodeStateful
from svrx.typing import (Required, StringP,
                         Anytype, BoolP, ColorP, FVectorP,
                         BMesh, Matrix, Vertices, Faces, Edges)
from svrx.util import bgl_callback_3dview as bgl_callback
import itertools
import mathutils as mu
from svrx.util.mesh import bmesh_from_pydata

class NodeView(NodeID, NodeStateful):

    def draw_buttons(self, context, layout):
        view_icon = 'RESTRICT_VIEW_' + ('OFF' if self.activate else 'ON')
        layout.prop(self, "activate", text="Show", toggle=True, icon=view_icon)
        col = layout.column()
        row = col.row(align=True)
        row.prop(self, "display_vert", toggle=True, icon='VERTEXSEL', text='')
        row.prop(self, "vert_color", text="")

        row = col.row(align=True)
        row.prop(self, "display_edge", toggle=True, icon='EDGESEL', text='')
        row.prop(self, "edge_color", text="")

        row = col.row(align=True)
        row.prop(self, "display_face", toggle=True, icon='FACESEL', text='')
        row.prop(self, "face_color", text="")

    def free(self):
        bgl_callback.callback_disable(self.node_id)


def draw_bmesh(context, args):
    obj_list = args[0]
    face_list = args[1]
    col_list = args[2]
    edg_list = args[3]
    edge_col, vert_col = args[4]

    for verts, vert_index, colors, edges in zip(obj_list, face_list, col_list, edg_list):
        if vert_index:
            bgl.glBegin(bgl.GL_TRIANGLES)
            for idx in range(0, len(vert_index), 3):
                p0 = verts[vert_index[idx]]
                p1 = verts[vert_index[idx + 1]]
                p2 = verts[vert_index[idx + 2]]
                bgl.glColor3f(*colors[idx//3])
                bgl.glVertex3f(*p0)
                bgl.glVertex3f(*p1)
                bgl.glVertex3f(*p2)
            bgl.glEnd()
        if vert_col:
            bgl.glBegin(bgl.GL_POINTS)
            bgl.glColor3f(*vert_col)
            for vert in verts:
                bgl.glVertex3f(*vert)
            bgl.glEnd()
        if edge_col:
            bgl.glBegin(bgl.GL_LINES)
            bgl.glColor3f(*edge_col)
            for x, y in edges:
                bgl.glVertex3f(*verts[x])
                bgl.glVertex3f(*verts[y])
            bgl.glEnd()


@stateful
class BMViewNode():

    bl_idname = "SvRxNodeBMViewGL"
    label = "View bm GL"
    cls_bases = (NodeView,)

    properties = {
        'activate': BoolP(name='activate', default=True),
        "vert_color": ColorP(default=(1., 1., 1.)),
        "edge_color": ColorP(default=(1., 1., .1)),
        "face_color": ColorP(default=(1., .8, .8)),
        "display_vert": BoolP(name='show_verts', default=True),
        "display_edge": BoolP(name='show_edges', default=True),
        "display_face": BoolP(name='show_faces', default=True)
    }

    def __init__(self, node=None):
        if node is not None:
            self.node = node
            self.activate = node.activate
            self.n_id = node.node_id

    def start(self):
        self.vertices = []
        self.faces = []
        self.colors = []
        self.edges = []

    @property
    def current_draw_data(self):
        args = (self.vertices, self.faces, self.colors, self.edges,
                (self.node.edge_color[:] if self.node.display_edge else None,
                 self.node.vert_color[:] if self.node.display_vert else None))
        return {
            'tree_name': self.node.id_data.name[:],
            'custom_function': draw_bmesh,
            'args': args
        }

    def stop(self):
        bgl_callback.callback_disable(self.n_id)
        if self.activate:
            bgl_callback.callback_enable(self.n_id, self.current_draw_data, overlay="POST_VIEW")

    def __call__(self, bm: BMesh = Required,
                 mat: Matrix = None):
        color = self.node.face_color[:]
        tess_faces = bm.calc_tessface()
        vert_index = [l.vert.index for l in itertools.chain(*bm.calc_tessface())]
        bm.normal_update()
        if mat is not None:
            matrix = mu.Matrix(mat)
            verts = [matrix * v.co for v in bm.verts]
            mat33 = matrix.to_3x3()
            normals = [mat33 * f.normal for f in bm.faces]
        else:
            verts = [v.co for v in bm.verts]
            normals = [f.normal for f in bm.faces]

        face_index = [t_f[0].face.index for t_f in tess_faces]
        edges_index = [(e.verts[0].index, e.verts[1].index) for e in bm.edges]
        colors = []
        for idx in face_index:
            normal = normals[idx]
            normal_nu = normal.angle((0, 0, 1), 0) / 3.14
            r = (normal_nu * color[0]) - 0.1
            g = (normal_nu * color[1]) - 0.1
            b = (normal_nu * color[2]) - 0.1
            colors.append((r, g, b))

        self.vertices.append(verts)
        self.faces.append(vert_index if self.node.display_face else [])
        self.colors.append(colors)
        self.edges.append(edges_index)



@stateful
class ViewNode(BMViewNode):
    bl_idname = "SvRxNodeRxViewGL"
    label = "Viewer Rx GL"

    def __call__(self,
                verts: Vertices = Required,
                edges: Edges = None,
                faces: Faces = None,
                mat: Matrix = None):
        bm = bmesh_from_pydata(verts[:,:3].tolist(), edges, faces)
        super().__call__(bm, mat)
