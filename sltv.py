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

class Sltv:

	def __init__(self):
		self.state = "stopped"
		self.interface = gtk.Builder()
		self.interface.add_from_file("sltv.ui")
		window = self.interface.get_object("window1")
		window.show_all()

		file_location_entry = self.interface.get_object("file_location_entry")
		play_button = self.interface.get_object("play_button")
		stop_button = self.interface.get_object("stop_button")
		stop_button.set_active(True)
		overlay_button = self.interface.get_object("overlay_button")

		play_button.connect("toggled", self.on_play_press)
		stop_button.connect("toggled", self.on_stop_press)
		overlay_button.connect("pressed", self.on_overlay_change)
		window.connect("delete_event", self.on_window_closed)

	def on_play_press(self, event):
		if (self.state == "stopped"):
			stop_button = self.interface.get_object("stop_button")
			stop_button.set_active(False)
			self.state = "playing"
			overlay_textview = self.interface.get_object("overlay_textview")
			overlay_buffer = overlay_textview.get_buffer()
			overlay_text = overlay_buffer.get_text(overlay_buffer.get_start_iter(),
					overlay_buffer.get_end_iter(),
					True)


			self.player = gst.Pipeline("player")
			self.source = gst.element_factory_make("v4l2src", "source")
			self.overlay = gst.element_factory_make("textoverlay", "overlay")
			self.sink = gst.element_factory_make("xvimagesink", "sink")
			self.player.add(self.source, self.overlay, self.sink)
			gst.element_link_many(self.source, self.overlay, self.sink)

			self.overlay.set_property("text", overlay_text)

			self.player.set_state(gst.STATE_PLAYING)
	
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.connect("message", self.on_message)

	def on_stop_press(self, event):
		if (self.state == "playing"):
			self.player.set_state(gst.STATE_NULL)
			play_button = self.interface.get_object("play_button")
			play_button.set_active(False)
			self.state = "stopped"

	def on_window_closed(self, event, data):
		loop.quit()

	def on_overlay_change(self, event):
		overlay_textview = self.interface.get_object("overlay_textview")
		overlay_buffer = overlay_textview.get_buffer()
		overlay_text = overlay_buffer.get_text(overlay_buffer.get_start_iter(),
				overlay_buffer.get_end_iter(),
				True)
		self.overlay.set_property("text", overlay_text)

	def on_message(self, bus, message):
		t = message.type 
		if t == gst.MESSAGE_EOS: 
			self.player.set_state(gst.STATE_NULL) 
		elif t == gst.MESSAGE_ERROR: 
			self.player.set_state(gst.STATE_NULL) 

Sltv()
loop = gobject.MainLoop()
loop.run()
