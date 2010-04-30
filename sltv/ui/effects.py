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

    def __init__(self, ui, sltv):
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
        self._create_effects_combobox(self.video_effect_combobox, MEDIA_VIDEO)
        self._create_effects_combobox(self.audio_effect_combobox, MEDIA_AUDIO)
        self.effect_checkbutton = self.interface.get_object(
            "effect_checkbutton"
        )
        self.apply_button = self.interface.get_object("apply_button")
        self.video_effect_label = self.interface.get_object("video_effect_label")
        self.audio_effect_label = self.interface.get_object("audio_effect_label")

        self.effect_checkbutton.connect("toggled", self.effect_toggled)
        self.apply_button.connect("clicked", self.effect_changed)
        self.set_effects(False)
        self.effect_enabled = False

        self.sltv.connect("preplay", self._preplay)
        self.sltv.connect("playing", self._playing)
        self.sltv.connect("stopped", self._stopped)

    def _preplay(self, sltv):
        video_effect_name = self.video_effect_combobox.get_active_text()
        audio_effect_name = self.audio_effect_combobox.get_active_text()
        self.sltv.set_effect_name(MEDIA_VIDEO, video_effect_name)
        self.sltv.set_effect_name(MEDIA_AUDIO, audio_effect_name)

    def _playing(self, sltv):
        if self.effect_enabled == True:
            self.apply_button.set_sensitive(True)

    def _stopped(self, sltv):
        self.apply_button.set_sensitive(False)

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
            self.apply_button.set_sensitive(True)
        elif self.sltv.playing() and state == False:
            self.apply_button.set_sensitive(False)
        else:
            self.apply_button.set_sensitive(False)

        self.effect_enabled = state
        self.sltv.set_effects(state)
        #Send signal

    def effect_toggled(self, checkbox):
        self.set_effects(not self.effect_enabled)

    def effect_changed(self, button):
        if self.effect_enabled:
            print "sending change_effect"
            self.sltv.change_effect(
                self.video_effect_combobox.get_active_text(), MEDIA_VIDEO
            )
            self.sltv.change_effect(
                self.audio_effect_combobox.get_active_text(), MEDIA_AUDIO
            )

    def get_widget(self):
        return self.widget
