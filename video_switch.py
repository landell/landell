# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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


class VideoSwitch:

	def __init__(self, window):
		self.interface = gtk.Builder()
		self.interface.add_from_file("video_switch.ui")
		self.dialog = self.interface.get_object("switch_dialog")
		self.dialog.set_transient_for(window)

		#input selection
		file_radiobutton = self.interface.get_object("file_radiobutton")
		webcam_radiobutton = self.interface.get_object("webcam_radiobutton")
		test_radiobutton = self.interface.get_object("test_radiobutton")

		input_action_group = gtk.ActionGroup("input_action_group")

		input_action_entries = [
			("webcam_action", None, "Webcam", None, "Input to webcam", 0),
			("file_action", None, "File", None, "Input to file", 1),
			("test_action", None, "Test", None, "Test", 2)
		]

		input_action_group.add_radio_actions(
			input_action_entries, 0, self.input_changed, None
		)

		webcam_action = input_action_group.get_action("webcam_action")
		webcam_action.connect_proxy(webcam_radiobutton)

		file_action = input_action_group.get_action("file_action")
		file_action.connect_proxy(file_radiobutton)

		test_action = input_action_group.get_action("test_action")
		test_action.connect_proxy(test_radiobutton)


		data = ""

		close_button = self.interface.get_object("close_button")
		file_chooser_button = self.interface.get_object("filechooserbutton1")
		file_chooser_button.set_local_only(True)
		close_button.connect("pressed", self.close_dialog, data)
		file_chooser_button.connect("file_set", self.set_filename)
		self.dialog.connect("delete_event", self.close_dialog)

		self.filename = ""
		self.status = "webcam"

	def show_window(self):
		self.dialog.show_all()
		self.dialog.run()

	def get_input(self):
		if self.input_selection == "file":
			self.sink = gst.element_factory_make("filesink", "filesink")
			self.sink.set_property("location", self.filename);
			return self.sink

	def close_dialog(self, button, data):
		self.dialog.hide_all()

	def set_filename(self, button):
		self.filename = button.get_filename()

	def get_filename(self):
		return self.filename

	def webcam_in(self):
		self.status = "webcam"
		print "webcam"
		notebook = self.interface.get_object("notebook1")
		notebook.prev_page()

	def file_in(self):
		self.status = "file"
		print "File"
		notebook = self.interface.get_object("notebook1")
		notebook.next_page()

	def test_in(self):
		self.status = "test"
		print "test"
		notebook = self.interface.get_object("notebook1")
		notebook.prev_page()

	def input_changed(self, radioaction, current):
		if current.get_name() == "file_action":
			self.file_in()

		if current.get_name() == "webcam_action":
			self.webcam_in()

		if current.get_name() == "test_action":
			self.test_in()


	def get_status(self):
		return self.status
