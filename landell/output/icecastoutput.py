# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
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
from core import Output

class IcecastOutput(Output):

    def __init__(self):
        Output.__init__(self)
        self.icecast_sink = Gst.ElementFactory.make(
                "shout2send", "icecastsink"
        )
        self.add(self.icecast_sink)
        self.sink_pad.set_target(self.icecast_sink.get_static_pad("sink"))

    def config(self, dict):
        self.icecast_sink.set_property("ip", dict["ip"])
        self.icecast_sink.set_property("username", dict["username"])
        self.icecast_sink.set_property("password", dict["password"])
        self.icecast_sink.set_property("port", int(dict["port"]))
        self.icecast_sink.set_property("mount", dict["mount"])
