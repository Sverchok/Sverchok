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
    name = name + "." + str(idx).zfill(4)

    def assign_empty_mesh(idx):
        meshes = bpy.data.meshes
        mt_name = name
        if mt_name in meshes:
            return meshes[mt_name]
        else:
            return meshes.new(mt_name)
    
    # remove object
    if name in objects:
        obj = objects[name]
        # assign the object an empty mesh, this allows the current mesh
        # to be uncoupled and removed from bpy.data.meshes
        obj.data = assign_empty_mesh(idx)

        # remove uncoupled mesh, and add it straight back.
        if name in meshes:
            meshes.remove(meshes[name])
        mesh = meshes.new(name)
        obj.data = mesh
    else:
        # this is only executed once, upon the first run.
        mesh = meshes.new(name)
        obj = objects.new(name, mesh)
        scene.objects.link(obj)

    # at this point the mesh is always fresh and empty
    obj['idx'] = idx
    obj['basename'] = name


    ''' get bmesh, write bmesh to obj, free bmesh'''
    bm = bmesh_from_pydata(verts, edges, faces, normals_update=True)
    bm.to_mesh(mesh)
    bm.free()

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

    if faces:
        add_face = bm.faces.new
        for face in faces:
            add_face(tuple(bm.verts[i] for i in face))

        bm.faces.index_update()

    if edges:
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