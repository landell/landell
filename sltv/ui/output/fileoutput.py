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
from sltv.settings import UI_DIR
from core import OutputUI

class FileOutputUI(OutputUI):
    def __init__(self):
        OutputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/output/fileoutput.ui")
        self.button = self.interface.get_object("filechooserbutton1")
        self.button.set_local_only(True)
        self.button.connect("file_set", self.set_filename)
        self.vbox = self.interface.get_object("file_vbox")
        self.config["location"] = "default.ogg"

    def set_filename(self, button):
        self.config["location"] = button.get_filename()

    def update_config(self):
        self.button.set_filename(self.config["location"])

    def get_widget(self):
        return self.vbox

    def get_name(self):
        return "File"

    def get_description(self):
        return "Output video to file"
