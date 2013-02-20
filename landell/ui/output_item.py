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

import gtk
import gi
from landell.settings import UI_DIR

class OutputItem(GObject.GObject):
    __gsignals__ = {
        'stopped' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
    }


    def __init__(self, name):
        GObject.GObject.__init__(self)
        self.name = name

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output.ui")

        self.widget = self.interface.get_object("output_box")
        self.button = self.interface.get_object("output_button")
        self.label = self.interface.get_object("output_label")
        self.label.set_text(self.name)

        self.button.connect("clicked", self._on_stop_clicked)

    def _on_stop_clicked(self, button):
        self.emit("stopped")

    def get_widget(self):
        return self.widget

    def set_stopped(self, state):
        self.button.set_sensitive(not state)

GObject.type_register(OutputItem)
