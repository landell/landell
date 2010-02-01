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
from output import *
from encoding import *
from preview import *
from audio import *
from preview import *

def show_output(menuitem, output):
	output.show_window()

def show_encoding(menuitem, encoding):
	encoding.show_window()

class Sltv:

	def __init__(self):
		self.state = "stopped"
		self.interface = gtk.Builder()
		self.interface.add_from_file("sltv.ui")
		window = self.interface.get_object("window1")
		window.show_all()

		self.encoding = Encoding()
		self.output = Output()
		self.audio = Audio()

		file_location_entry = self.interface.get_object("file_location_entry")
		play_button = self.interface.get_object("play_button")
		stop_button = self.interface.get_object("stop_button")
		stop_button.set_active(True)
		overlay_button = self.interface.get_object("overlay_button")
		output_menuitem = self.interface.get_object("output_menuitem")
		encoding_menuitem = self.interface.get_object("encoding_menuitem")

		play_button.connect("toggled", self.on_play_press)
		stop_button.connect("toggled", self.on_stop_press)
		overlay_button.connect("pressed", self.on_overlay_change)
		window.connect("delete_event", self.on_window_closed)
		output_menuitem.connect("activate", show_output, self.output)
		encoding_menuitem.connect("activate", show_encoding, self.encoding)

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

			preview_area = self.interface.get_object("preview_area")
			preview = Preview(preview_area)

			self.player = gst.Pipeline("player")
			self.source = gst.element_factory_make("v4l2src", "source")
			self.overlay = gst.element_factory_make("textoverlay", "overlay")
			self.tee = gst.element_factory_make("tee", "tee")
			self.queue1 = gst.element_factory_make("queue", "queue1")
			self.queue2 = gst.element_factory_make("queue", "queue2")
			self.video_encoding = self.encoding.get_video_encoding()
			self.audio_encoding = self.encoding.get_audio_encoding()
			self.mux = self.encoding.get_mux()
			self.sink = self.output.get_output()
			self.preview_element = preview.get_preview()
			self.audio_src = self.audio.get_audiosrc()
			self.player.add(self.source, self.overlay, self.tee, self.queue1,
					self.video_encoding, self.mux, self.queue2, self.preview_element, self.sink)
			err = gst.element_link_many(self.source, self.overlay, self.tee, self.queue1,
					self.video_encoding, self.mux, self.sink)
			if err == False:
				print "Erro ao conectar elementos"
			err = gst.element_link_many(self.tee, self.queue2, self.preview_element)
			if err == False:
				print "Erro ao conectar preview"

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
