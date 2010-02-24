# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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
import gtk
from settings import UI_DIR
from fileinput import *
from xinput import *
from testinput import *
from v4l2input import *
from dvinput import *

class InputFactory:
    def __init__(self):
        self.interface = gtk.Builder()
        self.config = {}
        self.id = ""
    def get_config(self):
        return self.config
    def get_id(self):
        return self.id

class FileInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "file"
        self.interface.add_from_file(UI_DIR + "/fileinput.ui")
        file_chooser_button = self.interface.get_object("filechooserbutton1")
        file_chooser_button.set_local_only(True)
        file_chooser_button.connect("file_set", self.set_filename)
        self.file_vbox = self.interface.get_object("file_vbox")
        self.config["location"] = ""

    def set_filename(self, button):
        self.config["location"] = button.get_filename()

    def get_ui(self):
        return self.file_vbox

    def new_input(self):
        input = FileInput()
        input.config(self.config)
        return input

    def get_name(self):
        return "File"

    def get_description(self):
        return "Get Video from file"

class V4L2InputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "v4l2"
        self.interface.add_from_file(UI_DIR + "/v4l2input.ui")
        self.v4l2_vbox = self.interface.get_object("v4l2_vbox")

    def new_input(self):
        input = V4L2Input()
        input.config(self.get_config())
        return input

    def get_ui(self):
        return self.v4l2_vbox

    def get_name(self):
        return "V4L2 + autoaudio"

    def get_description(self):
        return "Get Video from V4L2 and Audio from autoaudio"

    def get_config(self):
        v4l2_entry = self.interface.get_object("v4l2_entry")
        v4l2_device = v4l2_entry.get_text()
        self.config["v4l2_device"] = v4l2_device
        width_entry = self.interface.get_object("width_entry")
        width = width_entry.get_text()
        self.config["width"] = width
        height_entry = self.interface.get_object("height_entry")
        height = height_entry.get_text()
        self.config["height"] = height
        return self.config

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "x"
        self.interface.add_from_file(UI_DIR + "/xinput.ui")
        self.x_vbox = self.interface.get_object("x_vbox")

    def new_input(self):
        input = XInput()
        input.config(self.get_config())
        return input

    def get_ui(self):
        return self.x_vbox

    def get_name(self):
        return "XImageSrc"

    def get_description(self):
        return "Get Video from Desktop and Audio from ALSA"

    def get_config(self):
        framerate_entry = self.interface.get_object("framerate_entry")
        framerate = framerate_entry.get_text()
        self.config["framerate"] = framerate
        return self.config

class TestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "test"

    def new_input(self):
        return TestInput()

    def get_ui(self):
        return None

    def get_name(self):
        return "Test"

    def get_description(self):
        return "Video and Audio from test sources"

class DVInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "dv"
        self.interface.add_from_file(UI_DIR + "/dvinput.ui")
        self.dv_vbox = self.interface.get_object("dv_vbox")

    def new_input(self):
        input = DVInput()
        input.config(self.get_config())
        return input

    def get_ui(self):
        return self.dv_vbox

    def get_name(self):
        return "DV Firewire"

    def get_description(self):
        return "Get video and audio from Firewire DV"

    def get_config(self):
        channel_entry = self.interface.get_object("channel_entry")
        channel = channel_entry.get_text()
        self.config["channel"] = channel
        port_entry = self.interface.get_object("port_entry")
        port = port_entry.get_text()
        self.config["port"] = port
        width_entry = self.interface.get_object("width_entry")
        width = width_entry.get_text()
        self.config["width"] = width
        height_entry = self.interface.get_object("height_entry")
        height = height_entry.get_text()
        self.config["height"] = height

        return self.config
