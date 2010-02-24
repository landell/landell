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

import gobject
import pygst
pygst.require("0.10")
import gst
from input import *

class TestInput(Input):

    def __init__(self):
        Input.__init__(self)
        self.audio_src = gst.element_factory_make("audiotestsrc", "audio_src")
        self.video_src = gst.element_factory_make("videotestsrc", "video_src")
        self.video_src.set_property("is-live", True)
        self.audio_src.set_property("is-live", True)
        self.add(self.audio_src)
        self.add(self.video_src)
        self.audio_pad.set_target(self.audio_src.src_pads().next())
        self.video_pad.set_target(self.video_src.src_pads().next())

    def config(self, dict):
        self.video_src.set_property("pattern", int(dict["pattern"]))
