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
from previewarea import PreviewArea

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

        self.source_items = []

        self._create_items()

    def _create_items(self):
        self.a_group = gtk.ActionGroup("a_group")
        self.b_group = gtk.ActionGroup("b_group")
        for row in self.model:
            (name, source) = row
            self._add_item(name)

    def _add_item(self, name):
        source_item = SourceItem(self.sltv, name, self.a_group, self.b_group)
        self.source_items.append(source_item)
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
            for source_item in self.source_items:
                source_item.source_destroy()
                self.source_items.remove(source_item)
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

        self.preview_frame = self.interface.get_object("preview_frame")
        self.preview_area = PreviewArea()
        self.preview_area.show()
        self.preview_frame.add(self.preview_area)

        self.sltv.connect("pipeline-ready", self._on_pipeline_ready)

    def source_destroy(self):
        self.sltv.disconnect_by_func(self._on_pipeline_ready)

    def _on_pipeline_ready(self, sltv):
        thumbnail = self.sltv.get_thumbnail(self.name)
        self.preview_area.connect(thumbnail)

    def _create_actions(self):
        self._create_action_a(self.a_group, A_BUTTON)
        self._create_action_b(self.b_group, B_BUTTON)
        self.set_label(self.name)

    def _create_action_b(self, group, type):
        action = [(self.name, None, type, None),]
        group.add_toggle_actions(action)
        radioaction = group.get_action(self.name)
        if type == B_BUTTON:
            radioaction.connect_proxy(self.b_button)
            radioaction.connect("toggled", self._on_b_press)

    def _create_action_a(self, group, type):
        actions = group.list_actions()
        if actions:
            radioaction = gtk.RadioAction(
                    self.name, "A", type, None, len(actions)
            )
            radioaction.set_group(actions[0])
        else:
            radioaction = gtk.RadioAction(self.name, "A", type, None, 0)
            radioaction.activate()
            self.sltv.set_video_source(self.name)
        group.add_action(radioaction)
        if type == A_BUTTON:
            radioaction.connect_proxy(self.a_button)
            radioaction.connect("changed", self._on_a_press)

    def _on_a_press(self, radioaction, current):
        if radioaction.get_active():
            self.sltv.set_video_source(self.name)

    def _on_b_press(self, event):
        if event.get_active():
            self.sltv.set_pip_source(self.name)
            for action in self.b_group.list_actions():
                if action != event:
                    action.set_active(False)
        else:
            active = False
            for action in self.b_group.list_actions():
                if action.get_active():
                    active = True
            if not active:
                self.sltv.set_pip_source(None)


    def set_label(self, label):
        self.label.set_text(label)

    def get_widget(self):
        self.widget.show_all()
        return self.widget
