# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
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

import pygst
pygst.require("0.10")
import gst

class AudioInputBin(gst.Bin):

    def __init__(self, audio_input):
        gst.Bin.__init__(self)

        self.queue = gst.element_factory_make(
                "queue", "queue_audio"
        )
        self.add(self.queue)

        self.audioresample = audio_input.parent.create()
        self.add(self.audioresample)

        self.queue.link(self.audioresample)

        self.sink_pad = gst.GhostPad(
                "sink", self.queue.sink_pads().next()
        )
        self.src_pad = gst.GhostPad(
                "src", self.audioresample.src_pads().next()
        )
        self.add_pad(self.src_pad)
        self.add_pad(self.sink_pad)
