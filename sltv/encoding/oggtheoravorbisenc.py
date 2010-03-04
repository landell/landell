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

import gobject
import pygst
pygst.require("0.10")
import gst

from core import Encoder
from sltv.input.core import INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

class OggTheoraVorbisEncoder(Encoder):

    def __init__(self, type):
        Encoder.__init__(self, type)
        print "oggmux"
        oggmux = gst.element_factory_make("oggmux", "oggmux")
        self.add(oggmux)
        if type & INPUT_TYPE_AUDIO:
            audioconvert = gst.element_factory_make(
                "audioconvert", "audioconvert"
            )
            self.add(audioconvert)
            vorbisenc = gst.element_factory_make("vorbisenc", "vorbisenc")
            self.add(vorbisenc)
            queue_audio = gst.element_factory_make(
                    "queue", "queue_audio_enc"
            )
            self.add(queue_audio)
            gst.element_link_many(
                    audioconvert, vorbisenc, queue_audio, oggmux
            )
            self.audio_pad.set_target(audioconvert.sink_pads().next())
        if type & INPUT_TYPE_VIDEO:
            theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
            #theoraenc.set_property("quality", 32)
            theoraenc.set_property("keyframe-force", 1)
            self.add(theoraenc)
            queue_video = gst.element_factory_make(
                    "queue", "queue_video_enc"
            )
            self.add(queue_video)
            gst.element_link_many(theoraenc, queue_video, oggmux)
            self.video_pad.set_target(theoraenc.sink_pads().next())
        oggmux.set_property("max-delay",10000000)
        oggmux.set_property("max-page-delay",10000000)
        self.source_pad.set_target(oggmux.src_pads().next())
