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
from effects import *
from swap import *

def show_output(menuitem, output):
	output.show_window()

def show_encoding(menuitem, encoding):
	encoding.show_window()

def create_effects_combobox(combobox):
	liststore = gtk.ListStore(gobject.TYPE_STRING)
	combobox.set_model(liststore)
	cell = gtk.CellRendererText()
	combobox.pack_start(cell, True)
	combobox.add_attribute(cell, 'text', 0)
	for type in Effect.get_types():
		liststore.append((type,))
	combobox.set_active(0)

class Sltv:

	def __init__(self):
		self.state = "stopped"
		self.player = None
		self.interface = gtk.Builder()
		self.interface.add_from_file("sltv.ui")
		window = self.interface.get_object("window1")
		window.show_all()

		self.encoding = Encoding(window)
		self.output = Output(window)
		self.audio = Audio()

		file_location_entry = self.interface.get_object("file_location_entry")
		play_button = self.interface.get_object("play_button")
		stop_button = self.interface.get_object("stop_button")
		stop_button.set_active(True)
		overlay_button = self.interface.get_object("overlay_button")
		output_menuitem = self.interface.get_object("output_menuitem")
		encoding_menuitem = self.interface.get_object("encoding_menuitem")
		self.effect_combobox = self.interface.get_object("effect_combobox")
		create_effects_combobox(self.effect_combobox)
		self.effect_checkbutton = self.interface.get_object("effect_checkbutton")
		self.effect_label = self.interface.get_object("effect_label")
		self.set_effects(False)

		self.effect_checkbutton.connect("toggled", self.effect_toggled)
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
			self.preview = Preview(preview_area)

			self.player = gst.Pipeline("player")
			self.videosrc = gst.element_factory_make("v4l2src", "videosrc")
			self.overlay = gst.element_factory_make("textoverlay", "overlay")
			self.tee = gst.element_factory_make("tee", "tee")
			queue1 = gst.element_factory_make("queue", "queue1")
			queue2 = gst.element_factory_make("queue", "queue2")
			self.queue3 = gst.element_factory_make("queue", "queue3")
			queue4 = gst.element_factory_make("queue", "queue4")
			self.mux = self.encoding.get_mux()
			self.sink = self.output.get_output()
			self.preview_element = self.preview.get_preview()
			self.audiosrc = self.audio.get_audiosrc()
			self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspacesink")
			if self.effect_enabled:
				self.effect = Effect.make_effect(self.effect_combobox.get_active_text())
				self.effect_name = self.effect_combobox.get_active_text()
				self.player.add(self.effect)
			else:
				src_colorspace = gst.element_factory_make("ffmpegcolorspace", "src_colorspace")
				self.player.add(src_colorspace)
			self.player.add(self.videosrc, self.overlay, self.tee, queue1,
					self.queue3, self.mux, self.sink,
					self.audiosrc, queue4, self.colorspace)
			self.videosrc.link(self.queue3)
			if self.effect_enabled:
				gst.element_link_many(self.queue3, self.effect, self.overlay)
			else:
				gst.element_link_many(self.queue3, src_colorspace, self.overlay)
			#self.player.add(queue2, self.preview_element)
			err = gst.element_link_many(self.overlay, self.tee, queue1, self.colorspace, self.mux, self.sink)
			if err == False:
				print "Error conecting elements"
			#err = gst.element_link_many(self.tee, queue2, self.preview_element)
			gst.element_link_many(self.audiosrc, queue4, self.mux)
			if err == False:
				print "Error conecting preview"

			self.overlay.set_property("text", overlay_text)

			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.enable_sync_message_emission()
			bus.connect("message", self.on_message)
			bus.connect("sync-message::element", self.on_sync_message)
			self.player.set_state(gst.STATE_PLAYING)

	def set_effects(self, state):
		self.effect_combobox.set_sensitive(state)
		self.effect_label.set_sensitive(state)
		self.effect_enabled = state

	def effect_toggled(self, checkbox):
		self.set_effects(not self.effect_enabled)

	def on_stop_press(self, event):
		if (self.state == "playing"):
			self.player.set_state(gst.STATE_NULL)
			play_button = self.interface.get_object("play_button")
			play_button.set_active(False)
			self.state = "stopped"

	def on_window_closed(self, event, data):
		gtk.main_quit()

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

	def on_sync_message(self, bus, message):
		print "sync_message received"
		#import pdb; pdb.set_trace()
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			previewsink = message.src
			self.preview.set_display(previewsink)

Sltv()
gtk.gdk.threads_init()
gtk.main()
