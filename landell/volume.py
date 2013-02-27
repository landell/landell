# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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

class Volume(Gst.Bin):

    __gproperties__ = {
            'volume' : (GObject.TYPE_FLOAT,               # type
                        'volume',                         # nick name
                        'volume',                         # description
                        0,                                # minimum value
                        10,                               # maximum value
                        1,                                # default value
                        GObject.PARAM_READWRITE)          # flags
    }

    def __init__(self):
        Gst.Bin.__init__(self)

        self.volume_convert1 = Gst.ElementFactory.make(
                "audioconvert", "volume_convert1"
        )
        self.add(self.volume_convert1)
        self.volume_convert2 = Gst.ElementFactory.make(
                "audioconvert", "volume_convert2"
        )
        self.add(self.volume_convert2)
        self.volume = Gst.ElementFactory.make("volume", "volume")
        self.add(self.volume)
        self.volume_convert1.link(self.volume)
        self.volume.link(self.volume_convert2)

        self.sink_pad = Gst.GhostPad.new(
                "sink", self.volume_convert1.get_static_pad("sink")
        )
        self.src_pad = Gst.GhostPad.new(
                "src", self.volume_convert2.get_static_pad("src")
        )
        if (self.sink_pad is None or self.src_pad is None):
            Log.warning("error creating volume")
        self.add_pad(self.sink_pad)
        self.add_pad(self.src_pad)

    def do_get_property(self, property):
        if property.name == "volume":
            value = self.volume.get_property("volume")
            return value
        else:
            raise AttributeError, 'unknown property %s' % property.name

    def do_set_property(self, property, value):
        if property.name == "volume":
            self.volume.set_property("volume", value)
        else:
            raise AttributeError, 'unknown property %s' % property.name

GObject.type_register(Volume)
