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
from sltv.audio import *
from sltv.sltv import *
from sltv.settings import UI_DIR

import about
import sources
import message
import outputs


import preview
import effects
import overlay
import volume

class SltvUI:

    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/sltv.ui")
        self.main_window = self.interface.get_object("window1")
        self.main_window.show_all()
        self.about = about.About(self)

        preview_area = self.interface.get_object("preview_area")
        self.sltv = Sltv(preview_area)
        self.sltv.connect("stopped", self.stopped)
        self.sltv.connect("playing", self.playing)
        self.sltv.connect("preplay", self.preplay)
        self.sltv.connect("error", self.error)

        self.settings_box = self.interface.get_object("vbox4")
        self.preview = preview.PreviewUI(self, self.sltv)
        self.effects = effects.EffectsUI(self, self.sltv)
        self.overlay = overlay.OverlayUI(self, self.sltv)
        self.volume = volume.VolumeUI(self, self.sltv)
        self.settings_box.add(self.preview.get_widget())
        self.settings_box.add(self.effects.get_widget())
        self.settings_box.add(self.overlay.get_widget())
        self.settings_box.add(self.volume.get_widget())

        self.play_button = self.interface.get_object("play_button")
        self.stop_button = self.interface.get_object("stop_button")

        self.outputs = self.sltv.outputs
        self.outputs_ui = outputs.Outputs(self, self.outputs)

        #combobox to choose source

        self.source_combobox = self.interface.get_object("sources_combobox")
        self.sources = self.sltv.sources
        self.sources_ui = sources.Sources(self, self.sources)
        self.source_combobox.set_model(sources.VideoModel(self.sources).model)
        cell = gtk.CellRendererText()
        self.source_combobox.pack_start(cell, True)
        self.source_combobox.add_attribute(cell, "text", 0)
        self.source_combobox.set_active(0)
        self.source_combobox.connect("changed",self.on_switch_source)

        self.on_switch_source(self.source_combobox)

        # audio combobox
        self.audio_sources_combobox = self.interface.get_object("audio_sources_combobox")
        self.audio_sources_combobox.set_model(sources.AudioModel(self.sources).model)
        cell = gtk.CellRendererText()
        self.audio_sources_combobox.pack_start(cell, True)
        self.audio_sources_combobox.add_attribute(cell, "text", 0)
        self.audio_sources_combobox.connect("changed", self.on_select_audio_source)
        self.audio_sources_combobox.set_active(0)

        #menu

        output_menuitem = self.interface.get_object("output_menuitem")
        sources_menuitem = self.interface.get_object("sources_menuitem")
        self.about_menu = self.interface.get_object("about_menu")

        self.play_button.connect("clicked", self.on_play_press)
        self.stop_button.connect("clicked", self.on_stop_press)
        self.main_window.connect("delete_event", self.on_window_closed)
        output_menuitem.connect("activate", self.show_output)
        sources_menuitem.connect("activate", self.show_sources)
        self.about_menu.connect("activate", self.show_about)

    def stopped(self, sltv):
        self.stop_button.set_sensitive(False)
        self.play_button.set_sensitive(True)
        self.audio_sources_combobox.set_sensitive(True)

    def playing(self, sltv):
        self.play_button.set_sensitive(False)
        self.stop_button.set_sensitive(True)

    def preplay(self, sltv):
        self.audio_sources_combobox.set_sensitive(False)

    def error(self, sltv, msg):
        message.MessageError(msg, self)

    def selected_video_source(self):
        model = self.source_combobox.get_model()
        iter = self.source_combobox.get_active_iter()
        if iter == None:
            return None
        return model.get_value(iter, 0)

    def selected_audio_source(self):
        model = self.audio_sources_combobox.get_model()
        iter = self.audio_sources_combobox.get_active_iter()
        if iter == None:
            return None
        return model.get_value(iter, 0)

    def on_play_press(self, event):
        if self.selected_video_source() == None:
            message.MessageInfo(
                "Please, choose or add a video source.",
                self
            )
            return False

        self.play_button.set_sensitive(False)
        self.play()

    def play(self):
        if not self.sltv.playing():
            self.sltv.play()

    def on_switch_source(self, combobox):
        source_name = self.selected_video_source()
        self.sltv.set_video_source(source_name)

    def on_select_audio_source(self, combobox):
        source_name = self.selected_audio_source()
        self.sltv.set_audio_source(source_name)

    def show_encoding(self, menuitem):
        self.sltv.show_encoding()

    def show_output(self, menuitem):
        self.outputs_ui.show_window()

    def show_sources(self, menuitem):
        self.sources_ui.show_window()

    def show_about(self, menuitem):
        self.about.show_window()

    def on_stop_press(self, event):
        self.stop_button.set_sensitive(False)
        self.stop()

    def stop(self):
        if self.sltv.playing():
            self.sltv.stop()

    def on_window_closed(self, event, data):
        gtk.main_quit()
