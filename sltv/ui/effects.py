#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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
from sltv.settings import UI_DIR
import sltv.effects as effects
from sltv.sltv import MEDIA_VIDEO, MEDIA_AUDIO

class EffectsUI:

    def __init__(self, sltv):
        self.sltv = sltv
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/effects.ui")
        self.widget = self.interface.get_object("vbox")
        self.effect_registry = effects.EffectRegistry()
        self.video_effect_combobox = self.interface.get_object(
                "video_effect_combobox"
        )
        self.audio_effect_combobox = self.interface.get_object(
                "audio_effect_combobox"
        )
        self._create_effects_combobox(self.video_effect_combobox, "video")
        self._create_effects_combobox(self.audio_effect_combobox, "audio")
        self.effect_checkbutton = self.interface.get_object(
            "effect_checkbutton"
        )
        self.video_effect_button = self.interface.get_object(
                "video_effect_button"
        )
        self.audio_effect_button = self.interface.get_object(
                "audio_effect_button"
        )
        self.video_effect_label = self.interface.get_object("video_effect_label")
        self.audio_effect_label = self.interface.get_object("audio_effect_label")

        self.effect_checkbutton.connect("toggled", self.effect_toggled)
        self.video_effect_button.connect("clicked", self.effect_changed)
        self.audio_effect_button.connect("clicked", self.effect_changed)
        self.set_effects(False)
        self.effect_enabled = False

    def play(self):
        video_effect_name = self.video_effect_combobox.get_active_text()
        audio_effect_name = self.audio_effect_combobox.get_active_text()
        self.sltv.set_video_effect_name(video_effect_name)
        self.sltv.set_audio_effect_name(audio_effect_name)
        if self.effect_enabled == True:
            if self.sltv.audio_source == None:
                self.audio_effect_button.set_sensitive(False)
            else:
                self.audio_effect_button.set_sensitive(True)
            self.video_effect_button.set_sensitive(True)
    def stop(self):
        self.audio_effect_button.set_sensitive(False)
        self.video_effect_button.set_sensitive(False)
    def _create_effects_combobox(self, combobox, effect_type):
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        combobox.set_model(liststore)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 0)
        liststore.append(("none",))
        for etype in self.effect_registry.get_types(effect_type):
            liststore.append((etype,))
        combobox.set_active(0)

    def set_effects(self, state):
        self.video_effect_combobox.set_sensitive(state)
        self.audio_effect_combobox.set_sensitive(state)
        self.video_effect_label.set_sensitive(state)
        self.audio_effect_label.set_sensitive(state)
        if self.sltv.playing() and state == True:
            self.video_effect_button.set_sensitive(True)
            if self.selected_audio_source() == None:
                self.audio_effect_button.set_sensitive(False)
            else:
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
        if self.effect_enabled:
            print "sending change_effect"
            if button is self.video_effect_button:
                self.sltv.change_effect(
                        self.video_effect_combobox.get_active_text(), MEDIA_VIDEO
                )
            else:
                self.sltv.change_effect(
                        self.audio_effect_combobox.get_active_text(), MEDIA_AUDIO
                )

    def get_widget(self):
        return self.widget
