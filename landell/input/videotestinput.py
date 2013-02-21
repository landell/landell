# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst
from core import Input, INPUT_TYPE_VIDEO

CAPABILITIES = INPUT_TYPE_VIDEO

class VideoTestInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)

        self.video_src = Gst.ElementFactory.make("videotestsrc", "video_src")
        self.video_src.set_property("is-live", True)
        self.add(self.video_src)

        self.capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        self.add(self.capsfilter)

        self.video_src.link(self.capsfilter)

        self.video_pad.set_target(self.capsfilter.src_pads().next())

    def config(self, dict):
        self.video_src.set_property("pattern", int(dict["pattern"]))
        caps = Gst.caps_from_string(
            "video/x-raw, width=%d, height=%d" % (
                int(dict["width"]), int(dict["height"])
            )
        )
        self.capsfilter.set_property("caps", caps)
