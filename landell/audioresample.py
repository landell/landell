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

class AudioResample(Gst.Bin):

    __gproperties__ = {
            'audiorate' : (GObject.TYPE_INT,              # type
                        'audiorate',                      # nick name
                        'audiorate',                      # description
                        -1,                               # minimum value
                        2147483647,                       # maximum value
                        -1,                               # default value (not set)
                        GObject.PARAM_READWRITE)          # flags
    }

    def __init__(self):
        Gst.Bin.__init__(self)

        self.audioconvert = Gst.ElementFactory.make(
                "audioconvert", "audioconvert"
        )
        self.add(self.audioconvert)

        self.audioresample = Gst.ElementFactory.make(
                "audioresample", "audioresample"
        )
        self.add(self.audioresample)

        self.audiorate = Gst.ElementFactory.make(
                "audiorate", "audiorate"
        )
        self.add(self.audiorate)

        self.capsfilter = Gst.ElementFactory.make(
                "capsfilter", "audioresample_capsfilter"
        )
        self.add(self.capsfilter)

        self.audioconvert.link(self.audiorate)
        self.audiorate.link(self.audioresample)
        self.audioresample.link(self.capsfilter)

        self.sink_pad = Gst.GhostPad.new(
                "sink", self.audioconvert.get_static_pad("sink")
        )
        self.add_pad(self.sink_pad)
        self.src_pad = Gst.GhostPad.new(
                "src", self.capsfilter.get_static_pad("src")
        )
        self.add_pad(self.src_pad)
        self.audiorate_property = -1

    def config(self, config):
        self.set_property("audiorate", int(config["audiorate"]))

    def do_get_property(self, property):
        if property.name == "audiorate":
            return self.audiorate_property
        else:
            Log.warning('audioresample unknown property %s' % property.name)

    def do_set_property(self, property, value):
        if property.name == "audiorate":
            caps = Gst.caps_from_string(
                    "audio/x-raw, rate=%d" %(
                        value
                    )
            )
            self.capsfilter.set_property("caps", caps)
            self.audiorate_property = value
        else:
            Log.warning('audioresample unknown property %s' % property.name)

GObject.type_register(AudioResample)
