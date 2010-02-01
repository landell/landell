#!/usr/bin/python

# Copyright (C) 2009 Holoscopio Tecnologia
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
import pygst
pygst.require("0.10")
import gst
import gtk

class Preview:

	def __init__(self, widget):
		self.window_id = widget.window.xid

	def set_display(self):

		#Setting preview to be displayed at preview_area

		self.preview.set_xwindow_id(self.window_id)

	def get_preview(self):
		self.preview = gst.element_factory_make("xvimagesink", "preview")
		self.set_display()
		return self.preview

	def get_alternative_preview(self):
		self.preview = gst.Bin()
		sink = gst.element_factory_make("ximagesink", "sink")
		colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
		self.preview.add(colorspace, sink)
		sink_pad = gst.GhostPad("sink_ghost_pad", self.preview.find_unlinked_pad(gst.PAD_SINK))
		self.preview.add_pad(sink_pad)
		self.set_display()
		return self.preview
