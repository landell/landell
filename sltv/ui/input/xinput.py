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

import gobject
import gtk
from settings import UI_DIR
from core import InputUI

class XInputUI(InputUI):
    def __init__(self):
        InputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/input/xinput.ui")
        self.vbox = self.interface.get_object("x_vbox")
        self.framerate_entry = self.interface.get_object("framerate_entry")

    def get_widget(self):
        return self.vbox

    def get_name(self):
        return "XImageSrc"

    def get_description(self):
        return "Get Video from Desktop and Audio from ALSA"

    def update_config(self):
        self.framerate_entry.set_text(self.config["framerate"])

    def get_config(self):
        self.config["framerate"] = self.framerate_entry.get_text()
        return self.config
