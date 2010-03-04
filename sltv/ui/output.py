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

class FileOutputUI:
    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output/fileoutput.ui")
        self.vbox = self.interface.get_object("file_vbox")
        self.config = {}
        self.config["location"] = "default.ogg"
        button = self.interface.get_object("filechooserbutton1")
        button.set_local_only(True)
        button.connect("file_set", self.file_set)
    def file_set(self, button):
        self.config["location"] = button.get_filename()
    def get_widget(self):
        return self.vbox
    def get_config(self):
        return self.config
    def new_output(self):
        return sltv.output.fileoutput.FileOutput()

class FakeOutputUI:
    def __init__(self):
        self.interface = gtk.Builder()
        self.config = {}
    def get_widget(self):
        return None
    def get_config(self):
        return self.config
    def new_output(self):
        return sltv.output.fakeoutput.FakeOutput()

class IcecastOutputUI:
    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output/icecastoutput.ui")
        self.vbox = self.interface.get_object("icecast_vbox")
        self.server_entry = self.interface.get_object("server_entry")
        self.user_entry = self.interface.get_object("user_entry")
        self.port_spinbutton = self.interface.get_object("port_spinbutton")
        self.password_entry = self.interface.get_object("password_entry")
        self.mount_point_entry = self.interface.get_object("mount_point_entry")
        self.config = {}
    def get_widget(self):
        return self.vbox
    def get_config(self):
        self.config["ip"] = self.server_entry.get_text()
        self.config["username"] = self.user_entry.get_text()
        self.config["password"] = self.password_entry.get_text()
        self.config["port"] = self.port_spinbutton.get_value_as_int()
        self.config["mount"] = self.mount_point_entry.get_text()
        return self.config
    def new_output(self):
        return sltv.output.icecastoutput.IcecastOutput()


class OutputUI:

    def __init__(self, ui):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output.ui")
        self.output_box = self.interface.get_object("output_box")
        self.dialog = self.interface.get_object("dialog1")
        self.dialog.set_transient_for(ui.main_window)
        self.config_box = None

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

        self.factories = {
                        'file_action': FileOutputUI(),
                        'icecast_action': IcecastOutputUI(),
                        'fakesink_action': FakeOutputUI(),
                    }
        self.set_factory(self.factories['file_action'])

        self.config = {}

        close_button = self.interface.get_object("close_button")
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def get_output(self):
        self.sink = self.factory.new_output()
        self.sink.config(self.factory.get_config())
        return self.sink

    def close_dialog(self, button, data = None):
        self.dialog.hide_all()

    def output_changed(self, radioaction, current):
        name = current.get_name()
        self.set_factory(self.factories[name])

    def set_ui(self, vbox):
        if self.config_box:
            self.output_box.remove(self.config_box)
        self.config_box = vbox
        if self.config_box:
            self.output_box.add(self.config_box)

    def set_factory(self, factory):
        self.factory = factory
        self.set_ui(self.factory.get_widget())
