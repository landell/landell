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
from core import Input, INPUT_TYPE_VIDEO

CAPABILITIES = INPUT_TYPE_VIDEO

class XInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.video_src = gst.element_factory_make("ximagesrc", "video_src")

        # Setting format to time, to work with input-selector, since they're
        # were not working together in version 0.10.18-1 from Debian.
        # This should be fixed in ximagesrc's code and input-selector should
        # also be fixed to work with byte format.

        self.video_src.set_format(gst.FORMAT_TIME)
        self.video_src.set_property("use-damage", False)

        self.add(self.video_src)
        self.capsfilter = gst.element_factory_make("capsfilter", "capsfilter")
        self.add(self.capsfilter)

        gst.element_link_many(self.video_src, self.capsfilter)

        self.video_pad.set_target(self.capsfilter.src_pads().next())

    def config(self, dict):
        caps = gst.caps_from_string(
            "video/x-raw-rgb, framerate=%d/1" % int(dict["framerate"])
        )
        self.capsfilter.set_property("caps", caps)
