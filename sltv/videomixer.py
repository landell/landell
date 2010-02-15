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

class PictureInPicture(gst.Bin):

    def __init__(self, colorspace, width, height):
        gst.Bin.__init__(self)
        self.caps = self.make_caps(colorspace, width, height)
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
                self.inside_capsfilter, self.inside_csp
        )
        gst.element_link_many(
                self.outside_videoscale, self.outside_videorate,
                self.outside_capsfilter, self.outside_csp
        )

        videomixer_sink_1 = self.videomixer.get_pad("sink_1")
        videomixer_sink_1.set_property("zorder",1)
        videomixer_sink_1.set_property("xpos",0)
        videomixer_sink_1.set_property("ypos",0)
        self.inside_csp.get_static_pad("src").link(videomixer_sink_1)

        videomixer_sink_2 = self.videomixer.get_pad("sink_2")
        videomixer_sink_2.set_property("zorder",0)
        videomixer_sink_2.set_property("xpos",0)
        videomixer_sink_2.set_property("ypos",0)
        self.outside_csp.get_static_pad("src").link(videomixer_sink_2)

        self.videomixer.link(self.csp)
        src_pad = gst.GhostPad(
                "src", self.find_unlinked_pad(gst.PAD_SRC)
        )
        sink_pad1 = gst.GhostPad(
                "sink_1", self.inside_videoscale.get_static_pad("sink")
        )
        sink_pad2 = gst.GhostPad(
                "sink_2", self.outside_videoscale.get_static_pad("sink")
        )
        self.add_pad(src_pad)
        self.add_pad(sink_pad1)
        self.add_pad(sink_pad2)

    def make_caps(self, colorspace, width, height):
        caps = {}
        inside_width = width/2
        inside_height = height/2
        resolution = ",width=" + str(inside_width) + ",height=" + str(inside_height)
        caps_string_inside = "video/x-raw-" + colorspace + resolution
        resolution = ",width=" + str(width) + ",height=" + str(height)
        caps_string_outside = "video/x-raw-" + colorspace + resolution
        caps['inside'] = gst.caps_from_string(caps_string_inside)
        print caps['inside']
        caps['outside'] = gst.caps_from_string(caps_string_outside)
        print caps['outside']
        return caps
