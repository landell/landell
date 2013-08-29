# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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
from gi.repository import Gtk
from output_item import OutputItem

class OutputsView(Gtk.VBox):

    def __init__(self, sltv, outputs):
        Gtk.VBox.__init__(self)
        self.sltv = sltv
        self.outputs = outputs
        self.model = self.outputs.get_store()

        self.outputs.connect("add-item", self._add_output)
        self.outputs.connect("remove-item", self._remove_output)

        self.output_items = {}
        self._create_items()
        self._add_items()

        self._on_stop()
        self.sltv.connect("playing", self._on_playing)
        self.sltv.connect("stopped", self._on_stop)

    def _create_items(self):
        for row in self.model:
            (name, source) = row
            self._create_item(name)

    def _create_item(self, name):
        output_item = OutputItem(name)
        self.output_items[name] = output_item
        self.output_items[name].connect("stopped", self._on_output_stopped)

    def _add_output(self, medialist, name, item):
        self._create_item(name)
        self.foreach(self._remove_output_item, None)
        self._add_items()

    def _remove_output(self, medialist, name, item):
        # FIXME: the Gtk GI annotation seems to be wrong; user_data
        # should have a default value of None!
        self.foreach(self._remove_output_item, None)
        self.output_items[name].disconnect_by_func(self._on_output_stopped)
        self.output_items.pop(name)
        self._add_items()

    def _add_items(self):
        for name in sorted(self.output_items.keys()):
            self.pack_start(self.output_items[name].get_widget(), False, False, 0)

    def _remove_output_item(self, widget, *args):
        self.remove(widget)

    def _on_output_stopped(self, output_item):
        if self.sltv.stop_output(output_item.name):
            output_item.set_stopped(True)

    def _on_playing(self, sltv):
        for output_item in sorted(self.output_items.values()):
            output_item.set_stopped(False)

    def _on_stop(self, sltv=None):
        for output_item in sorted(self.output_items.values()):
            output_item.set_stopped(True)
