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

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst

from core import Encoder
from landell.input.core import INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO
from landell.log import Log

class VP8Encoder(Encoder):

    def __init__(self, type):
        Encoder.__init__(self, type)
        self.mux = Gst.ElementFactory.make("oggmux", "oggmux")
        self.add(self.mux)
        self.vp8enc = None
        self.vorbisenc = None

        if type & INPUT_TYPE_AUDIO:
            audioconvert = Gst.ElementFactory.make(
                "audioconvert", "audioconvert"
            )
            self.add(audioconvert)
            self.vorbisenc = Gst.ElementFactory.make("vorbisenc", "vorbisenc")
            self.add(self.vorbisenc)
            queue_audio = Gst.ElementFactory.make(
                    "queue", "queue_audio_enc"
            )
            self.add(queue_audio)
            audioconvert.link(self.vorbisenc)
            self.vorbisenc.link(queue_audio)
            queue_audio.link(self.mux)
            pad = audioconvert.get_static_pad("sink")
            self.audio_pad = Gst.GhostPad.new("audio_pad", pad)
            if (self.audio_pad is None):
                Log.warning("error when creating encoder")
            self.add_pad(self.audio_pad)

        if type & INPUT_TYPE_VIDEO:
            self.vp8enc = Gst.ElementFactory.make("vp8enc", "vp8enc")
            self.add(self.vp8enc)
            queue_video = Gst.ElementFactory.make(
                    "queue", "queue_video_enc"
            )
            self.add(queue_video)
            self.vp8enc.link(queue_video)
            queue_video.link(self.mux)
            pad = self.vp8enc.get_static_pad("sink")
            self.video_pad = Gst.GhostPad.new("video_pad", pad)
            if (self.video_pad is None):
                Log.warning("error when creating encoder")
            self.add_pad(self.video_pad)

        pad = self.mux.get_static_pad("src")
        self.source_pad = Gst.GhostPad.new("source_pad", pad)
        if (self.source_pad is None):
            Log.warning("error when creating encoder")
        self.add_pad(self.source_pad)

    def config(self, dict):
        """NotImplemented"""
        pass