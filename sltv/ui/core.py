#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
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
from sltv.output import *
from sltv.encoding import *
from sltv.audio import *
from sltv.sltv import *
from sltv.settings import UI_DIR

import about
import sources

def create_effects_combobox(combobox, effect_type):
    liststore = gtk.ListStore(gobject.TYPE_STRING)
    combobox.set_model(liststore)
    cell = gtk.CellRendererText()
    combobox.pack_start(cell, True)
    combobox.add_attribute(cell, 'text', 0)
    liststore.append(("none",))
    for etype in Effect.get_types(effect_type):
        liststore.append((etype,))
    combobox.set_active(0)

class SltvUI:

    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/sltv.ui")
        window = self.interface.get_object("window1")
        window.show_all()
        self.about = about.About(window)

        preview_area = self.interface.get_object("preview_area")
        self.sltv = Sltv(preview_area, window)

        file_location_entry = self.interface.get_object("file_location_entry")
        self.play_button = self.interface.get_object("play_button")
        self.stop_button = self.interface.get_object("stop_button")
        self.stop_button.set_active(True)
        self.overlay_button = self.interface.get_object("overlay_button")

        #combobox to choose source

        self.source_combobox = self.interface.get_object("sources_combobox")
        self.sources = self.sltv.sources
        self.sources_ui = sources.Sources(window, self.sources)
        self.source_combobox.set_model(sources.VideoModel(self.sources).model)
        cell = gtk.CellRendererText()
        self.source_combobox.pack_start(cell, True)
        self.source_combobox.add_attribute(cell, "text", 0)
        self.source_combobox.set_active(0)
        self.source_combobox.connect("changed",self.on_switch_source)

        #menu

        output_menuitem = self.interface.get_object("output_menuitem")
        encoding_menuitem = self.interface.get_object("encoding_menuitem")
        sources_menuitem = self.interface.get_object("sources_menuitem")
        self.about_menu = self.interface.get_object("about_menu")

        self.video_effect_combobox = self.interface.get_object(
                "video_effect_combobox"
        )
        self.audio_effect_combobox = self.interface.get_object(
                "audio_effect_combobox"
        )
        create_effects_combobox(self.video_effect_combobox, "video")
        create_effects_combobox(self.audio_effect_combobox, "audio")
        self.effect_checkbutton = self.interface.get_object(
            "effect_checkbutton"
        )
        self.video_effect_button = self.interface.get_object(
                "video_effect_button"
        )
        self.audio_effect_button = self.interface.get_object(
                "audio_effect_button"
        )
        self.preview_checkbutton = self.interface.get_object(
            "preview_checkbutton"
        )


        self.video_effect_label = self.interface.get_object("video_effect_label")
        self.audio_effect_label = self.interface.get_object("audio_effect_label")

        self.effect_checkbutton.connect("toggled", self.effect_toggled)
        self.preview_checkbutton.connect("toggled", self.preview_toggled)
        self.play_button.connect("toggled", self.on_play_press)
        self.stop_button.connect("toggled", self.on_stop_press)
        self.overlay_button.connect("clicked", self.on_overlay_change)
        window.connect("delete_event", self.on_window_closed)
        output_menuitem.connect("activate", self.show_output)
        encoding_menuitem.connect("activate", self.show_encoding)
        sources_menuitem.connect("activate", self.show_sources)
        self.about_menu.connect("activate", self.show_about)
        self.video_effect_button.connect("clicked", self.effect_changed)
        self.audio_effect_button.connect("clicked", self.effect_changed)

        self.set_effects(False)
        self.preview_state = False
        self.sltv.set_preview(False)
        self.overlay_textview = self.interface.get_object("overlay_textview")
        self.effect_enabled = False

    def selected_video_source(self):
        model = self.source_combobox.get_model()
        iter = self.source_combobox.get_active_iter()
        return model.get_value(iter, 0)

    def on_play_press(self, event):
        if not self.sltv.playing():
            self.stop_button.set_active(False)

            overlay_buffer = self.overlay_textview.get_buffer()
            overlay_text = overlay_buffer.get_text(
                overlay_buffer.get_start_iter(),
                overlay_buffer.get_end_iter(),
                True
            )
            video_effect_name = self.video_effect_combobox.get_active_text()
            audio_effect_name = self.audio_effect_combobox.get_active_text()
            self.overlay_button.set_sensitive(True)
            if self.effect_enabled == True:
                self.audio_effect_button.set_sensitive(True)
                self.video_effect_button.set_sensitive(True)
            self.sltv.play(
                    overlay_text, video_effect_name, audio_effect_name,
                    self.selected_video_source()
            )

    def on_switch_source(self, combobox):
        if self.sltv.playing():
            source_name = self.selected_video_source()
            self.sltv.switch_source(source_name)

    def show_encoding(self, menuitem):
        self.sltv.show_encoding()

    def show_output(self, menuitem):
        self.sltv.show_output()

    def show_sources(self, menuitem):
        self.sources_ui.show_window()

    def show_about(self, menuitem):
        self.about.show_window()

    def set_effects(self, state):
        self.video_effect_combobox.set_sensitive(state)
        self.audio_effect_combobox.set_sensitive(state)
        self.video_effect_label.set_sensitive(state)
        self.audio_effect_label.set_sensitive(state)
        if self.sltv.playing() and state == True:
            self.video_effect_button.set_sensitive(True)
            self.audio_effect_button.set_sensitive(True)
        elif self.sltv.playing() and state == False:
            self.video_effect_button.set_sensitive(False)
            self.audio_effect_button.set_sensitive(False)

        self.effect_enabled = state
        self.sltv.set_effects(state)
        #Send signal

    def effect_toggled(self, checkbox):
        self.set_effects(not self.effect_enabled)

    def effect_changed(self, button):
        print "button clicked"
        if self.effect_enabled:
            print "sending change_effect"
            if button.get_name() == "video_effect_button":
                self.sltv.change_effect(
                        self.video_effect_combobox.get_active_text(), "video"
                )
            else:
                self.sltv.change_effect(
                        self.audio_effect_combobox.get_active_text(), "audio"
                )

    def preview_toggled(self, checkbox):
        self.preview_state = not self.preview_state
        self.sltv.set_preview(self.preview_state)

    def on_stop_press(self, event):
        if self.sltv.playing():
            self.play_button.set_active(False)
            self.overlay_button.set_sensitive(False)
            self.audio_effect_button.set_sensitive(False)
            self.video_effect_button.set_sensitive(False)
            self.sltv.stop()

    def on_window_closed(self, event, data):
        gtk.main_quit()

    def on_overlay_change(self, event):
        overlay_buffer = self.overlay_textview.get_buffer()
        overlay_text = overlay_buffer.get_text(
            overlay_buffer.get_start_iter(),
            overlay_buffer.get_end_iter(),
            True
        )
        self.sltv.change_overlay(overlay_text)
