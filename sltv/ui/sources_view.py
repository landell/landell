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

import gtk
from sltv.settings import UI_DIR
from sltv.sltv import *
from sltv.input.core import INPUT_TYPE_VIDEO, INPUT_TYPE_AUDIO
import sources as video_model

A_BUTTON = "A"
B_BUTTON = "B"

class SourcesView(gtk.VBox):

    def __init__(self, sltv, sources):
        gtk.VBox.__init__(self)
        self.sltv = sltv
        self.sources = sources
        self.model = video_model.VideoModel(self.sources).model

        self.a_group = None
        self.b_group = None

        self.sources.connect("add-item", self._add_source)
        self.sources.connect("remove-item", self._remove_source)

        self._create_items()

    def _create_items(self):
        self.a_group = gtk.ActionGroup("a_group")
        self.b_group = gtk.ActionGroup("b_group")
        for row in self.model:
            (name, source) = row
            self._add_item(name)

    def _add_item(self, name):
        source_item = SourceItem(self.sltv, name, self.a_group, self.b_group)
        self.pack_start(source_item.get_widget(), False, False)

    def has_item_a_selected(self):
        for action in self.a_group.list_actions():
            if action.get_active():
              return True
        return False

    def _add_source(self, medialist, name, item):
        type = item.factory.get_capabilities()
        if item != None and type & INPUT_TYPE_VIDEO > 0:
            self._add_item(name)

    def _remove_source(self, medialist, name, item):
        type = item.factory.get_capabilities()
        if item != None and type & INPUT_TYPE_VIDEO > 0:
            self.foreach(self._remove_source_item)
            self._create_items()

    def _remove_source_item(self, widget):
        self.remove(widget)

class SourceItem:

    def __init__(self, sltv, name, a_group, b_group):
        self.sltv = sltv

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/source.ui")

        self.a_group = a_group
        self.b_group = b_group

        self.widget = self.interface.get_object("source_box")
        self.label = self.interface.get_object("source_label")
        self.a_button = self.interface.get_object("a_toolbutton")
        self.b_button = self.interface.get_object("b_toolbutton")

        self.name = name
        self._create_actions()

    def _create_actions(self):
        self._create_action(self.a_group, A_BUTTON)
        self._create_action(self.b_group, B_BUTTON)
        self.set_label(self.name)

    def _create_action(self, group, type):
        action = [(self.name, "gtk-missing-image", type, None),]
        group.add_toggle_actions(action)
        radioaction = group.get_action(self.name)
        if type == A_BUTTON:
            radioaction.connect_proxy(self.a_button)
            radioaction.connect("toggled", self._on_a_press)
        if type == B_BUTTON:
            radioaction.connect_proxy(self.b_button)
            radioaction.connect("toggled", self._on_b_press)

    def _on_a_press(self, event):
        if event.get_active():
            self.sltv.set_video_source(self.name)
            for action in self.a_group.list_actions():
                if action != event:
                    action.set_active(False)

    def _on_b_press(self, event):
        if event.get_active():
            for action in self.b_group.list_actions():
                if action != event:
                    action.set_active(False)

    def set_label(self, label):
        self.label.set_text(label)

    def get_widget(self):
        self.widget.show_all()
        return self.widget
