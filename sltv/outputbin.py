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

class OutputBin(gst.Bin):

    def __init__(self, output):
        gst.Bin.__init__(self)

        self.queue = gst.element_factory_make(
                "queue", "tee_queue"
        )
        self.add(self.queue)
        self.valve = gst.element_factory_make("valve", "valve")
        self.add(self.valve)
        self.sink = output.create()
        self.add(self.sink)
        gst.element_link_many(
                self.queue, self.valve, self.sink
        )

        self.sink_pad = gst.GhostPad(
                "sink", self.queue.sink_pads().next()
        )
        self.add_pad(self.sink_pad)

    def stop(self):
        self.valve.set_property("drop", True)
        self.sink.set_state(gst.STATE_NULL)
        self.fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.valve.unlink(self.sink)
        self.remove(self.sink)
        self.fakesink.set_state(gst.STATE_PLAYING)
        self.add(self.fakesink)
        self.valve.link(self.fakesink)
        self.valve.set_property("drop", False)
