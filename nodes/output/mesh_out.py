import bpy
import bmesh

from svrx.nodes.node_base import stateful
from svrx.typing import Vertices, Required, Faces, Edges, StringP, IntP, Matrix, BMesh
from svrx.util.mesh import bmesh_from_pydata

# pylint: disable=C0326

class Mesh_out_common:
    def __init__(self, node=None):
        if node:
            self.base_name = node.mesh_name
            self.max_mesh_count = node.max_mesh_count
        self.start()

    def get_children(self, basename):
        objects = bpy.data.objects
        objs = [obj for obj in objects if obj.type == 'MESH']
        return [o for o in objs if o.get('basename') == basename]


    def remove_non_updated_objects(self, obj_index):
        objs = self.get_children(self.base_name)
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

@stateful
class MeshOut(Mesh_out_common):

    bl_idname = "SvRxNodeMeshOut"
    label = "Mesh out"

    properties = {'mesh_name': StringP(name='Mesh name', default="svrx_mesh"),
                  'max_mesh_count': IntP(name="Max count", default=100)}

    def start(self):
        self.verts = []
        self.edges = []
        self.faces = []
        self.mats = []

    def stop(self):
        obj_index = 0
        #  using range to limit object number for now during testing
        param = zip(range(self.max_mesh_count), self.verts, self.edges, self.faces, self.mats)
        for idx, verts, edges, faces, mat in param:
            obj_index = idx
            bm = bmesh_from_pydata(verts[:, :3].tolist(), edges, faces, normal_update=False)
            obj = make_bmesh_geometry(bm,
                                      name=self.base_name,
                                      idx=idx,)
            if mat is not None:
                obj.matrix_world = mat.T

        # cleanup
        self.remove_non_updated_objects(obj_index)


    def __call__(self,
                 verts: Vertices = Required,
                 edges: Edges = None,
                 faces: Faces = None,
                 matrix: Matrix = None):
        self.verts.append(verts)
        self.edges.append(edges)
        self.faces.append(faces)
        self.mats.append(matrix)





@stateful
class BMesh_out(Mesh_out_common):
    bl_idname = "SvRxNodeBmeshOut"
    label = "BMesh out"

    properties = {'mesh_name': StringP(name='Mesh name', default="svrx_bm"),
                  'max_mesh_count': IntP(name="Max count", default=100)}
    def start(self):
        self.meshes = []
        self.mats = []

    def __call__(self, bm: BMesh = Required, mat: Matrix = None):
        self.meshes.append(bm.copy())
        self.mats.append(mat)

    def stop(self):
        obj_index = 0
        for idx, bm, mat in zip(range(self.max_mesh_count), self.meshes, self.mats):
            obj_index = idx
            obj = make_bmesh_geometry(bm, name=self.base_name, idx=idx)
            if mat is not None:
                obj.matrix_world = mat.T

        self.remove_non_updated_objects(obj_index)


def make_bmesh_geometry(bm, name="svrx_mesh", idx=0):

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
    bm.to_mesh(obj.data)
    bm.free()

    obj.update_tag(refresh={'OBJECT', 'DATA'})
    obj.hide_select = False
    return obj
