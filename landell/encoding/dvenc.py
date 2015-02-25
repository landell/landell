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
from landell.log import Log

class DVEncoder(Encoder):

    def __init__(self, type):
        Encoder.__init__(self, type)
        print "dv"
        ffmux = Gst.ElementFactory.make("ffmux_dv", "ffmux")
        self.add(ffmux)
        if type & INPUT_TYPE_AUDIO:
            audioconvert = Gst.ElementFactory.make(
                "audioconvert", "audioconvert"
            )
            self.add(audioconvert)
            queue_audio = Gst.ElementFactory.make(
                    "queue", "queue_audio_enc"
            )
            self.add(queue_audio)

            audioconvert.link(queue_audio)
            queue_audio.link(ffmux)

            self.audio_pad = Gst.GhostPad.new("audio_pad", audioconvert.get_static_pad("sink"))
            if (self.audio_pad is None):
                Log.warning("error when creating dvenc")
            self.add_pad(self.audio_pad)

        if type & INPUT_TYPE_VIDEO:
            dvenc = Gst.ElementFactory.make("ffenc_dvvideo", "dvenc")
            self.add(dvenc)
            queue_video = Gst.ElementFactory.make(
                    "queue", "queue_video_enc"
            )
            self.add(queue_video)
            dvenc.link(queue_video)
            queue_video.link(ffmux)
            self.video_pad = Gst.GhostPad.new("video_pad", dvenc.get_static_pad("sink"))
            if (self.video_pad is None):
                Log.warning("error when creating dvenc")
            self.add_pad(self.video_pad)

        pad = ffmux.get_static_pad("src")
        self.source_pad = Gst.GhostPad.new("source_pad", pad)
        if (self.source_pad is None):
            Log.warning("error when creating dvenc")
        self.add_pad(self.source_pad)