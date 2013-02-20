# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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
import gtk
from landell.settings import UI_DIR
from landell.ui.save_button import SaveButton
from core import InputUI

class FileInputUI(InputUI):
    def __init__(self):
        InputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/input/fileinput.ui")
        self.box = self.interface.get_object("file_box")
        self.config["location"] = ""
        self.button = SaveButton()
        self.box.attach(self.button, 1, 2, 0, 1)

    def get_config(self):
        self.config["location"] = self.button.get_filename()
        return self.config

    def update_config(self):
        self.button.set_filename(self.config["location"])

    def get_widget(self):
        return self.box

    def get_name(self):
        return "File"

    def get_description(self):
        return "Get Video from file"
