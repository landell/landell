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


import gobject
import pygst
pygst.require("0.10")
import gst

class Volume(gst.Bin):

    __gproperties__ = {
            'volume' : (gobject.TYPE_FLOAT,               # type
                        'volume',                         # nick name
                        'volume',                         # description
                        0,                                # minimum value
                        10,                               # maximum value
                        1,                                # default value
                        gobject.PARAM_READWRITE)          # flags
    }

    def __init__(self):
        gst.Bin.__init__(self)

        self.volume_convert1 = gst.element_factory_make(
                "audioconvert", "volume_convert1"
        )
        self.add(self.volume_convert1)
        self.volume_convert2 = gst.element_factory_make(
                "audioconvert", "volume_convert2"
        )
        self.add(self.volume_convert2)
        self.volume = gst.element_factory_make("volume", "volume")
        self.add(self.volume)
        self.volume_convert1.link(self.volume)
        self.volume.link(self.volume_convert2)

        self.sink_pad = gst.GhostPad(
                "sink", self.volume_convert1.sink_pads().next()
        )
        self.add_pad(self.sink_pad)
        self.src_pad = gst.GhostPad(
                "src", self.volume_convert2.src_pads().next()
        )
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

gobject.type_register(Volume)
