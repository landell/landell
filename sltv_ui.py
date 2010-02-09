#!/usr/bin/python

# Copyright (C) 2010 Holoscopio Tecnologia
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
import gtk
from output import *
from encoding import *
from audio import *
from sltv import *
from about import *

def create_effects_combobox(combobox):
	liststore = gtk.ListStore(gobject.TYPE_STRING)
	combobox.set_model(liststore)
	cell = gtk.CellRendererText()
	combobox.pack_start(cell, True)
	combobox.add_attribute(cell, 'text', 0)
	for type in Effect.get_types():
		liststore.append((type,))
	combobox.set_active(0)


class SltvUI:

	def __init__(self):
		self.state = "stopped"
		self.interface = gtk.Builder()
		self.interface.add_from_file("sltv.ui")
		window = self.interface.get_object("window1")
		window.show_all()
		self.about = About(window)

		file_location_entry = self.interface.get_object("file_location_entry")
		self.play_button = self.interface.get_object("play_button")
		self.stop_button = self.interface.get_object("stop_button")
		self.stop_button.set_active(True)
		self.overlay_button = self.interface.get_object("overlay_button")
		output_menuitem = self.interface.get_object("output_menuitem")
		encoding_menuitem = self.interface.get_object("encoding_menuitem")
		video_switch_menuitem = self.interface.get_object("video_switch_menuitem")
		self.about_menu = self.interface.get_object("about_menu")
		self.effect_combobox = self.interface.get_object("effect_combobox")
		create_effects_combobox(self.effect_combobox)
		self.effect_checkbutton = self.interface.get_object("effect_checkbutton")
		self.preview_checkbutton = self.interface.get_object("preview_checkbutton")
		preview_area = self.interface.get_object("preview_area")

		self.effect_label = self.interface.get_object("effect_label")

		self.effect_checkbutton.connect("toggled", self.effect_toggled)
		self.preview_checkbutton.connect("toggled", self.preview_toggled)
		self.play_button.connect("toggled", self.on_play_press)
		self.stop_button.connect("toggled", self.on_stop_press)
		self.overlay_button.connect("pressed", self.on_overlay_change)
		window.connect("delete_event", self.on_window_closed)
		output_menuitem.connect("activate", self.show_output)
		encoding_menuitem.connect("activate", self.show_encoding)
		video_switch_menuitem.connect("activate", self.show_video_switch)
		self.about_menu.connect("activate", self.show_about)

		self.sltv = Sltv(preview_area, window)
		self.set_effects(False)
		self.preview_state = False
		self.sltv.set_preview(False)
		self.overlay_textview = self.interface.get_object("overlay_textview")

	def on_play_press(self, event):
		if self.state == "stopped":
			self.stop_button.set_active(False)
			self.state = "playing"

			overlay_buffer = self.overlay_textview.get_buffer()
			overlay_text = overlay_buffer.get_text(overlay_buffer.get_start_iter(),
					overlay_buffer.get_end_iter(),
					True)
			effect_name = self.effect_combobox.get_active_text()
			self.overlay_button.set_sensitive(True)
			self.sltv.play(overlay_text, effect_name)

	def show_encoding(self, menuitem):
		self.sltv.show_encoding()

	def show_output(self, menuitem):
		self.sltv.show_output()

	def show_video_switch(self, menuitem):
		self.sltv.show_video_switch()

	def show_about(self, menuitem):
		self.about.show_window()

	def set_effects(self, state):
		self.effect_combobox.set_sensitive(state)
		self.effect_label.set_sensitive(state)
		self.effect_enabled = state
		self.sltv.set_effects(state)
		#Send signal

	def effect_toggled(self, checkbox):
		self.set_effects(not self.effect_enabled)

	def preview_toggled(self, checkbox):
		self.preview_state = not self.preview_state
		self.sltv.set_preview(self.preview_state)

	def on_stop_press(self, event):
		if (self.state == "playing"):
			self.play_button.set_active(False)
			self.state = "stopped"
			self.overlay_button.set_sensitive(False)
			self.sltv.stop()

	def on_window_closed(self, event, data):
		gtk.main_quit()

	def on_overlay_change(self, event):
		overlay_buffer = self.overlay_textview.get_buffer()
		overlay_text = overlay_buffer.get_text(overlay_buffer.get_start_iter(),
				overlay_buffer.get_end_iter(),
				True)
		self.sltv.change_overlay(overlay_text)

SltvUI()
gtk.gdk.threads_init()
gtk.main()
