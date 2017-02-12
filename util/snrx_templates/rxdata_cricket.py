from svrx.util.mesh import rxdata_from_pydata
from svrx.util.importers import named_mesh_path, obj_to_pydata_lite

@node_script
def sn_make_cricket() -> (Vertices, Edges, Faces):
    obj_path = named_mesh_path("cricket.obj")       #  returns the library path +  object name
    verts, _, faces = obj_to_pydata_lite(obj_path)  #  accepts full valid path
    return rxdata_from_pydata(verts, faces=faces)
