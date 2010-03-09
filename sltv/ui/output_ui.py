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
import output
import sltv.registry

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
            ("File", None, "File output", None, "Output to file", 0),
            ("Icecast", None, "Icecast output", None,
                "Output to Icecast", 1),
            ("Fake", None, "fakesink output", None,
                "Output to fakesink", 2)
        ]
        output_action_group.add_radio_actions(output_action_entries,
                5, self.output_changed, None)
        file_action = output_action_group.get_action("File")
        file_action.connect_proxy(file_radiobutton)
        icecast_action = output_action_group.get_action("Icecast")
        icecast_action.connect_proxy(icecast_radiobutton)
        fakesink_action = output_action_group.get_action("Fake")
        fakesink_action.connect_proxy(fakesink_radiobutton)

        self.registry = sltv.registry.registry
        self.factories = {}
        factories = self.registry.get_factories("output")
        for factory in factories:
            self.factories[factory.get_name()] = factory

        self.set_factory(self.factories["File"])

        self.config = {}

        close_button = self.interface.get_object("close_button")
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def get_output(self):
        name = "output"
        media_item = sltv.mediaitem.MediaItem(name, self.factory)
        media_item.set_config(self.factory.get_ui().get_config())
        self.sink = media_item.create()
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
        self.set_ui(self.factory.get_ui().get_widget())
