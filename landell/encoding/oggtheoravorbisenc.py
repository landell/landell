# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
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

from core import Encoder
from landell.input.core import INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

class OggTheoraVorbisEncoder(Encoder):

    def __init__(self, type):
        Encoder.__init__(self, type)
        self.oggmux = Gst.ElementFactory.make("oggmux", "oggmux")
        self.add(self.oggmux)
        self.theoraenc = None
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
            queue_audio.link(self.oggmux)
            self.audio_pad.set_target(audioconvert.get_static_pad("sink"))
        if type & INPUT_TYPE_VIDEO:
            self.theoraenc = Gst.ElementFactory.make("theoraenc", "theoraenc")
            self.add(self.theoraenc)
            queue_video = Gst.ElementFactory.make(
                    "queue", "queue_video_enc"
            )
            self.add(queue_video)
            self.theoraenc.link(queue_video)
            queue_video.link(self.oggmux)
            self.video_pad.set_target(self.theoraenc.get_static_pad("sink"))

        self.source_pad.set_target(self.oggmux.get_static_pad("src"))


    def config(self, dict):
        self.oggmux.set_property("max-delay", 10000000)
        self.oggmux.set_property("max-page-delay", 10000000)
        if self.theoraenc:
            self.theoraenc.set_property("quality", int(dict["theora_quality"]))
            self.theoraenc.set_property("keyframe-force", int(dict["keyframe"]))
            self.theoraenc.set_property("bitrate", int(dict["theora_bitrate"]))
        if self.vorbisenc:
            self.vorbisenc.set_property("quality", float(dict["vorbis_quality"]))
            self.vorbisenc.set_property("bitrate", int(dict["vorbis_bitrate"]))
