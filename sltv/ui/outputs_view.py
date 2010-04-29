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

class OutputsView(gtk.VBox):

    def __init__(self, sltv, outputs):
        gtk.VBox.__init__(self)
        self.sltv = sltv
        self.outputs = outputs
        self.model = self.outputs.get_store()

        self.outputs.connect("add-item", self._add_output)
        self.outputs.connect("remove-item", self._remove_output)

        self._create_items()

    def _create_items(self):
        for row in self.model:
            (name, source) = row
            self._add_item(name)

    def _add_item(self, name):
        output_item = OutputItem(name)
        self.pack_start(output_item.get_widget(), False, False)

    def _add_output(self, medialist, name, item):
        self._add_item(name)

    def _remove_output(self, medialist, name, item):
        self.foreach(self._remove_output_item)
        self._create_items()

    def _remove_output_item(self, widget):
        self.remove(widget)


class OutputItem:

    def __init__(self, name):
        self.name = name

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output.ui")

        self.widget = self.interface.get_object("output_box")
        self.label = self.interface.get_object("output_label")

        self.set_label(self.name)

    def set_label(self, label):
        self.label.set_text(label)

    def get_widget(self):
        return self.widget
