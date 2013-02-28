# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
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
from gi.repository import Gtk, GdkX11, GstVideo

class PreviewArea(Gtk.DrawingArea):

    def __init__(self):
        Gtk.DrawingArea.__init__(self)

    def connect(self, preview):
        self.preview = preview
        self.xid = self.get_property('window').get_xid()
        if not self.preview is None:
            self.preview.connect(
                    "prepare-window-handle", self.on_prepare_window_handle
            )

    def on_prepare_window_handle(self, preview, element):
        # Setting preview to be displayed at preview_area
        element.set_window_handle(self.xid)
