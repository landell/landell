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
import effect

def register_filter(feature_list, filter_string):
    type_list = []
    for plugin_feature in feature_list:
        if plugin_feature.get_klass() == filter_string:
            type_list.append(plugin_feature.get_name())
    return type_list

class Effects:

    registry = gst.registry_get_default()
    all_effects = registry.get_feature_list(gst.ElementFactory)
    effects = {}
    effects['video'] = register_filter(all_effects, "Filter/Effect/Video")
    effects['audio'] = register_filter(all_effects, "Filter/Effect/Audio")
    effect_klass = {
            'video': effect.video_effect.VideoEffect,
            'audio': effect.audio_effect.AudioEffect
    }

    @classmethod
    def get_types(klass, effect_type):
        return klass.effects[effect_type]

    @classmethod
    def make_effect(klass, effect_name, effect_type):
        effect_name = Effects.treat_effect_name(effect_name)

        print "effect_type " + effect_type
        effectbin = klass.effect_klass[effect_type](effect_name)
        return effectbin

    @classmethod
    def treat_effect_name(klass, effect_name):
        if effect_name == "none":
            return "identity"
        return effect_name
