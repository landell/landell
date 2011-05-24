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

import gobject
import pygst
pygst.require("0.10")
import gst
from core import Input, INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

CAPABILITIES = INPUT_TYPE_AUDIO | INPUT_TYPE_VIDEO

class HTTPInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.http_src = gst.element_factory_make("souphttpsrc", "src")
        self.http_src.set_property("is-live", True)
        self.add(self.http_src)
        self.decode_bin = gst.element_factory_make("decodebin2", "decoder")
        self.add(self.decode_bin)
        self.decode_bin.connect("new-decoded-pad", self.on_dynamic_pad)
        gst.element_link_many(self.http_src, self.decode_bin)

    def on_dynamic_pad(self, dbin, pad, islast):
        name = pad.get_caps()[0].get_name()

        if "audio" in name:
            self.audio_pad.set_target(pad)

        if "video" in name:
            self.video_pad.set_target(pad)

    def config(self, dict):
        self.http_src.set_property("location", dict["location"])

