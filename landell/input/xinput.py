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
from landell.utils import Fract

CAPABILITIES = INPUT_TYPE_VIDEO

class XInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.video_src = Gst.ElementFactory.make("ximagesrc", "video_src")

        # Setting format to time, to work with input-selector, since they're
        # were not working together in version 0.10.18-1 from Debian.
        # This should be fixed in ximagesrc's code and input-selector should
        # also be fixed to work with byte format.

        self.video_src.set_format(Gst.Format.TIME)
        self.video_src.set_property("use-damage", False)
        self.video_src.set_property("endx", 800)
        self.video_src.set_property("endy", 600)

        self.add(self.video_src)
        self.capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        self.add(self.capsfilter)

        self.video_src.link(self.capsfilter)

        self.video_pad = Gst.GhostPad.new("video_pad", self.capsfilter.get_static_pad("src"))
        if (self.video_pad is None):
            Log.warning("error creating input")
        self.add_pad(self.video_pad)

    def config(self, dict):
        num, den = Fract.fromdecimal(dict["framerate"])
        caps = Gst.caps_from_string(
            "video/x-raw, framerate=%d/%d" % (num, den)
        )
        self.capsfilter.set_property("caps", caps)
