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
import gtk
from sltv.settings import UI_DIR
import sltv.registry

class Edit:
    def __init__(self, window, media_list):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/edit.ui")
        self.dialog = self.interface.get_object("edit_dialog")
        self.dialog.set_transient_for(window)
        self.elements_combobox = self.interface.get_object("elements_combobox")

        self.elements_liststore = gtk.ListStore(str)
        self.elements_combobox.set_model(self.elements_liststore)
        cell = gtk.CellRendererText()
        self.elements_combobox.pack_start(cell, True)
        self.elements_combobox.add_attribute(cell, "text", 0)
        self.name_entry = self.interface.get_object("name_entry")
        self.container_box = self.interface.get_object("container_box")

        self.registry = sltv.registry.registry
        self.factories = {}

        self.elements_combobox.connect("changed", self.on_change_media_item)
        self.config_box = None
        self.media_list = media_list
        self.media_item = None

    def set_media_item(self, media_item):
        self.media_item = media_item
        if self.media_item:
            self.set_factory(self.media_item.factory)
            self.name_entry.set_text(self.media_item.name)
            self.media_item.factory.get_ui().set_config(media_item.get_config())

    def show_window(self):
        self.name_entry.set_sensitive(self.media_item == None)
        self.elements_combobox.set_sensitive(self.media_item == None)
        self.dialog.show_all()
        response = self.dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            self.save()
        self.dialog.hide_all()



    def _gfi_helper(self, model, path, iter):
        name = self.factory.get_name()
        if model.get_value(iter, 0) == name:
            self._factory_iter = iter
            return True
        return False

    def _get_factory_index(self):
        self._factory_iter = None
        self.elements_liststore.foreach(self._gfi_helper)
        return self._factory_iter

    def set_factory(self, factory):
        self.factory = factory
        self.elements_combobox.set_active_iter(self._get_factory_index())
        if self.config_box:
            self.container_box.remove(self.config_box)
        self.config_box = self.factory.get_ui().get_widget()
        if self.config_box:
            self.container_box.add(self.config_box)

    def on_change_media_item(self, button):
        selection = self.elements_combobox.get_active_text()
        self.set_factory(self.factories[selection])
