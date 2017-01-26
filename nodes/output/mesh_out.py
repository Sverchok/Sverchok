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



def make_bmesh_geometry(verts, edges=None, faces=None, name="svrx_mesh", idx=0):

    scene = bpy.context.scene
    meshes = bpy.data.meshes
    objects = bpy.data.objects

    name = name + "." + str(idx).zfill(4)

    def assign_empty_mesh(idx):
        if name in meshes:
            meshes.remove(meshes[name])
        return meshes.new(name)
    
    if name in objects:
        obj = objects[name]
        obj.data = assign_empty_mesh(idx)
    else:
        # this is only executed once, upon the first run.
        mesh = meshes.new(name)
        obj = objects.new(name, mesh)
        scene.objects.link(obj)

    # at this point the mesh is always fresh and empty
    obj['idx'] = idx
    obj['basename'] = name


    ''' get bmesh, write bmesh to obj, free bmesh'''
    bm = bmesh_from_pydata(verts, edges, faces, normal_update=True)
    bm.to_mesh(mesh)
    bm.free()

    obj.update_tag(refresh={'OBJECT', 'DATA'})
    obj.hide_select = False


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
