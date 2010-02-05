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
from audio import *
from preview import *
from effects import *
from swap import *


class Sltv:

	def __init__(self, preview_area, window):
		self.state = "stopped"
		self.player = None
		self.preview = Preview(preview_area)

		self.encoding = Encoding(window)
		self.output = Output(window)
		self.audio = Audio()

		self.effect_enabled = "False"

	def show_encoding(self):
		self.encoding.show_window()

	def show_output(self):
		self.output.show_window()

	def play(self, overlay_text, effect_name):
		if self.state == "stopped":
			self.state = "playing"

			#Element creation

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
				self.effect_name = effect_name
				self.effect = Effect.make_effect(effect_name)
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

	def stop(self):
		self.player.set_state(gst.STATE_NULL)
		self.state = "stopped"

	def set_effects(self, state):
		self.effect_enabled = state

	def change_overlay(self, overlay_text):
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
