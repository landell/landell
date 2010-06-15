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
import save_button
from sltv.settings import UI_DIR

class WaterMarkUI:

    def __init__(self, ui, sltv):
        self.ui = ui
        self.sltv = sltv

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/watermark.ui")
        self.widget = self.interface.get_object("table1")
        self.button = self.interface.get_object("filechooserbutton")
        self.adjustment = gtk.Adjustment(0.5, 0, 0.5, 0.05)
        self.scale = gtk.HScale(self.adjustment)
        self.widget.attach(self.scale, 1, 2, 1, 2)

        self.location = None
        self.sltv.set_watermark_size(0.5)
        self.widget.show_all()

        self.button.connect("file-set", self.on_file_set)
        self.scale.connect("value-changed", self.on_size_changed)

    def on_file_set(self, button):
        self.sltv.set_watermark_location(self.button.get_filename())

    def on_size_changed(self, adjustment):
        self.sltv.set_watermark_size(self.scale.get_value())

    def get_widget(self):
        return self.widget
