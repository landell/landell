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


import gobject
import gtk

class PreviewArea(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)

    def connect(self, preview):
        self.preview = preview
        if not self.preview is None:
            self.preview.connect(
                    "prepare-xwindow-id", self.on_prepare_xwindow_id
            )

    def on_prepare_xwindow_id(self, preview, element):
        # Setting preview to be displayed at preview_area
        gtk.gdk.threads_enter()
        element.set_xwindow_id(self.window.xid)
        gtk.gdk.threads_leave()
