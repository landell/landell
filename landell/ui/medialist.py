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
import gtk
from landell.settings import UI_DIR
import landell.registry

class MediaListUI:
    def __init__(self, media_list):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/medialist.ui")
        self.content_area = self.interface.get_object("content-area")
        add_button = self.interface.get_object("add_button")
        self.edit_button = self.interface.get_object("edit_button")
        self.remove_button = self.interface.get_object("remove_button")

        # Setting combobox for type to be added

        self.registry = landell.registry.registry
        self.factories = {}

        self.elements_combobox = self.interface.get_object("elements_combobox")

        self.elements_liststore = gtk.ListStore(str)
        self.elements_liststore.set_default_sort_func(lambda *args: -1)
        self.elements_liststore.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.elements_combobox.set_model(self.elements_liststore)
        cell = gtk.CellRendererText()
        self.elements_combobox.pack_start(cell, True)
        self.elements_combobox.add_attribute(cell, "text", 0)

        # Setting tree view

        self.media_list = media_list
        self.media_list_treeview = self.interface.get_object(
                "medialist_treeview"
        )

        media_liststore = self.media_list.get_store()
        media_liststore.set_default_sort_func(lambda *args: -1)
        media_liststore.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.media_list_treeview.set_model(media_liststore)
        cell = gtk.CellRendererText()
        column =  gtk.TreeViewColumn('Items', cell, text=0)
        self.media_list_treeview.append_column(column)

        selection = self.media_list_treeview.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)
        selection.connect("changed", self.on_treeview_changed)

        self.block_buttons(selection)

        add_button.connect("clicked", self.on_add_item)
        self.edit_button.connect("clicked", self.on_edit_item)
        self.remove_button.connect("clicked", self.on_remove_item)
        self.elements_combobox.connect("changed", self.on_change_element)

    def on_change_element(self, button):
        selection = self.elements_combobox.get_active_text()
        self.factory = self.factories[selection]

    def block_buttons(self, selection):
        (model, iter) = selection.get_selected()
        if iter == None or model == None:
            self.remove_button.set_sensitive(False)
            self.edit_button.set_sensitive(False)
        else:
            self.remove_button.set_sensitive(True)
            self.edit_button.set_sensitive(True)

    def on_treeview_changed(self, selection):
        self.block_buttons(selection)

    def get_widget(self):
        return self.content_area

    def on_add_item(self, button):
        self.edit_item.set_media_item(None)
        self.edit_item.set_factory(self.factory)
        self.edit_item.show_window()

    def on_edit_item(self, button):
        (model, iter) = self.media_list_treeview.get_selection().get_selected()
        if iter != None and model != None:
            name = model.get_value(iter, 0)
            media_item = self.media_list.get_item(name)
            self.edit_item.set_media_item(media_item)
            self.edit_item.show_window()

    def on_remove_item(self, button):
        (model, iter) = self.media_list_treeview.get_selection().get_selected()
        if iter != None and model != None:
            name = model.get_value(iter, 0)
            self.media_list.remove_item(name)
            self.media_list.save()
