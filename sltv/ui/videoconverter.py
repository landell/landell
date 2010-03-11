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
import gst
import pygst
pygst.require("0.10")
from sltv.settings import UI_DIR

class VideoConverterUI:
    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/output_setting.ui")
        self.box = self.interface.get_object("setting_box")
        self.width_entry = self.interface.get_object("width_entry")
        self.height_entry = self.interface.get_object("height_entry")

        self.config = {}

    def get_widget(self):
        return self.box

    def get_description(self):
        return "Video Converter"

    def get_config(self):
        self.config["width"] = self.width_entry.get_text()
        self.config["height"] = self.height_entry.get_text()
        return self.config

    def update_config(self):
        self.width_entry.set_text(self.config["width"])
        self.height_entry.set_text(self.config["height"])

    def set_config(self, config):
        self.config = config
        self.update_config()
