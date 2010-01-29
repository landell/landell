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


def file_out(self):
	print "File"
	notebook = self.interface.get_object("notebook1")
	notebook.prev_page()
	self.output_selection = "file"

class Output:
	
	def __init__(self):
		self.interface = gtk.Builder()
		self.interface.add_from_file("output.ui")
		dialog = self.interface.get_object("dialog1")

		#Encoding selection
		dv_radiobutton = self.interface.get_object("dv_radiobutton")
		theora_radiobutton = self.interface.get_object("theora_radiobutton")
		encoding_action_group = gtk.ActionGroup("encoding_action_group")
		action_entries = [("theora_action", None, "Ogg Theora", None, "Ogg Theora encoding", 0),
				("dv_action", None, "DV", None, "Uncompressed DV", 1)]
		encoding_action_group.add_radio_actions(action_entries,
				0, self.encoding_changed, None)
		theora_action = encoding_action_group.get_action("theora_action")
		theora_action.connect_proxy(theora_radiobutton)
		dv_action = encoding_action_group.get_action("dv_action")
		dv_action.connect_proxy(dv_radiobutton)
		self.encoding_selection = "theora"

		#Output selection
		file_radiobutton = self.interface.get_object("file_radiobutton")
		icecast_radiobutton = self.interface.get_object("icecast_radiobutton")
		output_action_group = gtk.ActionGroup("output_action_group")
		output_action_entries = [("file_action", None, "File output", None, "Output to file", 0), 
				("icecast_action", None, "Icecast output", None, "Output to Icecast", 1)]
		output_action_group.add_radio_actions(output_action_entries,
				5, self.output_changed, None)
		file_action = output_action_group.get_action("file_action")
		file_action.connect_proxy(file_radiobutton)
		icecast_action = output_action_group.get_action("icecast_action")
		icecast_action.connect_proxy(icecast_radiobutton)
		self.output_selection = "file"
		self.filename = "default.ogg"

		data = ""

		close_button = self.interface.get_object("close_button")
		file_chooser_button = self.interface.get_object("filechooserbutton1")
		file_chooser_button.set_local_only(True)
		close_button.connect("pressed", self.close_dialog, data)
		file_chooser_button.connect("file_set", self.file_set)
		dialog.connect("delete_event", self.close_dialog)

	def show_window(self):
		dialog = self.interface.get_object("dialog1")
		dialog.show_all()

	def get_output(self):
		if self.output_selection == "file":
			self.sink = gst.element_factory_make("filesink", "filesink")
			self.sink.set_property("location", self.filename);
		else:
			self.sink = gst.element_factory_make("shout2send", "icecastsink")
			server_entry = self.interface.get_object("server_entry")
			user_entry = self.interface.get_object("user_entry")
			port_spinbutton = self.interface.get_object("port_spinbutton")
			password_entry = self.interface.get_object("password_entry")
			mount_point_entry = self.interface.get_object("mount_point_entry")
			self.ip = server_entry.get_text()
			self.username = user_entry.get_text()
			self.password = password_entry.get_text()
			self.port = port_spinbutton.get_value_as_int()
			self.mount_point = mount_point_entry.get_text()
			self.sink.set_property("ip", self.ip)
			self.sink.set_property("username", self.username)
			self.sink.set_property("password", self.password)
			self.sink.set_property("port", self.port)
			self.sink.set_property("mount", self.mount_point)

		if self.encoding_selection == "theora":
			self.output = gst.Bin()
			theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
			oggmux = gst.element_factory_make("oggmux", "oggmux")
			self.output.add(theoraenc, oggmux, self.sink)
			gst.element_link_many(theoraenc, oggmux, self.sink)
			sink_pad = gst.GhostPad("sink_ghost_pad", self.output.find_unlinked_pad(gst.PAD_SINK))
			self.output.add_pad(sink_pad)
			return self.output
		if self.encoding_selection == "dv":
			print "dv"
			self.output = gst.Bin()
			dvenc = gst.element_factory_make("ffenc_dvvideo", "dvenc")
			ffmux = gst.element_factory_make("ffmux_dv", "ffmux")
			self.output.add(dvenc, ffmux, self.sink)
			gst.element_link_many(dvenc, ffmux, self.sink)
			sink_pad = gst.GhostPad("sink_ghost_pad", self.output.find_unlinked_pad(gst.PAD_SINK))
			self.output.add_pad(sink_pad)
			return self.output

	def file_set(self, button):
		self.filename = button.get_filename()

	def close_dialog(self, button, data):
		dialog = self.interface.get_object("dialog1")
		dialog.hide_all()

	def encoding_changed(self, radioaction, current):
		if current.get_name() == "theora_action":
			self.encoding_selection = "theora"
		if current.get_name() == "dv_action":
			self.encoding_selection = "dv"

	def output_changed(self, radioaction, current):
		if current.get_name() == "file_action":
			file_out(self)
		if current.get_name() == "icecast_action":
			self.icecast_out()

	def icecast_out(self):
		print "Icecast"
		notebook = self.interface.get_object("notebook1")
		notebook.next_page()
		self.output_selection = "icecast"

