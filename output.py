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

class Output:
	
	def __init__(self):
		self.interface = gtk.Builder()
		self.interface.add_from_file("output.ui")
		dialog = self.interface.get_object("dialog1")
		dialog.show_all()
		self.theora_enc()

		#Encoding selection
		dv_radiobutton = self.interface.get_object("dv_radiobutton")
		theora_radiobutton = self.interface.get_object("theora_radiobutton")
		encoding_selection_group = dv_radiobutton.get_group()
		encoding_action_group = gtk.ActionGroup("encoding_action_group")
		action_entries = [("theora_action", None, "Ogg Theora", None, "Ogg Theora encoding", 0),
				("dv_action", None, "DV", None, "Uncompressed DV", 1)]
		encoding_action_group.add_radio_actions(action_entries,
				0, self.encoding_changed, None)
		theora_action = encoding_action_group.get_action("theora_action")
		theora_action.connect_proxy(theora_radiobutton)
		dv_action = encoding_action_group.get_action("dv_action")
		dv_action.connect_proxy(dv_radiobutton)

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

	def encoding_changed(self, radioaction, current):
		value = radioaction.get_current_value()
		if (value == 0): #Theora
			self.theora_enc()
		if (value == 1): #DV
			self.dv_enc()

	def theora_enc(self):
		self.output = gst.Bin()
		theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
		oggmux = gst.element_factory_make("oggmux", "oggmux")
		filesink = gst.element_factory_make("filesink", "filesink")
		self.output.add(theoraenc, oggmux, filesink)
		gst.element_link_many(theoraenc, oggmux, filesink)
		filesink.set_property("location", "output.ogg")
		sink_pad = gst.GhostPad("sink_ghost_pad", self.output.find_unlinked_pad(gst.PAD_SINK))
		self.output.add_pad(sink_pad)

	def dv_enc(self):
		#TODO: implement that

	def output_changed(self, button):
		if (button.get_active()):
			self.output_selection = "blabla"

