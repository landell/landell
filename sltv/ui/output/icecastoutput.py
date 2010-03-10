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

class IcecastOutputUI(OutputUI):
    def __init__(self):
        OutputUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/output/icecastoutput.ui")

        self.server_entry = self.interface.get_object("server_entry")
        self.user_entry = self.interface.get_object("user_entry")
        self.port_spinbutton = self.interface.get_object("port_spinbutton")
        self.password_entry = self.interface.get_object("password_entry")
        self.mount_point_entry = self.interface.get_object("mount_point_entry")

        self.vbox = self.interface.get_object("icecast_vbox")
        self.config["location"] = ""

    def set_filename(self, button):
        self.config["location"] = button.get_filename()

    def get_widget(self):
        return self.vbox

    def get_name(self):
        return "Icecast"

    def get_description(self):
        return "Output video to Icecast"

    def update_config(self):
        self.server_entry.set_text(self.config["ip"])
        self.user_entry.set_text(self.config["username"])
        self.password_entry.set_text(self.config["password"])
        self.port_spinbutton.set_value_as_int(self.config["port"])
        self.mount_point_entry.set_text(self.config["mount_point"])

    def get_config(self):
        self.config["ip"] = self.server_entry.get_text()
        self.config["username"] = self.user_entry.get_text()
        self.config["password"] = self.password_entry.get_text()
        self.config["port"] = self.port_spinbutton.get_value_as_int()
        self.config["mount"] = self.mount_point_entry.get_text()
        return self.config
