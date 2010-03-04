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

from sltv.input.core import INPUT_TYPE_AUDIO, INPUT_TYPE_VIDEO

class Encoder(gst.Bin):

    def __init__(self, type):
        gst.Bin.__init__(self)
        self.source_pad = gst.ghost_pad_new_notarget("source_pad", gst.PAD_SRC)
        self.add_pad(self.source_pad)
        if (type & INPUT_TYPE_AUDIO):
            self.audio_pad = gst.ghost_pad_new_notarget("audio_pad", gst.PAD_SINK)
            self.add_pad(self.audio_pad)
        if (type & INPUT_TYPE_VIDEO):
            self.video_pad = gst.ghost_pad_new_notarget("video_pad", gst.PAD_SINK)
            self.add_pad(self.video_pad)
