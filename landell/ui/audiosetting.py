# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello
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

class AudioUI:
    def __init__(self):
        self.interface = Gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/audio_input.ui")
        self.config = {}
        self.box = self.interface.get_object("audio_box")
        self.audiorate_entry = self.interface.get_object("audiorate_entry")

    def get_widget(self):
        return self.box

    def get_name(self):
        return "Audio configuration"

    def get_config(self):
        self.config["audiorate"] = self.audiorate_entry.get_text()
        return self.config

    def update_config(self):
        self.audiorate_entry.set_text(self.config["audiorate"])

    def set_config(self, config):
        self.config = config
        self.update_config()
