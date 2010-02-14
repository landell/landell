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

class InputFactory:
    def __init__(self):
        self.interface = gtk.Builder()
        self.config = {}
    def get_config(self):
        return self.config

class FileInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
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

    def new_input(self):
        return V4L2Input()

    def get_ui(self):
        return None

    def get_name(self):
        return "V4L2 + ALSA"

    def get_description(self):
        return "Get Video from V4L2 and Audio from ALSA"

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)

    def new_input(self):
        return XInput()

    def get_ui(self):
        return None

    def get_name(self):
        return "XImageSrc"

    def get_description(self):
        return "Get Video from Desktop and Audio from ALSA"

class TestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)

    def new_input(self):
        return TestInput()

    def get_ui(self):
        return None

    def get_name(self):
        return "Test"

    def get_description(self):
        return "Video and Audio from test sources"


class VideoSwitch:

    def __init__(self, window):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/video_switch.ui")
        self.dialog = self.interface.get_object("switch_dialog")
        self.dialog.set_transient_for(window)

        self.factories = [TestInputFactory(), XInputFactory(), V4L2InputFactory(), FileInputFactory()]
        self.factory = self.factories[0]

        self.radio_box = self.interface.get_object("radio_box")
        self.radiogroup = None

        for factory in self.factories:
            self.radiogroup = gtk.RadioButton(self.radiogroup)
            self.radiogroup.set_label(factory.get_name())
            self.radiogroup.connect("toggled", self.input_changed, factory)
            self.radio_box.add(self.radiogroup)

        data = ""

        close_button = self.interface.get_object("close_button")
        close_button.connect("pressed", self.close_dialog, data)
        self.dialog.connect("delete_event", self.close_dialog)

        self.input_box = self.interface.get_object("input_box")
        self.config_box = None

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def close_dialog(self, button, data):
        self.dialog.hide_all()

    def input_changed(self, button, factory):
        if button.get_active():
            self.factory = factory
            if self.config_box:
                self.input_box.remove(self.config_box)
            self.config_box = self.factory.get_ui()
            if self.config_box:
                self.input_box.add(self.config_box)

    def new_input(self):
        return self.factory.new_input()
