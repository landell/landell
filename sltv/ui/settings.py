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
import watermark
import videobalance

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
        self.watermark = watermark.WaterMarkUI(self.ui, self.sltv)
        self.videobalance = videobalance.VideoBalanceUI(self.ui, self.sltv)

        self.effects_button = self.interface.get_object("effects_toolbutton")
        self.overlay_button = self.interface.get_object("overlay_toolbutton")
        self.watermark_button = self.interface.get_object("watermark_toolbutton")
        self.videobalance_button = self.interface.get_object(
                "videobalance_toolbutton"
        )

        settings_group = gtk.ActionGroup("settings_group")
        settings_actions = [
            ("effects_radioaction", "gtk-missing-image", "Effects", None,
                "Effects", 0),
            ("overlay_radioaction", "gtk-missing-image", "Overlay", None,
                "Overlay", 1),
            ("watermark_radioaction", "gtk-missing-image", "Watermark", None,
                "Watermark", 2),
            ("videobalance_radioaction", "gtk-missing-image", "VideoBalance", None,
                "Video Balance", 3),
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

        self.watermark_radioaction = settings_group.get_action(
            "watermark_radioaction"
        )
        self.watermark_radioaction.connect_proxy(self.watermark_button)

        self.videobalance_radioaction = settings_group.get_action(
            "videobalance_radioaction"
        )
        self.videobalance_radioaction.connect_proxy(self.videobalance_button)

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
        elif name == "watermark_radioaction":
            self.selected_box = self.watermark.get_widget()
        elif name == "videobalance_radioaction":
            self.selected_box = self.videobalance.get_widget()
        else:
            self.selected_box = None

        self.content.add(self.selected_box)

    def get_widget(self):
        return self.widget
