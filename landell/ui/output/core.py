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
from gi.repository import Gtk
from landell.settings import UI_DIR

class OutputUI:
    def __init__(self):
        self.interface = Gtk.Builder()
        self.config = {}

        self.parent_interface = Gtk.Builder()
        self.parent_interface.add_from_file(
                UI_DIR + "/output_encoder_setting.ui"
        )
        self.parent_box = self.parent_interface.get_object("encoder_box")
        self.combobox = self.parent_interface.get_object("encoder_combobox")
        cell = Gtk.CellRendererText()
        self.combobox.pack_start(cell, True)
        self.combobox.add_attribute(cell, "text", 0)


    def get_encoder_widget(self):
        return self.parent_box

    def set_encoder_model(self, model):
        self.combobox.set_model(model)

    def get_config(self):
        self.config["parent"] = self.combobox.get_active_text()
        return self.config

    def update_config(self):
        for i, (name, encoder) in enumerate(self.combobox.get_model()):
            if name == self.config["parent"]:
                self.combobox.set_active(i)

    def set_config(self, config):
        self.config = config
        self.update_config()
