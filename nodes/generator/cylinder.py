from svrx.nodes.node_base import node_func
from svrx.typing import Float, Int, Vertices, Edges, Faces, BoolP

import numpy as np
from svrx.util.geom import generator
from svrx.util.smesh import SvPolygon
from svrx.util.topology import cylinder_edges, cylinder_faces
from svrx.util.function import array_as


@node_func(bl_idname="SvRxNodeGenCylinder", multi_label="Cylinder", id=0)
@generator
def cylinder(r_top: Float = 1.0,
             r_bot: Float = 1.0,
             h: Float = 10,
             verts: Int =20,
             rings: Int = 10,
             caps: BoolP = False) -> ([Vertices], [Edges], [Faces]):
    z = np.zeros((rings, 4))
    z[:,2] = np.linspace(0, h, rings)
    scale = np.linspace(r_bot, r_top, rings)
    t = np.linspace(0, np.pi * 2 * (verts - 1 / verts), verts)
    circle = np.array([np.cos(t), np.sin(t), np.zeros(verts), np.ones(verts)]).T
    cylinder = np.empty((rings, verts, 4))
    cylinder[:] = z[:, np.newaxis, :] + circle
    cylinder[:,:,:2] *= scale[:,np.newaxis,np.newaxis]
    cylinder.shape = (-1, 4)
    return cylinder, cylinder_edges(rings, verts), cylinder_faces(rings, verts, caps)

@node_func(id=1, label="Scale control")
@generator
def cylinder(scale: Float(iterable=False) = 1.0,
             z_scale: Float(iterable=False) = 1.0,
             verts: Int = 20,
             rings: Int = 10,
             caps: BoolP = False) -> ([Vertices], [Edges], [Faces]):
    z = np.zeros((rings, 4))
    if len(z_scale) == 1:
        z[:,2] = np.linspace(0, z_scale[0] * rings, rings)
    else:
        z[:,2] = array_as(z_scale, (rings,))
    scale = array_as(scale, (rings,))
    t = np.linspace(0, np.pi * 2 * (verts - 1 / verts), verts)
    circle = np.array([np.cos(t), np.sin(t), np.zeros(verts), np.ones(verts)]).T
    cylinder = np.empty((rings, verts, 4))
    cylinder[:] = z[:, np.newaxis, :] + circle
    cylinder[:,:,:2] *= scale[:,np.newaxis,np.newaxis]
    cylinder.shape = (-1, 4)
    print(rings, verts)
    return cylinder, cylinder_edges(rings, verts), cylinder_faces(rings, verts, caps)
