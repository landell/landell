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

class Effect(Gst.Bin):

    def __init__(self):
        Gst.Bin.__init__(self)

        self.src_pad = Gst.ghost_pad_new_notarget("src", Gst.PAD_SRC)
        self.add_pad(self.src_pad)
        self.sink_pad = Gst.ghost_pad_new_notarget("sink", Gst.PAD_SINK)
        self.add_pad(self.sink_pad)
