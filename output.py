# -*- coding: utf-8 -*-
# Copyright (C) 2009 Holoscopio Tecnologia
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

class Output:

    def __init__(self, window):
        self.interface = gtk.Builder()
        self.interface.add_from_file("output.ui")
        self.dialog = self.interface.get_object("dialog1")
        self.dialog.set_transient_for(window)

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
        self.filename = "default.ogg"

        data = ""

        close_button = self.interface.get_object("close_button")
        file_chooser_button = self.interface.get_object("filechooserbutton1")
        file_chooser_button.set_local_only(True)
        close_button.connect("pressed", self.close_dialog, data)
        file_chooser_button.connect("file_set", self.file_set)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def get_output(self):
        if self.output_selection == "file":
            self.sink = gst.element_factory_make("filesink", "filesink")
            self.sink.set_property("location", self.filename);
        if self.output_selection == "icecast":
            self.sink = gst.element_factory_make("shout2send", "icecastsink")
            server_entry = self.interface.get_object("server_entry")
            user_entry = self.interface.get_object("user_entry")
            port_spinbutton = self.interface.get_object("port_spinbutton")
            password_entry = self.interface.get_object("password_entry")
            mount_point_entry = self.interface.get_object("mount_point_entry")
            self.ip = server_entry.get_text()
            self.username = user_entry.get_text()
            self.password = password_entry.get_text()
            self.port = port_spinbutton.get_value_as_int()
            self.mount_point = mount_point_entry.get_text()
            self.sink.set_property("ip", self.ip)
            self.sink.set_property("username", self.username)
            self.sink.set_property("password", self.password)
            self.sink.set_property("port", self.port)
            self.sink.set_property("mount", self.mount_point)
        if self.output_selection == "fakesink":
            self.sink = gst.element_factory_make("fakesink", "filesink")
        return self.sink

    def file_set(self, button):
        self.filename = button.get_filename()

    def close_dialog(self, button, data):
        self.dialog.hide_all()

    def output_changed(self, radioaction, current):
        if current.get_name() == "file_action":
            self.file_out()
        if current.get_name() == "icecast_action":
            self.icecast_out()

        if current.get_name() == "fakesink_action":
            self.fakesink_out()

    def icecast_out(self):
        print "Icecast"
        notebook = self.interface.get_object("notebook1")
        notebook.set_current_page(1)
        self.output_selection = "icecast"

    def file_out(self):
        print "File"
        notebook = self.interface.get_object("notebook1")
        notebook.set_current_page(0)
        self.output_selection = "file"

    def fakesink_out(self):
        print "fakesink"
        notebook = self.interface.get_object("notebook1")
        notebook.set_current_page(2)
        self.output_selection = "fakesink"
