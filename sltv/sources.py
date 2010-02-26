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
from settings import UI_DIR
from edit_source import *

class Sources:
    def __init__(self, window, liststore):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/sources.ui")
        self.dialog = self.interface.get_object("sources_dialog")
        self.dialog.set_transient_for(window)
        add_button = self.interface.get_object("add_button")
        edit_button = self.interface.get_object("edit_button")
        remove_button = self.interface.get_object("remove_button")
        close_button = self.interface.get_object("close_button")

        self.sources_liststore = liststore
        self.sources_treeview = self.interface.get_object("sources_treeview")
        self.sources_treeview.set_model(self.sources_liststore)
        cell = gtk.CellRendererText()
        column =  gtk.TreeViewColumn('Sources', cell, text=0)
        self.sources_treeview.append_column(column)

        add_button.connect("clicked", self.on_add_source)
        edit_button.connect("clicked", self.on_edit_source)
        remove_button.connect("clicked", self.on_remove_source)
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def close_dialog(self, widget, data= None):
        self.dialog.hide_all()

    def on_add_source(self, button):
        edit_source = EditSource(self.dialog, self)
        edit_source.show_window()

    def on_edit_source(self, button):
        self.sources_treeview.get_selection().get_selected()

    def on_remove_source(self, button):
        (model, iter) = self.sources_treeview.get_selection().get_selected()
        model.remove(iter)

    def add_source(self, name, element):
        self.sources_liststore.append((name,element))
