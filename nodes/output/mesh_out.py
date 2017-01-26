import bpy
import bmesh

from svrx.nodes.node_base import Stateful
from svrx.typing import Vertices, Required, Faces, Edges


class MeshOut(Stateful):
    def __init__(self):
        self.start()

    bl_idname = "SvRxNodeMeshOut"
    label = "Mesh out"

    inputs_template = [('SvRxVertexSocket', 'Vertices', None),
                       ('SvRxTopoSocket', 'Edges', None),
                       ('SvRxTopoSocket', 'Faces', None)]

    outputs_template = []
    properties = {}
    parameters = [(0, 0), (1, 0), (2, 0)]
    returns = []

    def start(self):
        self.verts = []
        self.edges = []
        self.faces = []

    def stop(self):
        for idx, verts, edges, faces in zip(range(1000), self.verts, self.edges, self.faces):
            make_bmesh_geometry(verts[:, :3], edges, faces, idx=idx)

    def __call__(self, verts: Vertices = Required, edges: Edges = None, faces: Faces = None):
        self.verts.append(verts)
        self.edges.append(edges)
        self.faces.append(faces)



def default_mesh(name):
    verts, faces = [(1, 1, -1), (1, -1, -1), (-1, -1, -1)], [(0, 1, 2)]
    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()
    return mesh_data


def make_bmesh_geometry(verts, edges=None, faces=None, name="svrx_mesh", idx=0):
    scene = bpy.context.scene
    meshes = bpy.data.meshes
    objects = bpy.data.objects
    name = name + "_" + str(idx)
    vert_count = len(verts)

    if name in objects:
        sv_object = objects[name]
    else:
        temp_mesh = default_mesh(name)
        sv_object = objects.new(name, temp_mesh)
        scene.objects.link(sv_object)

    mesh = sv_object.data

    ''' get bmesh, write bmesh to obj, free bmesh'''
    bm = bmesh_from_pydata(verts, edges, faces)
    bm.to_mesh(sv_object.data)
    bm.free()

    sv_object.hide_select = False


def bmesh_from_pydata(verts=None, edges=None, faces=None):
    ''' verts is necessary, edges/faces are optional '''

    bm = bmesh.new()
    add_vert = bm.verts.new
    [add_vert(co) for co in verts]
    bm.verts.index_update()

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    if len(faces):
        add_face = bm.faces.new
        for face in faces:
            add_face(tuple(bm.verts[i] for i in face))
        bm.faces.index_update()

    if len(edges):
        add_edge = bm.edges.new
        for edge in edges:
            edge_seq = tuple(bm.verts[i] for i in edge)
            try:
                add_edge(edge_seq)
            except ValueError:
                # edge exists!
                pass

        bm.edges.index_update()

    return bm
