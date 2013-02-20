# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
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
from utils import Fract

class VideoConverter(Gst.Bin):

    def __init__(self):
        Gst.Bin.__init__(self)
        self.colorspace = Gst.ElementFactory.make(
                "colorspace", "videoconvert_colorspace"
        )
        self.add(self.colorspace)

        self.videorate = Gst.ElementFactory.make(
                "videorate", "videoconvert_videorate"
        )
        self.add(self.videorate)

        self.videoscale = Gst.ElementFactory.make(
                "videoscale", "videoconvert_videoscale"
        )
        self.add(self.videoscale)
        self.videoscale.set_property("method", 1)

        self.capsfilter = Gst.ElementFactory.make(
                "capsfilter", "videoconvert_capsfilter"
        )
        self.add(self.capsfilter)

        self.colorspace.link(self.videorate)
        self.videorate.link(self.videoscale)
        self.videoscale.link(self.capsfilter)

        self.source_pad = Gst.GhostPad(
                "src", self.capsfilter.src_pads().next()
        )
        self.add_pad(self.source_pad)
        self.sink_pad = Gst.GhostPad(
                "sink", self.colorspace.sink_pads().next()
        )
        self.add_pad(self.sink_pad)

    def config(self, dict):
        num, den = Fract.fromdecimal(dict["framerate"])
        caps = Gst.caps_from_string(
                "video/x-raw-yuv, width=%d, height=%d, framerate=%d/%d" % (
                    int(dict["width"]), int(dict["height"]), num, den
                )
        )
        self.capsfilter.set_property("caps", caps)
