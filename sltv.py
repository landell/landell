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
from video_switch import *
from swap import *


class Sltv:

	def __init__(self, preview_area, window):
		self.state = "stopped"
		self.player = None
		self.preview = Preview(preview_area)

		self.encoding = Encoding(window)
		self.output = Output(window)
		self.audio = Audio()
		self.video_switch = VideoSwitch(window)

		self.effect_enabled = "False"

	def show_encoding(self):
		self.encoding.show_window()

	def show_output(self):
		self.output.show_window()

	def show_video_switch(self):
		self.video_switch.show_window()

	def play(self, overlay_text, effect_name):
		if self.state == "stopped":
			self.state = "playing"

			#Element creation

			self.player = gst.Pipeline("player")

			self.queue_video = gst.element_factory_make("queue", "queue_video")
			self.queue_audio = gst.element_factory_make("queue", "queue_audio")
			self.player.add (self.queue_video, self.queue_audio)

			self.convert = gst.element_factory_make("audioconvert", "convert")
			self.player.add (self.convert)

			self.switch_status = self.video_switch.get_status()

			if (self.switch_status == "webcam"):
				self.videosrc = gst.element_factory_make ("v4l2src", "videosrc")
				self.capsfilter = gst.element_factory_make("capsfilter", "capsfilter")
				self.audiosrc = self.audio.get_audiosrc ()
				self.player.add(self.videosrc, self.capsfilter, self.audiosrc)
				gst.element_link_many(self.videosrc, self.capsfilter, self.queue_video)
				gst.element_link_many (self.audiosrc, self.queue_audio)
				caps = gst.caps_from_string("video/x-raw-yuv, width=640, height=480")
				self.capsfilter.set_property("caps", caps)

			if (self.switch_status == "file"):
				self.filesrc = gst.element_factory_make ("filesrc", "source")
				self.filesrc.set_property ("location", self.video_switch.get_filename())
				self.decode = gst.element_factory_make ("decodebin", "decode")
				self.decode.connect ("new-decoded-pad", self.on_dynamic_pad)
				self.player.add (self.filesrc, self.decode)
				gst.element_link_many (self.filesrc, self.decode)

			if (self.switch_status == "test"):
				self.videosrc = gst.element_factory_make ("videotestsrc", "videotestsrc")
				self.audiosrc = gst.element_factory_make ("audiotestsrc", "audiotestsrc")
				self.player.add (self.videosrc, self.audiosrc)
				gst.element_link_many (self.videosrc, self.queue_video)
				gst.element_link_many (self.audiosrc, self.queue_audio)

			self.overlay = gst.element_factory_make("textoverlay", "overlay")
			self.tee = gst.element_factory_make("tee", "tee")
			queue1 = gst.element_factory_make("queue", "queue1")
			queue2 = gst.element_factory_make("queue", "queue2")
			self.mux = self.encoding.get_mux()
			self.sink = self.output.get_output()
			self.preview_element = self.preview.get_preview()
			self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspacesink")

			if self.effect_enabled:
				self.effect_name = effect_name
				self.effect = Effect.make_effect(effect_name)
				self.player.add(self.effect)
			else:
				src_colorspace = gst.element_factory_make("ffmpegcolorspace", "src_colorspace")
				self.player.add(src_colorspace)

			self.player.add(self.overlay, self.tee, queue1, self.mux, self.sink, self.colorspace)
			if self.effect_enabled:
				gst.element_link_many(self.queue_video, self.effect, self.overlay)
			else:
				gst.element_link_many(self.queue_video, src_colorspace, self.overlay)

			err = gst.element_link_many(self.overlay, self.tee, queue1, self.colorspace, self.mux, self.sink)
			if err == False:
				print "Error conecting elements"

			gst.element_link_many(self.queue_audio, self.convert, self.mux)

			if self.preview_enabled:
				self.player.add(queue2, self.preview_element)
				err = gst.element_link_many(self.tee, queue2, self.preview_element)
				if (err == False):
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

	def on_dynamic_pad(self, dbin, pad, islast):
		print "dynamic pad called!"
		name = pad.get_caps()[0].get_name()
		print name

		if ("audio" in name):
			pad.link(self.queue_audio.get_pad("sink"))

		if ("video" in name):
			pad.link(self.queue_video.get_pad("sink"))

	def set_effects(self, state):
		self.effect_enabled = state

	def set_preview(self, state):
		self.preview_enabled = state

	def on_stop_press(self, event):
		if (self.state == "playing"):
			self.player.set_state(gst.STATE_NULL)
			play_button = self.interface.get_object("play_button")
			play_button.set_active(False)
			self.state = "stopped"
			self.overlay_button.set_sensitive(False)

	def on_window_closed(self, event, data):
		gtk.main_quit()

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
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			previewsink = message.src
			self.preview.set_display(previewsink)
			previewsink.set_property("sync", "false")
