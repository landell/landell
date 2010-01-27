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
#import pygst
#pygst.require("0.10")
#import gst
import gtk

class Output:
	
	def __init__(self):
		self.interface = gtk.Builder()
		self.interface.add_from_file("output.ui")
		dialog = self.interface.get_object("dialog1")
		dialog.show_all()

		#Encoding selection
		dv_radiobutton = self.interface.get_object("dv_radiobutton")
		encoding_selection_group = dv_radiobutton.get_group()
		#encoding_action_group = gtk.ActionGroup()
		self.encoding_selection = "theora"
		for radiobutton in encoding_selection_group:
			radiobutton.connect("toggled", self.encoding_changed)

		#Output selection
		file_radiobutton = self.interface.get_object("file_radiobutton")
		output_selection_group = file_radiobutton.get_group()
		self.output_selection = "file"
		for radiobutton in output_selection_group:
			radiobutton.connect("toggled", self.output_changed)

		data = ""
		close_button = self.interface.get_object("close_button")
		close_button.connect("pressed", self.close_dialog, data)
		dialog.connect("delete_event", self.close_dialog)

	def close_dialog(self, button, data):
		dialog = self.interface.get_object("dialog1")
		dialog.hide_all()

	def encoding_changed(self, button):
		if (button.get_active()):
			self.encoding_selection = "blabla"

	def output_changed(self, button):
		if (button.get_active()):
			self.output_selection = "blabla"

