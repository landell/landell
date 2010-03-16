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

import gobject
import pygst
pygst.require("0.10")
import gst

class Effect(gst.Bin):

    def __init__(self):
        gst.Bin.__init__(self)

        self.effect_queue = gst.element_factory_make("queue", "effect_queue")
        self.add(self.effect_queue)

        self.src_pad = gst.ghost_pad_new_notarget("src", gst.PAD_SRC)
        self.add_pad(self.src_pad)
        self.sink_pad = gst.ghost_pad_new_notarget("sink", gst.PAD_SINK)
        self.add_pad(self.sink_pad)
