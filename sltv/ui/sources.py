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
from edit_source import *

from sltv.input.core import INPUT_TYPE_VIDEO, INPUT_TYPE_AUDIO

class VideoModel:
    def __init__(self, sources):
        self.model = sources.get_store().filter_new()
        self.model.set_visible_func(self.filter)
    def filter(self, model, iter):
        source = model.get_value(iter, 1)
        return source != None and \
            source.factory.get_capabilities() & INPUT_TYPE_VIDEO > 0

class AudioModel:
    def __init__(self, sources):
        self.model = sources.get_store().filter_new()
        self.model.set_visible_func(self.filter)
    def filter(self, model, iter):
        source = model.get_value(iter, 1)
        return source != None and \
            source.factory.get_capabilities() & INPUT_TYPE_AUDIO > 0

class Sources:
    def __init__(self, ui, sources):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/sources.ui")
        self.dialog = self.interface.get_object("sources_dialog")
        self.dialog.set_transient_for(ui.main_window)
        add_button = self.interface.get_object("add_button")
        edit_button = self.interface.get_object("edit_button")
        self.remove_button = self.interface.get_object("remove_button")
        close_button = self.interface.get_object("close_button")

        self.sources = sources
        self.sources_treeview = self.interface.get_object("sources_treeview")
        self.sources_treeview.set_model(self.sources.get_store())
        cell = gtk.CellRendererText()
        column =  gtk.TreeViewColumn('Sources', cell, text=0)
        self.sources_treeview.append_column(column)

        selection = self.sources_treeview.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)
        selection.connect("changed", self.on_treeview_changed)

        self.block_remove_button(selection)

        add_button.connect("clicked", self.on_add_source)
        edit_button.connect("clicked", self.on_edit_source)
        self.remove_button.connect("clicked", self.on_remove_source)
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

        self.edit_source = EditSource(self.dialog, self.sources)

    def block_remove_button(self, selection):
        (model, iter) = selection.get_selected()
        if iter == None or model == None:
            self.remove_button.set_sensitive(False)
        else:
            self.remove_button.set_sensitive(True)

    def on_treeview_changed(self, selection):
        self.block_remove_button(selection)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def close_dialog(self, widget, data= None):
        self.dialog.hide_all()

    def on_add_source(self, button):
        self.edit_source.set_source(None)
        self.edit_source.show_window()

    def on_edit_source(self, button):
        (model, iter) = self.sources_treeview.get_selection().get_selected()
        if iter != None and model != None:
            name = model.get_value(iter, 0)
            source = self.sources.get_source(name)
            self.edit_source.set_source(source)
            self.edit_source.show_window()

    def on_remove_source(self, button):
        (model, iter) = self.sources_treeview.get_selection().get_selected()
        if iter != None and model != None:
            name = model.get_value(iter, 0)
            self.sources.remove_source(name)
