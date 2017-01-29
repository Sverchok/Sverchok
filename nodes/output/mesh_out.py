import bpy
import bmesh

from svrx.nodes.node_base import Stateful
from svrx.typing import Vertices, Required, Faces, Edges

# pylint: disable=C0326

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
        obj_index = 0
        for idx, verts, edges, faces in zip(range(1000), self.verts, self.edges, self.faces):
            obj_index = idx
            make_bmesh_geometry(verts[:, :3], edges, faces, idx=idx, normal_update=False)

        # cleanup
        self.remove_non_updated_objects(obj_index)


    def __call__(self, verts: Vertices = Required, edges: Edges = None, faces: Faces = None):
        self.verts.append(verts)
        self.edges.append(edges)
        self.faces.append(faces)


    def get_children(self, basename):
        objects = bpy.data.objects
        objs = [obj for obj in objects if obj.type == 'MESH']
        return [o for o in objs if o.get('basename') == basename]


    def remove_non_updated_objects(self, obj_index):
        objs = self.get_children("svrx_mesh")
        objs = [obj.name for obj in objs if obj['idx'] > obj_index]
        if not objs:
            return

        meshes = bpy.data.meshes
        objects = bpy.data.objects
        scene = bpy.context.scene

        # remove excess objects
        for object_name in objs:
            obj = objects[object_name]
            obj.hide_select = False
            scene.objects.unlink(obj)
            objects.remove(obj, do_unlink=True)

        # delete associated meshes
        for object_name in objs:
            meshes.remove(meshes[object_name])



def make_bmesh_geometry(verts, edges=None, faces=None, name="svrx_mesh", idx=0, normal_update=True):

    scene = bpy.context.scene
    meshes = bpy.data.meshes
    objects = bpy.data.objects

    rx_name = name + "." + str(idx).zfill(4)

    # def assign_empty_mesh(idx):
    #     if rx_name in meshes:
    #         meshes.remove(meshes[rx_name])
    #     return meshes.new(rx_name)

    def assign_empty_mesh(idx):
        # if rx_name in meshes:
        bm = bmesh.new()   # create an empty BMesh
        # bm.from_mesh(meshes[rx_name])
        # bm.clear()
        bm.to_mesh(meshes[rx_name])
        bm.free()
        return meshes[rx_name]
    
    if rx_name in objects:
        obj = objects[rx_name]
        obj.data = assign_empty_mesh(idx)
        obj.data.update()
    else:
        # this is only executed once, upon the first run.
        mesh = meshes.new(rx_name)
        obj = objects.new(rx_name, mesh)
        scene.objects.link(obj)

        obj['idx'] = idx
        obj['basename'] = name

    # at this point the mesh is always fresh and empty

    ''' get bmesh, write bmesh to obj, free bmesh'''
    bm = bmesh_from_pydata(verts, edges, faces, normal_update)
    bm.to_mesh(obj.data)
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

    if not faces is None and len(faces):
        add_face = bm.faces.new
        for face in faces:
            add_face(tuple(bm.verts[i] for i in face))

        bm.faces.index_update()

    if not edges is None and len(edges):
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
