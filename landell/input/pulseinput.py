# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Luciana Fujii Pontelloo <luciana@holoscopio.com>
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

CAPABILITIES = INPUT_TYPE_AUDIO

class PulseInput(Input):

    def __init__(self):
        Input.__init__(self, CAPABILITIES)
        self.audio_src = Gst.ElementFactory.make("pulsesrc", "audio_src")
        self.add(self.audio_src)
        self.audio_pad.set_target(self.audio_src.src_pads().next())

    def config(self, dict):
        pass
