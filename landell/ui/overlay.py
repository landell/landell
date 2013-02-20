# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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


import gi
import Gtk
from landell.settings import UI_DIR
import landell.config as config

DEFAULT_FONT = "Sans Bold 14"
DEFAULT_HALIGN = "center"
DEFAULT_VALIGN = "baseline"

class OverlayUI:

    def __init__(self, ui, landell):
        self.ui = ui
        self.landell = landell
        self.interface = Gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/overlay.ui")
        self.widget = self.interface.get_object("vbox")

        self.button = self.interface.get_object("apply_button")
        self.clear_button = self.interface.get_object("clear_button")
        self.textview = self.interface.get_object("overlay_textview")

        self.font_selector = Gtk.FontSelectionDialog("Select a font name")

        self.font_selector_button = self.interface.get_object(
            "font_selector_button"
        )

        self.font_selector.set_transient_for(self.ui.main_window)
        self.font_selector.set_destroy_with_parent(True)

        self.font_selector_entry = self.interface.get_object(
            "font_selector_entry"
        )

        # halign
        self.left_button = self.interface.get_object("left_toolbutton")
        self.center_button = self.interface.get_object("center_toolbutton")
        self.right_button = self.interface.get_object("right_toolbutton")

        self.horizontal_group = Gtk.ActionGroup("horizontal_group")
        horizontal_actions = [
            ("left_radioaction", "Gtk-justify-left", "Left", None,
                "Left", 0),
            ("center_radioaction", "Gtk-justify-center", "Center", None,
                "Center", 1),
            ("right_radioaction", "Gtk-justify-right", "Right", None,
                "Right", 2)
        ]
        self.horizontal_group.add_radio_actions(
                horizontal_actions, 0, None, None
        )
        self.left_radioaction = self.horizontal_group.get_action("left_radioaction")
        self.left_radioaction.connect_proxy(self.left_button)
        self.center_radioaction = self.horizontal_group.get_action(
                "center_radioaction"
        )
        self.center_radioaction.connect_proxy(self.center_button)
        self.right_radioaction = self.horizontal_group.get_action(
                "right_radioaction"
        )
        self.right_radioaction.connect_proxy(self.right_button)

        # valign
        self.top_button = self.interface.get_object("top_toolbutton")
        self.baseline_button = self.interface.get_object("baseline_toolbutton")
        self.bottom_button = self.interface.get_object("bottom_toolbutton")

        self.vertical_group = Gtk.ActionGroup("vertical_group")
        vertical_actions = [
            ("top_radioaction", "Gtk-goto-top", "Top", None,
                "Top", 0),
            ("baseline_radioaction", "Gtk-missing-image", "Baseline", None,
                "Baseline", 1),
            ("bottom_radioaction", "Gtk-goto-bottom", "Bottom", None,
                "Bottom", 2)
        ]
        self.vertical_group.add_radio_actions(
                vertical_actions, 0, None, None
        )

        self.top_radioaction = self.vertical_group.get_action("top_radioaction")
        self.top_radioaction.connect_proxy(self.top_button)
        self.baseline_radioaction = self.vertical_group.get_action(
                "baseline_radioaction"
        )
        self.baseline_radioaction.connect_proxy(self.baseline_button)
        self.bottom_radioaction = self.vertical_group.get_action(
                "bottom_radioaction"
        )
        self.bottom_radioaction.connect_proxy(self.bottom_button)

        self._set_font(DEFAULT_FONT)
        self._set_halign(DEFAULT_HALIGN)
        self._set_valign(DEFAULT_VALIGN)

        self._set_config()
        self._load_config()

        self.button.connect("clicked", self.on_apply_clicked)
        self.clear_button.connect("clicked", self.on_clear_clicked)
        self.landell.connect("preplay", self._preplay)
        self.landell.connect("playing", self._playing)
        self.landell.connect("stopped", self._stopped)
        self.font_selector_button.connect("clicked", self.on_font_change)
        self.font_selector.connect("response", self.on_close_dialog)
        self.left_radioaction.connect("changed", self.on_horizontal_changed)
        self.top_radioaction.connect("changed", self.on_vertical_changed)

    def _set_config(self):
        self.config = config.config
        self.section = "Settings"
        self.item = "Text Overlay"

    def _load_config(self):
        config_item = self.config.get_item(self.section, self.item)
        if config_item:
            if "font" in config_item:
                self._set_font(config_item['font'])
            if "halign" in config_item:
                self._set_halign(config_item['halign'])
            if "valign" in config_item:
                self._set_valign(config_item['valign'])

    def _set_halign(self, halign):
        self.halign = halign
        action = self.horizontal_group.get_action(self.halign+"_radioaction")
        action.set_active(True)

    def _set_valign(self, valign):
        self.valign = valign
        action = self.vertical_group.get_action(self.valign+"_radioaction")
        action.set_active(True)

    def _set_font(self, font):
        self.font = font
        self.font_selector_entry.set_text(font)
        self.font_selector.set_font_name(font)

    def on_font_change(self, event):
        self.font_selector.show_all()
        self.font_selector.run()

    def on_horizontal_changed(self, widget, current):
        name = current.get_name()
        if name == "left_radioaction":
            action = "left"
        elif name == "right_radioaction":
            action = "right"
        elif name == "center_radioaction":
            action = "center"

        self.halign = action
        self.save()

    def on_vertical_changed(self, widget, current):
        name = current.get_name()
        if name == "top_radioaction":
            action = "top"
        elif name == "bottom_radioaction":
            action = "bottom"
        elif name == "baseline_radioaction":
            action = "baseline"

        self.valign = action
        self.save()

    def _make_config(self):
        config = {}
        config['font'] = self.font
        config['valign'] = self.valign
        config['halign'] = self.halign
        return config

    def save(self):
        self.config.set_item(self.section, self.item, self._make_config())

    def on_close_dialog(self, dialog, response):
        if response == Gtk.RESPONSE_CANCEL or \
           response == Gtk.RESPONSE_DELETE_EVENT:
            dialog.hide_all()

        if response == Gtk.RESPONSE_OK:
            font = self.font_selector.get_font_name()
            self._set_font(font)
            self.save()
            dialog.hide_all()

        if response == Gtk.RESPONSE_APPLY:
            font = self.font_selector.get_font_name()
            self._set_font(font)
            self.save()

    def _get_text(self):
        buffer = self.textview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)
        return text

    def apply_settings(self):
        self.landell.set_overlay_text(self._get_text())
        self.landell.set_overlay_font(self.font)
        self.landell.set_halign(self.halign)
        self.landell.set_valign(self.valign)

    def _preplay(self, landell):
        self.apply_settings()

    def _playing(self, landell):
        self.button.set_sensitive(True)

    def _stopped(self, landell):
        self.button.set_sensitive(False)

    def on_apply_clicked(self, event):
        self.apply_settings()

    def on_clear_clicked(self, event):
        buffer = self.textview.get_buffer()
        buffer.set_text("")
        self.apply_settings()

    def get_widget(self):
        return self.widget
