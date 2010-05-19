# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Copyright (C) 2010 Gustavo Noronha Silva <gns@gnome.org>
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

from core import Encoder
from sltv.input.core import INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

class VP8Encoder(Encoder):

    def __init__(self, type):
        Encoder.__init__(self, type)
        self.mux = gst.element_factory_make("oggmux", "oggmux")
        self.add(self.mux)
        self.vp8enc = None
        self.vorbisenc = None

        if type & INPUT_TYPE_AUDIO:
            audioconvert = gst.element_factory_make(
                "audioconvert", "audioconvert"
            )
            self.add(audioconvert)
            self.vorbisenc = gst.element_factory_make("vorbisenc", "vorbisenc")
            self.add(self.vorbisenc)
            queue_audio = gst.element_factory_make(
                    "queue", "queue_audio_enc"
            )
            self.add(queue_audio)
            gst.element_link_many(
                    audioconvert, self.vorbisenc, queue_audio, self.mux
            )
            self.audio_pad.set_target(audioconvert.sink_pads().next())
        if type & INPUT_TYPE_VIDEO:
            self.vp8enc = gst.element_factory_make("vp8enc", "vp8enc")
            self.add(self.vp8enc)
            queue_video = gst.element_factory_make(
                    "queue", "queue_video_enc"
            )
            self.add(queue_video)
            gst.element_link_many(self.vp8enc, queue_video, self.mux)
            self.video_pad.set_target(self.vp8enc.sink_pads().next())

        self.source_pad.set_target(self.mux.src_pads().next())


    def config(self, dict):
        """NotImplemented"""
        pass
