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
import Gtk
from landell.settings import UI_DIR
import landell.registry
from edit import Edit
import landell.factory

class EditOutput(Edit):
    def __init__(self, window, outputs, encoders):
        Edit.__init__(self, window, outputs)
        label = self.interface.get_object("name_label")
        label.set_label("Output name:")
        self.dialog.set_title("Edit Output")
        self.encoders = encoders
        self.encoder_box = None

    def set_factory(self, factory):
        Edit.set_factory(self, factory)
        if self.encoder_box:
            self.container_box.remove(self.encoder_box)
        self.encoder_box = factory.get_ui().get_encoder_widget()
        self.container_box.add(self.encoder_box)
        factory.get_ui().set_encoder_model(self.encoders.liststore)
