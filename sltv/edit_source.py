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
from settings import UI_DIR
from factory import *
from registry import *

class EditSource:
    def __init__(self, window, sources):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/edit_source.ui")
        self.dialog = self.interface.get_object("edit_source_dialog")
        self.dialog.set_transient_for(window)
        self.elements_combobox = self.interface.get_object("elements_combobox")
        close_button = self.interface.get_object("close_button")
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

        self.elements_liststore = gtk.ListStore(str)
        self.elements_combobox.set_model(self.elements_liststore)
        cell = gtk.CellRendererText()
        self.elements_combobox.pack_start(cell, True)
        self.elements_combobox.add_attribute(cell, "text", 0)
        self.name_entry = self.interface.get_object("name_entry")
        self.input_box = self.interface.get_object("input_box")

        self.registry = Registry()
        factories = self.registry.get_factories()
        self.factories = {}

        for factory in factories:
            self.elements_liststore.append((factory.get_name(),))
            self.factories[factory.get_name()] = factory

        self.elements_combobox.set_active(0)
        self.elements_combobox.connect("changed", self.on_change_element)
        self.config_box = None
        self.sources = sources

        self.set_factory(factories[0])

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def close_dialog(self, widget, data= None):
        self.save()
        self.dialog.hide_all()

    def save(self):
        name = self.name_entry.get_text()
        source = self.factory
        self.sources.add_source(name, source)

    def set_factory(self, factory):
        self.factory = factory
        if self.config_box:
            self.input_box.remove(self.config_box)
        self.config_box = self.factory.get_ui()
        if self.config_box:
            self.input_box.add(self.config_box)

    def on_change_element(self, button):
        selection = self.elements_combobox.get_active_text()
        self.set_factory(self.factories[selection])
