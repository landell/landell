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
import pygst
pygst.require("0.10")
import gst

class EffectRegistry:

    def __init__(self):

        self.gst_registry = gst.registry_get_default()
        all_effects = self.gst_registry.get_feature_list(gst.ElementFactory)
        self.registry = {}
        self.registry['video'] = self._register_filter(all_effects, "Filter/Effect/Video")
        self.registry['audio'] = self._register_filter(all_effects, "Filter/Effect/Audio")

    def get_types(self, effect_type):
        return self.registry[effect_type]

    def _register_filter(self, feature_list, filter_string):
        type_list = []
        for plugin_feature in feature_list:
            if plugin_feature.get_klass() == filter_string:
                type_list.append(plugin_feature.get_name())
        return type_list
