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

import gobject
import gtk
from sltv.settings import UI_DIR
from sltv.ui.save_button import SaveButton
from core import InputUI

class DVInputUI(InputUI):
    def __init__(self):
        InputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/input/dvinput.ui")
        self.box = self.interface.get_object("dv_box")
        self.channel_entry = self.interface.get_object("channel_entry")
        self.port_entry = self.interface.get_object("port_entry")
        self.width_entry = self.interface.get_object("width_entry")
        self.height_entry = self.interface.get_object("height_entry")
        self.file_checkbutton = self.interface.get_object("file_checkbutton")
        self.file_label = self.interface.get_object("file_label")
        self.filechooserbutton = SaveButton()
        self.filechooserbutton.set_sensitive(False)
        self.box.attach(self.filechooserbutton, 1, 2, 5, 6)

        self.file_checkbutton.connect("toggled", self.file_toggle)

    def file_toggle(self, checkbutton):
        self.file_label.set_sensitive(checkbutton.get_active())
        self.filechooserbutton.set_sensitive(checkbutton.get_active())

    def get_widget(self):
        return self.box

    def get_name(self):
        return "DV Firewire"

    def get_description(self):
        return "Get video and audio from Firewire DV"

    def update_config(self):
        self.channel_entry.set_text(self.config["channel"])
        self.port_entry.set_text(self.config["port"])
        self.width_entry.set_text(self.config["width"])
        self.height_entry.set_text(self.config["height"])
        self.file_checkbutton.set_active(bool(self.config["file_enabled"]))
        #  set_filename doesn't accept null values
        if not self.config["filename"]:
            self.config["filename"] = ""
        self.filechooserbutton.set_filename(self.config["filename"])

    def get_config(self):
        self.config["channel"] = self.channel_entry.get_text()
        self.config["port"] = self.port_entry.get_text()
        self.config["width"] = self.width_entry.get_text()
        self.config["height"] = self.height_entry.get_text()
        self.config["file_enabled"] = self.file_checkbutton.get_active()
        self.config["filename"] = self.filechooserbutton.get_filename()
        return self.config
