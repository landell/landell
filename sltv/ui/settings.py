# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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

import gtk
from sltv.settings import UI_DIR
import effects
import overlay
import volume

class SettingsUI:

    def __init__(self, ui, sltv):
        self.ui = ui
        self.sltv = sltv
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/settings.ui")
        self.widget = self.interface.get_object("vbox")
        self.content = self.interface.get_object("content_viewport")

        self.effects = effects.EffectsUI(self.ui, self.sltv)
        self.overlay = overlay.OverlayUI(self.ui, self.sltv)
        self.volume = volume.VolumeUI(self.ui, self.sltv)

        self.effects_button = self.interface.get_object("effects_toolbutton")
        self.overlay_button = self.interface.get_object("overlay_toolbutton")
        self.volume_button = self.interface.get_object("volume_toolbutton")

        settings_group = gtk.ActionGroup("settings_group")
        settings_actions = [
            ("effects_radioaction", "gtk-missing-image", "Effects", None,
                "Effects", 0),
            ("overlay_radioaction", "gtk-missing-image", "Overlay", None,
                "Overlay", 1),
            ("volume_radioaction", "gtk-missing-image", "Volume", None,
                "Volume", 2)
        ]
        settings_group.add_radio_actions(
                settings_actions, 0, self.on_settings_changed, None
        )

        self.effects_radioaction = settings_group.get_action(
            "effects_radioaction"
        )
        self.effects_radioaction.connect_proxy(self.effects_button)

        self.overlay_radioaction = settings_group.get_action(
            "overlay_radioaction"
        )
        self.overlay_radioaction.connect_proxy(self.overlay_button)

        self.volume_radioaction = settings_group.get_action(
            "volume_radioaction"
        )
        self.volume_radioaction.connect_proxy(self.volume_button)

        self.selected_box = self.effects.get_widget()
        self.content.add(self.effects.get_widget())


    def on_settings_changed(self, widget, current):
        if self.selected_box:
            self.content.remove(self.selected_box)

        name = current.get_name()
        if name == "effects_radioaction":
            self.selected_box = self.effects.get_widget()
        elif name == "overlay_radioaction":
            self.selected_box = self.overlay.get_widget()
        elif name == "volume_radioaction":
            self.selected_box =  self.volume.get_widget()
        else:
            self.selected_box = None

        self.content.add(self.selected_box)

    def get_widget(self):
        return self.widget
