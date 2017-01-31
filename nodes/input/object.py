
from svrx.typing import Vertices, Edges, Object, Faces
from svrx.nodes.node_base import node_func
from svrx.util.smesh import SMesh

@node_func(bl_idname="SvRxObjectIn")
def object_in(obj : Object = None) -> (Vertices, Edges, Faces):
    if obj and obj.type == 'MESH':
        sm = SMesh.from_mesh(obj.data)
        return sm.as_pydata()
    else:
        return None, None, None
