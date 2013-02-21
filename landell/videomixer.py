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

class PictureInPicture(Gst.Bin):

    __gproperties__ = {
            'width' : (GObject.TYPE_INT,                  # type
                        'width',                          # nick name
                        'Width of bigger video',          # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        320,                              # default value
                        GObject.PARAM_READWRITE),         # flags

            'height' : (GObject.TYPE_INT,                 # type
                        'height',                         # nick name
                        'height of bigger video',         # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        240,                              # default value
                        GObject.PARAM_READWRITE),         # flags

            'xposition' : (GObject.TYPE_INT,              # type
                        'Position X',                     # nick name
                        'PIP X coordinate',               # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        0,                                # default value
                        GObject.PARAM_READWRITE),         # flags

            'yposition' : (GObject.TYPE_INT,              # type
                        'Position Y',                     # nick name
                        'PIP Y coordinate',               # description
                        0,                                # minimum value
                        32767,                            # maximum value
                        0,                                # default value
                        GObject.PARAM_READWRITE),         # flags
            'enabled' : (GObject.TYPE_BOOLEAN,            # type
                        'status',                         # nick name
                        'Status of pip',                  # description
                        True,                             # default value
                        GObject.PARAM_READWRITE),         # flags
            'position' : (GObject.TYPE_INT,               # type
                        'position',                       # nick name
                        'Selected position',              # description
                        0,                                # minimum value
                        3,                                # maximum value
                        0,                                # default value
                        GObject.PARAM_READWRITE),         # flags
            'a-active' : (GObject.TYPE_INT,               # type
                          'Active A',                     # nick name
                          'A Pad to be active',           # description
                          0,                              # minimum value
                          32,                             # maximum value
                          0,                              # default value
                          GObject.PARAM_READWRITE),       # flags
            'b-active' : (GObject.TYPE_INT,               # type
                          'Active B',                     # nick name
                          'B Pad to be active',           # description
                          0,                              # minimum value
                          32,                             # maximum value
                          0,                              # default value
                          GObject.PARAM_READWRITE),       # flags
    }

    def __init__(self):
        Gst.Bin.__init__(self)

        self.width = 320
        self.height = 240
        self.x_position = 0
        self.y_position = 0
        self.enabled = True
        self.position = 0

        self.videomixer = Gst.ElementFactory.make("videomixer2", "videomixer")
        self.add(self.videomixer)
        self.caps = self.make_caps(self.width, self.height)

        self.csp = Gst.ElementFactory.make("videoconvert", "pip_csp")
        self.add(self.csp)

        self.A_capsfilter = []
        self.B_capsfilter = []
        self.A_pads = []
        self.B_pads = []

        self.videomixer.link(self.csp)

        src_pad = Gst.GhostPad.new("src", self.csp.src_pads().next())
        self.add_pad(src_pad)

        self.A_number = 0
        self.B_number = 0

        self.a_active = 0
        self._set_active_a(self.a_active)
        self.b_active = 0
        self._set_active_b(self.b_active)

    def get_request_pad_A(self):
        return self._create_A_input()

    def get_request_pad_B(self):
        return self._create_B_input()

    def _create_A_input(self):
        A_videoscale = Gst.ElementFactory.make(
                "videoscale", None
        )
        self.add(A_videoscale)
        A_videorate = Gst.ElementFactory.make(
                "videorate", None
        )
        self.add(A_videorate)
        A_capsfilter = Gst.ElementFactory.make(
                "capsfilter", None
        )
        self.add(A_capsfilter)
        self.A_capsfilter.append(A_capsfilter)
        A_csp = Gst.ElementFactory.make(
                "videoconvert", None
        )
        self.add(A_csp)
        A_alpha = Gst.ElementFactory.make(
                "identity", None
        )
        self.add(A_alpha)
        A_capsfilter.set_property("caps", self.caps['A'])

        A_videoscale.link(A_videorate)
        A_videorate.link(A_csp)
        A_csp.link(A_alpha)
        A_alpha.link(A_capsfilter)

        pad = self.videomixer.get_request_pad("sink_%d")
        pad.set_property("zorder",1)
        pad.set_property("xpos",0)
        pad.set_property("ypos",0)
        A_capsfilter.src_pads().next().link(pad)
        self.A_pads.append(pad)

        sink_pad = Gst.GhostPad.new(
                "sink_a_%d" % self.A_number, A_videoscale.sink_pads().next()
        )
        self.add_pad(sink_pad)
        self.A_number = self.A_number + 1
        return sink_pad

    def _create_B_input(self):
        B_videoscale = Gst.ElementFactory.make(
                "videoscale", None
        )
        self.add(B_videoscale)
        B_videorate = Gst.ElementFactory.make(
                "videorate", None
        )
        self.add(B_videorate)
        B_capsfilter = Gst.ElementFactory.make(
                "capsfilter", None
        )
        self.add(B_capsfilter)
        self.B_capsfilter.append(B_capsfilter)
        B_capsfilter.set_property("caps", self.caps['B'])
        B_csp = Gst.ElementFactory.make(
                "videoconvert", None
        )
        B_alpha = Gst.ElementFactory.make("identity", None)
        self.add(B_alpha)
        self.add(B_csp)

        B_videoscale.link(B_videorate)
        B_videorate.link(B_csp)
        B_csp.link(B_alpha)
        B_alpha.link(B_capsfilter)

        pad = self.videomixer.get_request_pad("sink_%d")
        pad.set_property("zorder", 10)
        pad.set_property("xpos",0)
        pad.set_property("ypos",0)
        B_capsfilter.src_pads().next().link(pad)
        self.B_pads.append(pad)

        sink_pad = Gst.GhostPad.new(
                "sink_b_%d" % self.B_number, B_videoscale.sink_pads().next()
        )
        self.add_pad(sink_pad)
        self.B_number = self.B_number + 1
        return sink_pad

    def make_caps(self, width, height):
        caps = {}
        inside_width = width/2
        inside_height = height/2
        resolution = ",width=" + str(inside_width) + ",height=" + str(inside_height)
        caps_string_inside = "video/x-raw" + resolution
        resolution = ",width=" + str(width) + ",height=" + str(height)
        caps_string_outside = "video/x-raw" + resolution
        caps['B'] = Gst.caps_from_string(caps_string_inside)
        caps['A'] = Gst.caps_from_string(caps_string_outside)
        return caps

    def _set_active_a(self, pad_number):
        for i, pad in enumerate(self.A_pads):
            if i == pad_number:
                pad.set_property("alpha", 1)
            else:
                pad.set_property("alpha", 0)

    def _set_active_b(self, pad_number):
        for i, pad in enumerate(self.B_pads):
            if i == pad_number:
                pad.set_property("alpha", 1)
            else:
                pad.set_property("alpha", 0)

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
        elif property.name == "position":
            return self.position
        elif property.name == "a-active":
            return self.a_active
        elif property.name == "b-active":
            return self.b_active
        else:
            Log.warning('PictureInPicture unknown property %s' % property.name)

    def _set_caps(self):
        self.caps = self.make_caps(self.width, self.height)
        for capsfilter in self.A_capsfilter:
            capsfilter.set_property("caps", self.caps['A'])
        for capsfilter in self.B_capsfilter:
            capsfilter.set_property("caps", self.caps['B'])

    def _set_B_pad_property(self, property_name, value):
        for pad in self.B_pads:
            pad.set_property(property_name, value)

    def set_selected_position(self, selected):
        self.position = selected
        if selected == 0:
            self.set_property("xposition", 0)
            self.set_property("yposition", 0)
        elif selected == 1:
            self.set_property("xposition", (self.width - self.width/2))
            self.set_property("yposition", 0)
        elif selected == 2:
            self.set_property("xposition", 0)
            self.set_property("yposition", (self.height - self.height/2))
        elif selected == 3:
            self.set_property("xposition", (self.width - self.width/2))
            self.set_property("yposition", (self.height - self.height/2))

    def do_set_property(self, property, value):
        if property.name == "width":
            self.width = value
            self._set_caps()
        elif property.name == "height":
            self.height = value
            self._set_caps()
        elif property.name == "xposition":
            self.x_position = value
            self._set_B_pad_property("xpos", self.x_position)
        elif property.name == "yposition":
            self.y_position = value
            self._set_B_pad_property("ypos", self.y_position)
        elif property.name == "enabled":
            self.enabled = value
            if self.enabled:
                self._set_B_pad_property("zorder", 10)
            else:
                self._set_B_pad_property("zorder", 0)
        elif property.name == "position":
            self.set_selected_position(value)
        elif property.name == "a-active":
            self.a_active = value
            self._set_active_a(value)
        elif property.name == "b-active":
            self.b_active = value
            self._set_active_b(value)
        else:
            Log.warning('PictureInPicture unknown property %s' % property.name)

GObject.type_register(PictureInPicture)
