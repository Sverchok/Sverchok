import bgl
import blf

import bpy
import bmesh
import time
from svrx.nodes.node_base import stateful
from svrx.nodes.classes import NodeID, NodeStateful
from svrx.typing import Required, StringP, Anytype, BoolP
from svrx.util import bgl_callback_3dview_2d as bgl_callback

# pylint: disable=C0326


def draw_indexviz(context, args):

    draw_verts, draw_edges, draw_faces, draw_matrix = args.data

    # ensure data or empty lists.
    data_vector = Vector_generate(draw_verts) if draw_verts else []
    data_edges = draw_edges
    data_faces = draw_faces
    data_matrix = Matrix_generate(draw_matrix) if draw_matrix else []


    if (data_vector, data_matrix) == (0, 0):
    #    callback_disable(n_id)
    #   not sure that it is safe to disable the callback in callback
    #   just return instead.
        return

    fx = args.fx
    region = context.region
    region3d = context.space_data.region_3d

    # vars for projection
    perspective_matrix = region3d.perspective_matrix.copy()

    font_id = 0
    text_height = 13
    blf.size(font_id, text_height, 72)  # should check prefs.dpi

    region_mid_width = region.width / 2.0
    region_mid_height = region.height / 2.0


    def draw_index(rgb, rgb2, index, vec):

        vec_4d = perspective_matrix * vec.to_4d()
        if vec_4d.w <= 0.0:
            return

        x = region_mid_width + region_mid_width * (vec_4d.x / vec_4d.w)
        y = region_mid_height + region_mid_height * (vec_4d.y / vec_4d.w)
        index = str(index)

        if fx.draw_bg:
            polyline = get_points(index)

            ''' draw polygon '''
            bgl.glColor4f(*rgb2)
            bgl.glBegin(bgl.GL_POLYGON)
            for pointx, pointy in polyline:
                bgl.glVertex2f(pointx+x, pointy+y)
            bgl.glEnd()

        ''' draw text '''
        txt_width, txt_height = blf.dimensions(0, index)
        bgl.glColor4f(*rgb)
        blf.position(0, x - (txt_width / 2), y - (txt_height / 2), 0)
        blf.draw(0, index)

    ########
    # points
    def calc_median(vlist):
        a = Vector((0, 0, 0))
        for v in vlist:
            a += v
        return a / len(vlist)

    for obj_index, verts in enumerate(data_vector):
        final_verts = verts

        # quickly apply matrix if necessary
        if draw_matrix:
            matrix = data_matrix[obj_index]
            final_verts = [matrix * v for v in verts]

        if fx.display_vert_index:
            for idx, v in enumerate(final_verts):
                draw_index(fx.vert_idx_color, fx.vert_bg_color, idx, v)

        if data_edges and fx.display_edge_index:
            for edge_index, (idx1, idx2) in enumerate(data_edges[obj_index]):
                
                v1 = Vector(final_verts[idx1])
                v2 = Vector(final_verts[idx2])
                loc = v1 + ((v2 - v1) / 2)
                draw_index(fx.edge_idx_color, fx.edge_bg_color, edge_index, loc)

        if data_faces and fx.display_face_index:
            for face_index, f in enumerate(data_faces[obj_index]):
                verts = [Vector(final_verts[idx]) for idx in f]
                median = calc_median(verts)
                draw_index(fx.face_idx_color, fx.face_bg_color, face_index, median)




class NodeIndexView(NodeID, NodeStateful):

    def free(self):
        bgl_callback.callback_disable(self.node_id)



@stateful
class SvRxIndexView():

    bl_idname = "SvRxIndexView"
    label = "Index View"
    cls_bases = (NodeIndexView,)

    properties = {
        'activate': BoolP(name='activate', default=True),
        'draw_bg': BoolP(name='draw bg', default=False),
        "vert_idx_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(1., 1., 1., 1.), subtype='COLOR'),
        "edge_idx_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(1., 1., .1, 1.), subtype='COLOR'),
        "face_idx_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(1., .8, .8, 1.), subtype='COLOR'),
        "vert_bg_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "edge_bg_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "face_bg_color": FloatVectorP(size=4, min=0.0, max=1.0, default=(.2, .2, .2, 1.), subtype='COLOR'),
        "display_vert_index": BoolP(name='show_verts', default=True), 
        "display_edge_index": BoolP(name='show_edges', default=True),
        "display_face_index": BoolP(name='show_faces', default=True)
    }

    def __init__(self, node=None):
        if node is not None:
            self.node = node
            self.activate = node.activate
            self.n_id = node.node_id


    @property
    def get_fx(self):
        params = [
           "vert_idx_color", "edge_idx_color", "face_idx_color",
           "vert_bg_color", "edge_bg_color", "face_bg_color",
           "display_vert_index", "display_edge_index", "display_face_index",
           "draw_bg"
        ]

        fx = namedtuple('fx', params)
        for param_name in params:
            if param_name.endswith('index'):
                param_value = getattr(self.param_name)
            else:
                param_value = getattr(self.param_name)[:]
            setattr(fx, param_name, param_value)
        return fx


    @property
    def get_data(self):
        return 


    @property
    def current_draw_data(self):
        args.fx = self.get_fx
        args.data = self.get_data
        return {
            'tree_name': self.node.id_data.name[:],
            'custom_function': draw_index_viz,
            'args': args
        }


    def stop(self):
        bgl_callback.callback_disable(self.n_id)
        if self.activate:
            bgl_callback.callback_enable(self.n_id, self.current_draw_data)


    def __call__(self, data: Anytype = Required):
        pass
