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

class PictureInPicture(gst.Bin):

    __gproperties__ = {
            'width' : (gobject.TYPE_INT,                  # type
                        'width',                          # nick name
                        'Width of bigger video',          # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        320,                              # default value
                        gobject.PARAM_READWRITE),         # flags

            'height' : (gobject.TYPE_INT,                 # type
                        'height',                         # nick name
                        'height of bigger video',         # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        240,                              # default value
                        gobject.PARAM_READWRITE),         # flags

            'xposition' : (gobject.TYPE_INT,              # type
                        'Position X',                     # nick name
                        'PIP X coordinate',               # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        0,                                # default value
                        gobject.PARAM_READWRITE),         # flags

            'yposition' : (gobject.TYPE_INT,              # type
                        'Position Y',                     # nick name
                        'PIP Y coordinate',               # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        0,                                # default value
                        gobject.PARAM_READWRITE),         # flags
            'enabled' : (gobject.TYPE_BOOLEAN,            # type
                        'status',                         # nick name
                        'Status of pip',                  # description
                        True,                             # default value
                        gobject.PARAM_READWRITE),         # flags
    }

    def __init__(self):
        gst.Bin.__init__(self)

        self.width = 320
        self.height = 240
        self.x_position = 0
        self.y_position = 0
        self.enabled = True

        self.caps = self.make_caps(self.width, self.height)
        self.videomixer = gst.element_factory_make("videomixer", "videomixer")
        self.add(self.videomixer)
        self.inside_videoscale = gst.element_factory_make(
                "videoscale", "inside_videoscale"
        )
        self.add(self.inside_videoscale)
        self.outside_videoscale = gst.element_factory_make(
                "videoscale", "outside_videoscale"
        )
        self.add(self.outside_videoscale)
        self.inside_videorate = gst.element_factory_make(
                "videorate", "inside_videorate"
        )
        self.add(self.inside_videorate)
        self.outside_videorate = gst.element_factory_make(
                "videorate", "outside_videorate"
        )
        self.add(self.outside_videorate)
        self.inside_capsfilter = gst.element_factory_make(
                "capsfilter", "inside_capsfilter"
        )
        self.add(self.inside_capsfilter)
        self.outside_capsfilter = gst.element_factory_make(
                "capsfilter", "outsidecapsfilter"
        )
        self.add(self.outside_capsfilter)
        self.inside_capsfilter.set_property("caps", self.caps['inside'])
        self.outside_capsfilter.set_property("caps", self.caps['outside'])

        self.inside_csp = gst.element_factory_make(
                "ffmpegcolorspace", "inside_csp"
        )
        self.add(self.inside_csp)
        self.outside_csp = gst.element_factory_make(
                "ffmpegcolorspace", "outside_csp"
        )
        self.add(self.outside_csp)
        self.csp = gst.element_factory_make("ffmpegcolorspace", "pip_csp")
        self.add(self.csp)

        gst.element_link_many(
                self.inside_videoscale, self.inside_videorate,
                self.inside_csp, self.inside_capsfilter
        )
        gst.element_link_many(
                self.outside_videoscale, self.outside_videorate,
                self.outside_csp, self.outside_capsfilter
        )

        self.videomixer_sink_1 = self.videomixer.get_pad("sink_1")
        self.videomixer_sink_1.set_property("zorder",2)
        self.videomixer_sink_1.set_property("xpos",0)
        self.videomixer_sink_1.set_property("ypos",0)
        self.inside_capsfilter.get_static_pad("src").link(
                self.videomixer_sink_1
        )

        videomixer_sink_2 = self.videomixer.get_pad("sink_2")
        videomixer_sink_2.set_property("zorder",1)
        videomixer_sink_2.set_property("xpos",0)
        videomixer_sink_2.set_property("ypos",0)
        self.outside_capsfilter.get_static_pad("src").link(videomixer_sink_2)

        self.videomixer.link(self.csp)
        src_pad = gst.GhostPad("src", self.csp.src_pads().next())
        sink_pad1 = gst.GhostPad(
                "sink_1", self.inside_videoscale.sink_pads().next()
        )
        sink_pad2 = gst.GhostPad(
                "sink_2", self.outside_videoscale.sink_pads().next()
        )
        self.add_pad(src_pad)
        self.add_pad(sink_pad1)
        self.add_pad(sink_pad2)

    def make_caps(self, width, height):
        caps = {}
        inside_width = width/2
        inside_height = height/2
        resolution = ",width=" + str(inside_width) + ",height=" + str(inside_height)
        caps_string_inside = "video/x-raw-yuv" + resolution
        resolution = ",width=" + str(width) + ",height=" + str(height)
        caps_string_outside = "video/x-raw-yuv" + resolution
        caps['inside'] = gst.caps_from_string(caps_string_inside)
        caps['outside'] = gst.caps_from_string(caps_string_outside)
        return caps

    def do_get_property(self, property):
        if property.name == "width":
            return self.width
        elif property.name == "height":
            return self.height
        elif property.name == "xposition":
            return self.x_position
        elif property.name == "yposition":
            return self.y_position
        elif property.name == "enabled":
            return self.enabled
        else:
            Log.warning('PictureInPicture unknown property %s' % property.name)

    def _set_caps(self):
        self.caps = self.make_caps(self.width, self.height)
        self.inside_capsfilter.set_property("caps", self.caps['inside'])
        self.outside_capsfilter.set_property("caps", self.caps['outside'])

    def do_set_property(self, property, value):
        if property.name == "width":
            self.width = value
            self._set_caps()
        elif property.name == "height":
            self.height = value
            self._set_caps()
        elif property.name == "xposition":
            self.x_position = value
            self.videomixer_sink_1.set_property("xpos",self.x_position)
        elif property.name == "yposition":
            self.y_position = value
            self.videomixer_sink_1.set_property("ypos",self.y_position)
        elif property.name == "enabled":
            self.enabled = value
            if self.enabled:
                self.videomixer_sink_1.set_property("zorder",2)
            else:
                self.videomixer_sink_1.set_property("zorder",0)
        else:
            Log.warning('PictureInPicture unknown property %s' % property.name)
        self.caps = self.make_caps(self.width, self.height)
        self.inside_capsfilter.set_property("caps", self.caps['inside'])
        self.outside_capsfilter.set_property("caps", self.caps['outside'])

gobject.type_register(PictureInPicture)
