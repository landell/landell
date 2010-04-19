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
from log import Log

class AudioResample(gst.Bin):

    __gproperties__ = {
            'audiorate' : (gobject.TYPE_INT,              # type
                        'audiorate',                      # nick name
                        'audiorate',                      # description
                        -1,                               # minimum value
                        2147483647,                       # maximum value
                        -1,                               # default value (not set)
                        gobject.PARAM_READWRITE)          # flags
    }

    def __init__(self):
        gst.Bin.__init__(self)

        self.audioresample = gst.element_factory_make(
                "audioresample", "audioresample"
        )
        self.add(self.audioresample)

        self.capsfilter = gst.element_factory_make(
                "capsfilter", "audioresample_capsfilter"
        )
        self.add(self.capsfilter)
        self.audioresample.link(self.capsfilter)

        self.sink_pad = gst.GhostPad(
                "sink", self.audioresample.sink_pads().next()
        )
        self.add_pad(self.sink_pad)
        self.src_pad = gst.GhostPad(
                "src", self.capsfilter.src_pads().next()
        )
        self.add_pad(self.src_pad)
        self.audiorate_property = -1

    def do_get_property(self, property):
        if property.name == "audiorate":
            return self.audiorate_property
        else:
            Log.warning('audioresample unknown property %s' % property.name)

    def do_set_property(self, property, value):
        if property.name == "audiorate":
            caps = gst.caps_from_string(
                    "audio/x-raw-int, rate=%d; audio/x-raw-float, rate=%d" %(
                        value, value
                    )
            )
            self.capsfilter.set_property("caps", caps)
            self.audiorate_property = value
        else:
            Log.warning('audioresample unknown property %s' % property.name)

gobject.type_register(AudioResample)
