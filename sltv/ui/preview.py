# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
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
from sltv.settings import UI_DIR

class PreviewUI:

    def __init__(self, sltv):
        self.sltv = sltv
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/preview.ui")
        self.widget = self.interface.get_object("vbox")
        self.button = self.interface.get_object("preview_checkbutton")
        self.button.connect("toggled", self.toggled)
        self.preview_state = False
        sltv.set_preview(self.preview_state)
    def toggled(self, checkbox):
        self.preview_state = not self.preview_state
        self.sltv.set_preview(self.preview_state)
    def get_widget(self):
        return self.widget
