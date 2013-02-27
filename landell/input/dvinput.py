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
from core import Input, INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO
from landell.log import Log

CAPABILITIES = INPUT_TYPE_AUDIO | INPUT_TYPE_VIDEO

class DVInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.dv_src = Gst.ElementFactory.make("dv1394src", "video_src")
        self.dv_src.set_property("use-avc", False)
        self.add(self.dv_src)
        self.capsfilter = Gst.ElementFactory.make(
                "capsfilter", "dv_capsfilter"
        )
        self.add(self.capsfilter)
        self.tee = Gst.ElementFactory.make("tee", "dv_tee")
        self.add(self.tee)
        self.queue_src = Gst.ElementFactory.make("queue", "dv_src_queue")
        self.add(self.queue_src)
        self.dvdemux = Gst.ElementFactory.make("ffdemux_dv", "dvdemux")
        self.add(self.dvdemux)
        self.dvdemux.connect("pad-added", self.on_pad_added)
        self.video_queue = Gst.ElementFactory.make(
                "multiqueue", "video_demux_queue"
        )
        self.add(self.video_queue)

        self.videoconvert = Gst.ElementFactory.make(
                "videoconvert", "video_dv_videoconvert"
        )

        self.add(self.videoconvert)

        self.dvdec = Gst.ElementFactory.make("dvdec", "dvdec")
        self.add(self.dvdec)
        self.videoscale = Gst.ElementFactory.make(
                "videoscale", "dv_videoscale"
        )
        self.add(self.videoscale)

        self.dv_src.link(self.capsfilter)
        self.capsfilter.link(self.tee)
        self.tee.link(self.queue_src)
        self.queue_src.link(self.dvdemux)

        self.dvdec.link(self.videoconvert)
        self.videoconvert.link(self.videoscale)

        self.video_pad = Gst.GhostPad.new("video_pad", self.videoscale.get_static_pad("src"))
        if (self.video_pad is None):
            Log.warning("error creating input")
        self.add_pad(self.video_pad)
        index = 1

    def on_pad_added(self, element, pad):
        name = pad.query_caps(None).to_string()

        if "video" in name:
            request_pad = self.video_queue.get_request_pad("sink%d")
            pad.link(request_pad)
            src_pad = request_pad.iterate_internal_links().next()
            src_pad.link(self.dvdec.get_static_pad("sink"))

        if "audio" in name:
            request_pad = self.video_queue.get_request_pad("sink%d")
            pad.link(request_pad)
            src_pad = request_pad.iterate_internal_links().next()
            self.audio_pad = Gst.GhostPad.new("audio_pad", src_pad)
            if (self.audio_pad is None):
                Log.warning("error creating input")
            self.add_pad(self.audio_pad)

    def config(self, dict):
        self.dv_src.set_property("channel", int(dict["channel"]))
        self.dv_src.set_property("port", int(dict["port"]))
        self.dv_src.set_property("use-avc", bool(dict["use-avc"]))
        caps = Gst.caps_from_string(
            "video/x-dv, width=%d, height=%d" % (
                int(dict["width"]), int(dict["height"])
            )
        )
        self.capsfilter.set_property("caps", caps)

        if dict["file_enabled"] == 'True':
            self.queue_save = Gst.ElementFactory.make("queue", "dv_save_queue")
            self.add(self.queue_save)
            self.filesink = Gst.ElementFactory.make("filesink", "dvfilesink")
            self.add(self.filesink)
            self.tee.link(self.queue_save)
            self.queue_save.link(self.filesink)
            self.filesink.set_property("location", dict["filename"])
