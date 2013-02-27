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
from gi.repository import Gst, GObject
from log import Log

class MulTeeQueue(Gst.Bin):

    def __init__(self):
        Gst.Bin.__init__(self)
        self.tee = Gst.ElementFactory.make("tee", "multeequeue_tee")
        self.add(self.tee)
        self.multiqueue = Gst.ElementFactory.make("multiqueue", "multiqueue")
        self.add(self.multiqueue)
        self.sink_pad = Gst.GhostPad.new("sink", self.tee.get_static_pad("sink"))
        if (self.sink_pad is None):
            Log.warning("error creating multeequeue")
        self.add_pad(self.sink_pad)
        self.pad_index = 0

    def get_src_pad(self):
        request_pad = self.multiqueue.get_request_pad("sink%d")
        self.tee.get_request_pad("src%d").link(request_pad)
        src_pad = request_pad.iterate_internal_links().next()
        src_ghost_pad = Gst.GhostPad.new(
                "src%d" % self.pad_index, src_pad
        )
        if (src_ghost_pad is None):
            Log.warning("error creating multeequeue")
        self.add_pad(src_ghost_pad)
        self.pad_index += 1
        return src_ghost_pad

GObject.type_register(MulTeeQueue)
