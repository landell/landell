# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
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
from core import Input, INPUT_TYPE_AUDIO
from landell.log import Log

CAPABILITIES = INPUT_TYPE_AUDIO

class AudioTestInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.audio_src = Gst.ElementFactory.make("audiotestsrc", "audio_src")
        self.audio_src.set_property("is-live", True)
        self.add(self.audio_src)
        pad = self.audio_src.get_static_pad("src")
        self.audio_pad = Gst.GhostPad.new("audio_pad", pad)
        if (self.audio_pad is None):
            Log.warning("error creating input")
        self.add_pad(self.audio_pad)

    def config(self, dict):
        pass
