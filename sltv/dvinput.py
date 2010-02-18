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

import gobject
import pygst
pygst.require("0.10")
import gst
from input import *

class DVInput(Input):

    def __init__(self):
        Input.__init__(self)
        self.dv_src = gst.element_factory_make("dv1394src", "video_src")
        self.add(self.dv_src)
        self.dvdemux = gst.element_factory_make("dvdemux", "dvdemux")
        self.add(self.dvdemux)
        self.video_queue = gst.element_factory_make("queue", "video_demux_queue")
        self.add(self.video_queue)
        self.dvdec = gst.element_factory_make("dvdec", "dvdec")
        self.add(self.dvdec)
        self.videoscale = gst.element_factory_make(
                "videoscale", "dv_videoscale"
        )
        self.add(self.videoscale)
        self.capsfilter = gst.element_factory_make("capsfilter", "capsfilter")
        self.add(self.capsfilter)
        gst.element_link_many(
                self.dv_src, self.dvdemux,
        )
        gst.element_link_many(
                self.video_queue, self.dvdec,
                self.videoscale, self.capsfilter
        )
        self.video_pad.set_target(self.capsfilter.src_pads().next())

    def on_pad_added(self, element, pad):
        name = pad.get_caps()[0].get_name()

        if "video" in name:
            pad.link(self.video_queue.get_static_pad("sink"))

        if "audio" in name:
            self.audio_pad.set_target(pad)

    def config(self, dict):
        self.dv_src.set_property("channel", int(dict["channel"]))
