# -*- coding: utf-8 -*-
# Copyright (C) 2009 Holoscópio Tecnologia
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

class Preview(Gst.Bin):

    __gsignals__ = {
        "prepare-window-handle" : (
            GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE,
            (GObject.type_from_name("GstElement"),)
        )
    }

    def __init__(self, sltv):
        GObject.GObject.__init__(self)
        sltv.connect("sync-message", self.on_sync_message)
        self.sink = Gst.ElementFactory.make("autovideosink", "sink")
        self.add(self.sink)
        self.videoconvert = Gst.ElementFactory.make(
            "videoconvert", "videoconvert"
        )
        self.add(self.videoconvert)
        self.videoscale = Gst.ElementFactory.make("videoscale")
        self.add(self.videoscale)
        self.videoconvert.link(self.videoscale)
        self.videoscale.link(self.sink)
        sink_pad = Gst.GhostPad.new(
            "sink_ghost_pad", self.videoconvert.sink_pads().next()
        )
        self.add_pad(sink_pad)

    def on_sync_message(self, sltv, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-window-handle":
            previewsink = message.src
            if previewsink.get_parent() == self.sink:
                previewsink.set_property("sync", False)
                previewsink.set_property("force-aspect-ratio", True)
                self.emit("prepare-window-handle", previewsink)

GObject.type_register(Preview)
