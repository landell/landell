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
from video_switch import *
from swap import *

def show_output(menuitem, output):
	output.show_window()

def show_encoding(menuitem, encoding):
	encoding.show_window()

def show_video_switch(menuitem, output):
	output.show_window()

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
		self.video_switch = VideoSwitch(window)

		file_location_entry = self.interface.get_object("file_location_entry")
		play_button = self.interface.get_object("play_button")
		stop_button = self.interface.get_object("stop_button")
		stop_button.set_active(True)
		self.overlay_button = self.interface.get_object("overlay_button")
		output_menuitem = self.interface.get_object("output_menuitem")
		encoding_menuitem = self.interface.get_object("encoding_menuitem")
		video_switch_menuitem = self.interface.get_object("video_switch_menuitem")
		self.effect_combobox = self.interface.get_object("effect_combobox")
		create_effects_combobox(self.effect_combobox)
		self.effect_checkbutton = self.interface.get_object("effect_checkbutton")
		self.effect_label = self.interface.get_object("effect_label")
		self.set_effects(False)

		self.effect_checkbutton.connect("toggled", self.effect_toggled)
		play_button.connect("toggled", self.on_play_press)
		stop_button.connect("toggled", self.on_stop_press)
		self.overlay_button.connect("pressed", self.on_overlay_change)
		window.connect("delete_event", self.on_window_closed)
		output_menuitem.connect("activate", show_output, self.output)
		encoding_menuitem.connect("activate", show_encoding, self.encoding)
		video_switch_menuitem.connect(
		  "activate", show_video_switch, self.video_switch
		)
		self.effect_combobox.connect("changed", self.effect_changed)

	def on_play_press(self, event):
		if (self.state == "stopped"):
			stop_button = self.interface.get_object("stop_button")
			stop_button.set_active(False)
			self.state = "playing"
			self.overlay_button.set_sensitive(True)
			overlay_textview = self.interface.get_object("overlay_textview")
			overlay_buffer = overlay_textview.get_buffer()
			overlay_text = overlay_buffer.get_text (
				overlay_buffer.get_start_iter(),
				overlay_buffer.get_end_iter(),
				True
			)

			preview_area = self.interface.get_object("preview_area")
			self.preview = Preview(preview_area)

			self.player = gst.Pipeline("player")

			self.queue_video = gst.element_factory_make("queue", "queue_video")
			self.queue_audio = gst.element_factory_make("queue", "queue_audio")
			self.player.add (self.queue_video, self.queue_audio)

			self.convert = gst.element_factory_make("audioconvert", "convert")
			self.player.add (self.convert)

			self.switch_status = self.video_switch.get_status()

			if (self.switch_status == "webcam"):
				self.videosrc = gst.element_factory_make ("v4l2src", "videosrc")
				self.audiosrc = self.audio.get_audiosrc ()
				self.player.add (self.videosrc, self.audiosrc)
				gst.element_link_many (self.videosrc, self.queue_video)
				gst.element_link_many (self.audiosrc, self.queue_audio)

			if (self.switch_status == "file"):
				self.filesrc = gst.element_factory_make ("filesrc", "source")
				self.filesrc.set_property ("location", self.video_switch.get_filename())
				self.decode = gst.element_factory_make ("decodebin", "decode")
				self.decode.connect ("new-decoded-pad", self.on_dynamic_pad)
				self.player.add (self.filesrc, self.decode)
				gst.element_link_many (self.filesrc, self.decode)

			self.effect = Effect.make_effect(self.effect_combobox.get_active_text())
			self.effect_name = self.effect_combobox.get_active_text()
			self.overlay = gst.element_factory_make("textoverlay", "overlay")
			self.tee = gst.element_factory_make("tee", "tee")
			queue1 = gst.element_factory_make("queue", "queue1")
			queue2 = gst.element_factory_make("queue", "queue2")
			self.mux = self.encoding.get_mux()
			self.sink = self.output.get_output()
			self.preview_element = self.preview.get_preview()
			self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspacesink")

			self.player.add (
				self.overlay, self.tee, queue1,
				self.mux, queue2, self.preview_element,
				self.sink, self.effect, self.colorspace
			)

			err = gst.element_link_many (
				self.queue_video, self.effect, self.overlay,
				self.tee, queue1, self.colorspace, self.mux, self.sink
			)
			if (err == False):
				print "Error conecting elements"

			#err = gst.element_link_many(self.tee, queue2, self.preview_element)
			if (err == False):
				print "Error conecting preview"

			gst.element_link_many (self.queue_audio, self.convert, self.mux)

			self.overlay.set_property("text", overlay_text)

			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.enable_sync_message_emission()
			bus.connect("message", self.on_message)
			bus.connect("sync-message::element", self.on_sync_message)
			self.player.set_state(gst.STATE_PLAYING)

	def on_dynamic_pad(self, dbin, pad, islast):
		print "dynamic pad called!"
		name = pad.get_caps()[0].get_name()
		print name

		if ("audio" in name):
			pad.link(self.queue_audio.get_pad("sink"))

		if ("video" in name):
			pad.link(self.queue_video.get_pad("sink"))

	def set_effects(self, state):
		self.effect_combobox.set_sensitive(state)
		self.effect_label.set_sensitive(state)
		self.effect_enabled = state

	def effect_toggled(self, checkbox):
		self.set_effects(not self.effect_enabled)

	def effect_changed(self, combobox):
		#FIXME set signal
#		new_effect = Effect.make_effect(self.effect_combobox.get_active_text())
#		Swap.swap_element(self.player, self.queue3, self.overlay, self.effect, new_effect)
#		self.effect = new_effect
		if self.player != None:
			print "Effect name is: " + self.effect_name
			Effect.change(self.effect, self.effect_name, self.effect_combobox.get_active_text())
			self.effect_name = self.effect_combobox.get_active_text()

	def on_stop_press(self, event):
		if (self.state == "playing"):
			self.player.set_state(gst.STATE_NULL)
			play_button = self.interface.get_object("play_button")
			play_button.set_active(False)
			self.state = "stopped"
			self.overlay_button.set_sensitive(False)

	def on_window_closed(self, event, data):
		gtk.main_quit()

	def on_overlay_change(self, event):
		overlay_textview = self.interface.get_object("overlay_textview")
		overlay_buffer = overlay_textview.get_buffer()
		overlay_text = overlay_buffer.get_text(
			overlay_buffer.get_start_iter(),
			overlay_buffer.get_end_iter(),
			True
		)
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
