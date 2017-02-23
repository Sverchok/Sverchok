# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import numpy as np

from svrx.typing import Float, Int, Vertices, BoolP
from svrx.nodes.node_base import node_func

from svrx.util.function import generator


def gen_rand_vecs(dims, number):
    vecs = np.random.normal(size=(number, dims))
    mags = np.linalg.norm(vecs, axis=-1)
    return vecs / mags[..., np.newaxis]


@node_func(bl_idname="SvRxNodeVectorRandom")
@generator
def random_unit_vector(size: Int =1,
                       seed: Int = 1,
                       scale: Float = 1.0,
                       point: BoolP = False
                       ) -> [Vertices]:
    np.random.seed(seed)
    if point:
        res = np.ones((size, 4))
    else:
        res = np.zeros((size, 4))
    res[:, :3] = scale * gen_rand_vecs(3, size)
    return res
