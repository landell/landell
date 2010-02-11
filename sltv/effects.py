# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
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
from swap import *

def register_filter(feature_list, filter_string):
    type_list = []
    for plugin_feature in feature_list:
        if plugin_feature.get_klass() == filter_string:
            type_list.append(plugin_feature.get_name())
    return type_list

class Effect:

    registry = gst.registry_get_default()
    all_effects = registry.get_feature_list(gst.ElementFactory)
    effects = {}
    effects['video'] = register_filter(all_effects, "Filter/Effect/Video")
    effects['audio'] = register_filter(all_effects, "Filter/Effect/Audio")
    convertion = {
            'video': 'ffmpegcolorspace',
            'audio': 'audioconvert'
    }

    @classmethod
    def get_types(klass, effect_type):
        return klass.effects[effect_type]

    @classmethod
    def make_effect(klass, effect_name, effect_type):
        effect_name = Effect.treat_effect_name(effect_name)
        effectbin = gst.Bin()
        convertion_element1 = gst.element_factory_make(
                klass.convertion[effect_type], "conv1"
        )
        convertion_element2 = gst.element_factory_make(
                klass.convertion[effect_type], "conv2"
        )
        effect_queue = gst.element_factory_make("queue", "effect_queue")
        effect_element = gst.element_factory_make(effect_name, effect_name)
        effectbin.add(
                convertion_element1, effect_queue, effect_element,
                convertion_element2
        )
        gst.element_link_many(
                convertion_element1, effect_queue, effect_element,
                convertion_element2
        )
        sink_pad = gst.GhostPad(
                "sink", effectbin.find_unlinked_pad(gst.PAD_SINK)
        )
        src_pad = gst.GhostPad("src", effectbin.find_unlinked_pad(gst.PAD_SRC))
        effectbin.add_pad(sink_pad)
        effectbin.add_pad(src_pad)
        return effectbin

    @classmethod
    def treat_effect_name(klass, effect_name):
        if effect_name == "none":
            return "identity"
        return effect_name

    @classmethod
    def change(klass, effect_bin, old_effect_name, effect_name):
        old_effect_name = Effect.treat_effect_name(old_effect_name)
        effect_name = Effect.treat_effect_name(effect_name)
        print old_effect_name + " " +  effect_name
        new_effect = gst.element_factory_make(effect_name, effect_name)
        effect_element = effect_bin.get_by_name(old_effect_name)
        effect_queue = effect_bin.get_by_name("effect_queue")
        colorspace2 = effect_bin.get_by_name("conv2")
        Swap.swap_element(
                effect_bin, effect_queue, colorspace2,
                effect_element, new_effect
        )
