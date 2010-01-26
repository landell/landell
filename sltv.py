#!/usr/bin/python

import gobject
import pygst
pygst.require("0.10")
import gst
import gtk

class Sltv:

	def __init__(self):
		self.state = 0
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
		if (self.state == 0):
			stop_button = self.interface.get_object("stop_button")
			stop_button.set_active(False)
			self.state = 1
			overlay_text_entry = self.interface.get_object("overlay_text_entry")
			overlay_text = overlay_text_entry.get_text()
			self.player = gst.Pipeline("player")
			self.source = gst.element_factory_make("v4l2src", "source")
			self.overlay = gst.element_factory_make("cairotextoverlay", "overlay")
			self.sink = gst.element_factory_make("xvimagesink", "sink")
			self.player.add(self.source, self.overlay, self.sink)
			gst.element_link_many(self.source, self.overlay, self.sink)

			self.overlay.set_property("text", overlay_text)

			self.player.set_state(gst.STATE_PLAYING)
	
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.connect("message", self.on_message)

	def on_stop_press(self, event):
		if (self.state == 1):
			self.player.set_state(gst.STATE_NULL)
			play_button = self.interface.get_object("play_button")
			play_button.set_active(False)
			self.state = 0

	def on_window_closed(self, event, data):
		self.player.set_state(gst.STATE_NULL)
		loop.quit()

	def on_overlay_change(self, event):

		overlay_text_entry = self.interface.get_object("overlay_text_entry")
		overlay_text = overlay_text_entry.get_text()
		self.overlay.set_property("text", overlay_text)

	def on_message(self, bus, message):
		t = message.type 
		if t == gst.MESSAGE_EOS: 
			self.player.set_state(gst.STATE_NULL) 
		elif t == gst.MESSAGE_ERROR: 
			self.player.set_state(gst.STATE_NULL) 
			loop.quit()

Sltv()
loop = gobject.MainLoop()
loop.run()
