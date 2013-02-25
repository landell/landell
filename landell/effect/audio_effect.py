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

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst
from core import Effect

class AudioEffect(Effect):

    def __init__(self, effect_name):
        Effect.__init__(self)
        self.convertion1 = Gst.ElementFactory.make(
                "audioconvert", "effect_audioconvert1"
        )
        self.add(self.convertion1)

        self.convertion2 = Gst.ElementFactory.make(
                "audioconvert", "effect_audioconvert2"
        )
        self.add(self.convertion2)

        self.effect_element = Gst.ElementFactory.make(effect_name, effect_name)
        self.add(self.effect_element)

        self.convertion1.link(self.effect_element)
        self.effect_element.link(self.convertion2)

        self.sink_pad.set_target(self.convertion1.get_static_pad("sink"))
        self.src_pad.set_target(self.convertion2.get_static_pad("src"))
