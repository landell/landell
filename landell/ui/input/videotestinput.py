# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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
from core import InputUI

class VideoTestInputUI(InputUI):
    def __init__(self):
        InputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/input/videotestinput.ui")
        self.box = self.interface.get_object("videotest_box")
        self.pattern_entry = self.interface.get_object("pattern_entry")
        self.width_entry = self.interface.get_object("width_entry")
        self.height_entry = self.interface.get_object("height_entry")

    def get_widget(self):
        return self.box

    def get_name(self):
        return "Video Test"

    def get_description(self):
        return "Video from test source"

    def update_config(self):
        self.pattern_entry.set_text(self.config["pattern"])
        self.width_entry.set_text(self.config["width"])
        self.height_entry.set_text(self.config["height"])

    def get_config(self):
        self.config["pattern"] = self.pattern_entry.get_text()
        self.config["width"] = self.width_entry.get_text()
        self.config["height"] = self.height_entry.get_text()
        return self.config
