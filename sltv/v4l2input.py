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

import gobject
import pygst
pygst.require("0.10")
import gst
from input import *

class V4L2Input(Input):

    def __init__(self):
        Input.__init__(self)

        self.audio_src = gst.element_factory_make("autoaudiosrc", "audio_src")
        self.add(self.audio_src)
        self.video_src = gst.element_factory_make("v4l2src", "video_src")
        self.add(self.video_src)

        self.capsfilter = gst.element_factory_make("capsfilter", "capsfilter")
        self.add(self.capsfilter)

        gst.element_link_many(self.video_src, self.capsfilter)

        self.audio_pad.set_target(self.audio_src.src_pads().next())
        self.video_pad.set_target(self.capsfilter.src_pads().next())

    def config(self, dict):
        self.video_src.set_property("device", dict["v4l2_device"])
        caps = gst.caps_from_string(
            "video/x-raw-yuv, width=%d, height=%d" % (
                int(dict["width"]), int(dict["height"])
            )
        )
        self.capsfilter.set_property("caps", caps)
