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
from core import Input, INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

class DVInput(Input):

    def __init__(self):
        Input.__init__(self, INPUT_TYPE_AUDIO | INPUT_TYPE_VIDEO)
        self.dv_src = gst.element_factory_make("dv1394src", "video_src")
        self.add(self.dv_src)
        self.capsfilter = gst.element_factory_make(
                "capsfilter", "dv_capsfilter"
        )
        self.add(self.capsfilter)
        self.tee = gst.element_factory_make("tee", "dv_tee")
        self.add(self.tee)
        self.queue_save = gst.element_factory_make("queue", "dv_save_queue")
        self.add(self.queue_save)
        self.queue_src = gst.element_factory_make("queue", "dv_src_queue")
        self.add(self.queue_src)
        self.filesink = gst.element_factory_make("filesink", "dvfilesink")
        self.add(self.filesink)
        self.dvdemux = gst.element_factory_make("dvdemux", "dvdemux")
        self.add(self.dvdemux)
        self.dvdemux.connect("pad-added", self.on_pad_added)
        self.video_queue = gst.element_factory_make("queue", "video_demux_queue")
        self.add(self.video_queue)
        self.dvdec = gst.element_factory_make("dvdec", "dvdec")
        self.add(self.dvdec)
        self.videoscale = gst.element_factory_make(
                "videoscale", "dv_videoscale"
        )
        self.add(self.videoscale)
        gst.element_link_many(
                self.dv_src, self.capsfilter, self.tee, self.queue_src, self.dvdemux,
        )
        gst.element_link_many(
                self.tee, self.queue_save, self.filesink
        )
        gst.element_link_many(
                self.video_queue, self.dvdec, self.videoscale
        )
        self.video_pad.set_target(self.videoscale.src_pads().next())

    def on_pad_added(self, element, pad):
        name = pad.get_caps()[0].get_name()

        if "video" in name:
            pad.link(self.video_queue.get_static_pad("sink"))

        if "audio" in name:
            self.audio_pad.set_target(pad)

    def config(self, dict):
        self.dv_src.set_property("channel", int(dict["channel"]))
        self.dv_src.set_property("port", int(dict["port"]))
        caps = gst.caps_from_string(
            "video/x-dv, width=%d, height=%d" % (
                int(dict["width"]), int(dict["height"])
            )
        )
        self.capsfilter.set_property("caps", caps)
        self.filesink.set_property("location", dict["filename"])
