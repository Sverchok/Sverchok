import bpy
import bmesh

from svrx.nodes.node_base import stateful
from svrx.typing import Vertices, Required, Faces, Edges, StringP
from svrx.util.mesh import bmesh_from_pydata

# pylint: disable=C0326

@stateful
class MeshOut():

    def __init__(self, node=None):
        if node:
            self.base_name = node.name
        self.start()

    bl_idname = "SvRxNodeMeshOut"
    label = "Mesh out"

    def start(self):
        self.verts = []
        self.edges = []
        self.faces = []


    def stop(self):
        obj_index = 0
        #  using range to limit object number for now during testing
        for idx, verts, edges, faces in zip(range(100), self.verts, self.edges, self.faces):
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

    if rx_name in objects:
        obj = objects[rx_name]
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
