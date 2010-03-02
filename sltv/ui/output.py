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
import gtk
from sltv.settings import UI_DIR
import sltv.output

class OutputUI:

    def __init__(self, ui):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output.ui")
        self.output_box = self.interface.get_object("output_box")
        self.file_interface = gtk.Builder()
        self.file_interface.add_from_file(UI_DIR + "/output/fileoutput.ui")
        self.file_vbox = self.file_interface.get_object("file_vbox")
        self.icecast_interface = gtk.Builder()
        self.icecast_interface.add_from_file(UI_DIR + "/output/icecastoutput.ui")
        self.icecast_vbox = self.icecast_interface.get_object("icecast_vbox")
        self.dialog = self.interface.get_object("dialog1")
        self.dialog.set_transient_for(ui.main_window)
        self.config_box = None
        self.set_ui(self.file_vbox)

        #Output selection
        file_radiobutton = self.interface.get_object("file_radiobutton")
        icecast_radiobutton = self.interface.get_object("icecast_radiobutton")
        fakesink_radiobutton = self.interface.get_object("fakesink_radiobutton")
        output_action_group = gtk.ActionGroup("output_action_group")
        output_action_entries = [
            ("file_action", None, "File output", None, "Output to file", 0),
            ("icecast_action", None, "Icecast output", None,
                "Output to Icecast", 1),
            ("fakesink_action", None, "fakesink output", None,
                "Output to fakesink", 2)
        ]
        output_action_group.add_radio_actions(output_action_entries,
                5, self.output_changed, None)
        file_action = output_action_group.get_action("file_action")
        file_action.connect_proxy(file_radiobutton)
        icecast_action = output_action_group.get_action("icecast_action")
        icecast_action.connect_proxy(icecast_radiobutton)
        fakesink_action = output_action_group.get_action("fakesink_action")
        fakesink_action.connect_proxy(fakesink_radiobutton)

        self.output_selection = "file"
        self.config = {}
        self.config["location"] = "default.ogg"

        close_button = self.interface.get_object("close_button")
        file_chooser_button = self.file_interface.get_object("filechooserbutton1")
        file_chooser_button.set_local_only(True)
        close_button.connect("clicked", self.close_dialog)
        file_chooser_button.connect("file_set", self.file_set)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def get_output(self):
        if self.output_selection == "file":
            self.sink = sltv.output.fileoutput.FileOutput()
        if self.output_selection == "icecast":
            self.sink = sltv.output.icecastoutput.IcecastOutput()

            server_entry = self.icecast_interface.get_object("server_entry")
            user_entry = self.icecast_interface.get_object("user_entry")
            port_spinbutton = self.icecast_interface.get_object("port_spinbutton")
            password_entry = self.icecast_interface.get_object("password_entry")
            mount_point_entry = self.icecast_interface.get_object("mount_point_entry")
            self.config["ip"] = server_entry.get_text()
            self.config["username"] = user_entry.get_text()
            self.config["password"] = password_entry.get_text()
            self.config["port"] = port_spinbutton.get_value_as_int()
            self.config["mount"] = mount_point_entry.get_text()

        if self.output_selection == "fakesink":
            self.sink = sltv.output.fakeoutput.FakeOutput()
        self.sink.config(self.config)
        return self.sink

    def file_set(self, button):
        self.config["location"] = button.get_filename()

    def close_dialog(self, button, data = None):
        self.dialog.hide_all()

    def output_changed(self, radioaction, current):
        if current.get_name() == "file_action":
            self.file_out()
        if current.get_name() == "icecast_action":
            self.icecast_out()

        if current.get_name() == "fakesink_action":
            self.fakesink_out()

    def set_ui(self, vbox):
        if self.config_box:
            self.output_box.remove(self.config_box)
        self.config_box = vbox
        if self.config_box:
            self.output_box.add(self.config_box)

    def icecast_out(self):
        print "Icecast"
        self.set_ui(self.icecast_vbox)
        self.output_selection = "icecast"

    def file_out(self):
        print "File"
        self.set_ui(self.file_vbox)
        self.output_selection = "file"

    def fakesink_out(self):
        print "fakesink"
        self.set_ui(None)
        self.output_selection = "fakesink"