# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Luciana Fujii Pontello
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
from landell.log import Log
import datetime

class FileOutput(Output):

    def __init__(self):
        Output.__init__(self)
        self.file_sink = Gst.ElementFactory.make("filesink", "filesink")
        self.add(self.file_sink)
        pad = self.file_sink.get_static_pad("sink")
        self.sink_pad = Gst.GhostPad.new("sink_pad", pad)
        if (self.sink_pad is None):
            Log.warning("error creating output")
        self.add_pad(self.sink_pad)

    def config(self, dict):
        timestamp = str(datetime.datetime.now())
        self.file_sink.set_property("location", dict["location"] + timestamp)