# -*- coding: utf-8 -*-
# Copyright (C) 2010-2011 Holoscopio Tecnologia
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
from core import Input, INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

CAPABILITIES = INPUT_TYPE_AUDIO | INPUT_TYPE_VIDEO

class HTTPInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.http_src = Gst.ElementFactory.make("souphttpsrc", "src")
        self.http_src.set_property("is-live", True)
        self.add(self.http_src)
        self.decode_bin = Gst.ElementFactory.make("decodebin", "decoder")
        self.add(self.decode_bin)
        self.decode_bin.connect("new-decoded-pad", self.on_dynamic_pad)
        self.lkv = Gst.ElementFactory.make("livekeeper", "lkv")
        self.add(self.lkv)
        self.lka = Gst.ElementFactory.make("livekeeper", "lka")
        self.add(self.lka)
        self.http_src.link(self.decode_bin)
        self.video_pad = Gst.GhostPad.new("video_pad", self.lkv.get_static_pad("src"))
        if (self.video_pad is None):
            Log.warning("error creating input")
        self.add_pad(self.video_pad)

        pad = self.lka.get_static_pad("src")
        self.audio_pad = Gst.GhostPad.new("audio_pad", pad)
        self.add_pad(self.audio_pad)
        if (self.audio_pad is None):
            Log.warning("error creating input")

    def on_dynamic_pad(self, dbin, pad, islast):
        name = pad.query_caps(None).to_string()

        if "audio" in name:
            sink = self.lka.get_static_pad("sink")
            pad.link(sink)

        if "video" in name:
            sink = self.lkv.get_static_pad("sink")
            pad.link(sink)

    def config(self, dict):
        self.http_src.set_property("location", dict["location"])
