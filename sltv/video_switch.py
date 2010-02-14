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

class V4L2InputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)

    def new_input(self):
        return V4L2Input()

    def get_ui(self):
        return None

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)

    def new_input(self):
        return XInput()

    def get_ui(self):
        return None

class TestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)

    def new_input(self):
        return TestInput()

    def get_ui(self):
        return None


class VideoSwitch:

    def __init__(self, window):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/video_switch.ui")
        self.dialog = self.interface.get_object("switch_dialog")
        self.dialog.set_transient_for(window)

        #input selection
        file_radiobutton = self.interface.get_object("file_radiobutton")
        v4l2_radiobutton = self.interface.get_object("v4l2_radiobutton")
        test_radiobutton = self.interface.get_object("test_radiobutton")
        ximagesrc_radiobutton = self.interface.get_object(
            "ximagesrc_radiobutton"
        )
        input_action_group = gtk.ActionGroup("input_action_group")

        input_action_entries = [
            ("v4l2_action", None, "V4L2 + ALSA", None, "Input to v4l2", 0),
            ("file_action", None, "File", None, "Input to file", 1),
            ("test_action", None, "Test", None, "Test", 2),
            ("ximagesrc_action", None, "ximagesrc", None, "ximagesrc", 3)
        ]

        input_action_group.add_radio_actions(
            input_action_entries, 0, self.input_changed, None
        )

        v4l2_action = input_action_group.get_action("v4l2_action")
        v4l2_action.connect_proxy(v4l2_radiobutton)

        file_action = input_action_group.get_action("file_action")
        file_action.connect_proxy(file_radiobutton)

        test_action = input_action_group.get_action("test_action")
        test_action.connect_proxy(test_radiobutton)

        ximagesrc_action = input_action_group.get_action("ximagesrc_action")
        ximagesrc_action.connect_proxy(ximagesrc_radiobutton)

        data = ""

        close_button = self.interface.get_object("close_button")
        close_button.connect("pressed", self.close_dialog, data)
        self.dialog.connect("delete_event", self.close_dialog)

        self.input_box = self.interface.get_object("input_box")
        self.config_box = None

        self.factories = {}
        self.factories['test_action'] =  TestInputFactory()
        self.factories['ximagesrc_action'] = XInputFactory()
        self.factories['v4l2_action'] = V4L2InputFactory()
        self.factories['file_action'] = FileInputFactory()

        self.factory = self.factories['v4l2_action']

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def close_dialog(self, button, data):
        self.dialog.hide_all()

    def input_changed(self, radioaction, current):
        self.factory = self.factories[current.get_name()]
        if self.config_box:
            self.input_box.remove(self.config_box)
        self.config_box = self.factory.get_ui()
        if self.config_box:
            self.input_box.add(self.config_box)

    def new_input(self):
        return self.factory.new_input()
