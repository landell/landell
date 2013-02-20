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

import gi
import gtk
from landell.settings import UI_DIR

class VideoBalanceUI:

    def __init__(self, ui, landell):
        self.ui = ui
        self.landell = landell

        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/videobalance.ui")
        self.widget = self.interface.get_object("table1")
        self.contrast_adjustment = gtk.Adjustment(1.0, 0, 2.0)
        self.contrast_scale = gtk.HScale(self.contrast_adjustment)
        self.contrast_scale.set_property("digits", 2)
        self.widget.attach(self.contrast_scale, 1, 2, 0, 1)

        self.brightness_adjustment = gtk.Adjustment(0, -1.0, 1.0)
        self.brightness_scale = gtk.HScale(self.brightness_adjustment)
        self.brightness_scale.set_property("digits", 2)
        self.widget.attach(self.brightness_scale, 1, 2, 1, 2)

        self.hue_adjustment = gtk.Adjustment(0, -1.0, 1.0)
        self.hue_scale = gtk.HScale(self.hue_adjustment)
        self.hue_scale.set_property("digits", 2)
        self.widget.attach(self.hue_scale, 1, 2, 2, 3)

        self.saturation_adjustment = gtk.Adjustment(1.0, 0, 2.0)
        self.saturation_scale = gtk.HScale(self.saturation_adjustment)
        self.saturation_scale.set_property("digits", 2)
        self.widget.attach(self.saturation_scale, 1, 2, 3, 4)

        self.widget.show_all()

        self.contrast_scale.connect("value-changed", self._on_contrast_changed)
        self.brightness_scale.connect("value-changed", self._on_brightness_changed)
        self.hue_scale.connect("value-changed", self._on_hue_changed)
        self.saturation_scale.connect("value-changed", self._on_saturation_changed)

    def _on_contrast_changed(self, adjustment):
        self.landell.set_videobalance_contrast(self.contrast_scale.get_value())

    def _on_brightness_changed(self, adjustment):
        self.landell.set_videobalance_brightness(self.brightness_scale.get_value())

    def _on_hue_changed(self, adjustment):
        self.landell.set_videobalance_hue(self.hue_scale.get_value())

    def _on_saturation_changed(self, adjustment):
        self.landell.set_videobalance_saturation(self.saturation_scale.get_value())

    def get_widget(self):
        return self.widget
