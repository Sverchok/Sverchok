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


def draw_frame(x, y, w, h, t):
    coord = [(x, y), (x - t, y + t), (x + w, y), (x + w + t, y + t),
             (x + w, y - h), (x + w + t, y - t - h), (x, y - h), (x - t, y - h - t)]
    bgl.glColor3f(1, 0, 0)

    bgl.glBegin(bgl.GL_TRIANGLE_STRIP)
    for i in range(10):
        bgl.glVertex2f(*coord[i % 8])
    bgl.glEnd()


def draw_text(x, y, args):
    lines = args[0]
    w, h = args[1]
    max_len = args[2]
    #  disable reed frame for now
    #  draw_frame(x - 5, y + 5, w + 10, h + 40, 10)
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
    xpos = x + w + 30
    h = 1.3 * line_height * (len(lines) + 1)
    bgl.glColor3f(0.2,  0.2, 0.2)
    draw_rect(xpos, ypos + 1.5 * line_height, max_len * 8, h)
    bgl.glColor3f(*color)
    for line in lines:
        blf.position(0, xpos, ypos, 0)
        blf.draw(font_id, line)
        ypos -= int(line_height * 1.3)


def show(node, err, script=False):
    if node.bl_idname == "SvRxVirtualNode":
        return  # for now
    ng_name = node.id_data.name
    bgl_callback.callback_disable("error:" + ng_name)

    text = bpy.data.texts.get(ng_name + "_Error")
    if not text:
        text = bpy.data.texts.new(ng_name + "_Error")
    text.clear()
    msg = traceback.format_exc()
    print(msg, file=sys.stderr)
    text.from_string(msg)

    frames = traceback.extract_tb(err.__traceback__)
    if isinstance(err, SyntaxError):
        lines = ["SyntaxError"]
        lines.append("@ -> {}".format(err.text))
        lines.append("{}:{}".format(err.filename, err.lineno))
    else:
        lines = [str(type(err).__name__) + " " + str(err)]

        for info in reversed(frames):
            print(info)
            file = info[0].lower()

            if not script:
                loc = file.find("svrx")
                if loc == -1:
                    loc = file.find("bpy.data")
            else:
                loc = file.find("bpy.data")
                print(loc, file, *info)

            if loc > -1:
                lines.append("@ -> {}".format(info[3]))
                lines.append("{}:{} in {}".format(file[loc:], *info[1:3]))
                break

    x = node.location.x
    y = node.location.y
    max_len = max(map(len, lines))
    draw_data = {
        'tree_name': ng_name,
        'custom_function': draw_text,
        'loc': (x, y),
        'args': (lines, (node.width, node.height), max_len)
    }

    bgl_callback.callback_enable("error:" + node.id_data.name, draw_data)


def clear(ng):
    bgl_callback.callback_disable("error:" + ng.name)
