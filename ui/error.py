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
# ##### END GPL LICENSE BLOCK

import svrx.util.bgl_callback as bgl_callback
import bgl
import blf
import traceback
import bpy
import sys


def draw_rect(x=0, y=0, w=30, h=10):

    bgl.glBegin(bgl.GL_TRIANGLE_STRIP)

    bgl.glVertex2f(x, y)
    bgl.glVertex2f(x + w, y)
    bgl.glVertex2f(x, y-h)
    bgl.glVertex2f(w+x, y-h)
    bgl.glEnd()


def draw_text(x, y, args):
    lines = args[0]
    x, y = int(x), int(y)
    color = (0.9, 0.9, 0.9)
    font_id = 0

    text_height = 15
    line_height = 14

    # why does the text look so jagged?  <-- still valid question
    # dpi = bpy.context.user_preferences.system.dpi
    blf.size(font_id, int(text_height), 72)
    bgl.glColor3f(*color)
    ypos = y
    h = 1.3 * line_height * len(lines)
    for line in lines:
        blf.position(0, x, ypos, 0)
        blf.draw(font_id, line)
        ypos -= int(line_height * 1.3)


def show(node, err):
    if node.bl_idname == "SvRxVirtualNode":
        return  # for now
    ng_name = node.id_data.name
    text = bpy.data.texts.get(ng_name + "_Error")
    if not text:
        text = bpy.data.texts.new(ng_name + "_Error")
    text.clear()

    msg = traceback.format_exc()
    print(msg, file=sys.stderr)
    text.from_string(msg)
    print(err)

    msg = [str(err)]
    frames = traceback.extract_tb(err.__traceback__)
    for info in reversed(frames):
        file = info[0].lower()
        loc = file.find("svrx")
        if loc == -1:
            loc = file.find("bpy.data.texts")
        if loc > -1:
            msg.append("@ -> {}".format(info[3]))
            msg.append("{}:{} in {}".format(file[loc:], *info[1:3]))
            break

    x = node.location.x + node.width + 20
    y = node.location.y
    draw_data = {
        'tree_name': ng_name,
        'custom_function': draw_text,
        'loc': (x, y),
        'args': (msg,)
    }

    bgl_callback.callback_enable("error:" + node.id_data.name, draw_data)


def clear(ng):
    bgl_callback.callback_disable("error:" + ng.name)
