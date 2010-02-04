#!/usr/bin/python

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

def register_filter(feature_list):
	type_list = []
	for plugin_feature in feature_list:
		if plugin_feature.get_klass() == "Filter/Effect/Video":
			type_list.append(plugin_feature.get_name())
			print plugin_feature.get_name()
			print plugin_feature.get_num_pad_templates()
	return type_list

class Effect:

	registry = gst.registry_get_default()
	effects = registry.get_feature_list(gst.ElementFactory)
	effects = register_filter(effects)

	@classmethod
	def get_types(klass):
		return klass.effects
	
	@classmethod
	def make_effect(klass, effect_name):
		plugin_feature = klass.registry.find_feature(effect_name, gst.ElementFactory)
		description = "ffmpegcolorspace ! " + effect_name + " ! ffmpegcolorspace"
		print description
		effectbin = gst.parse_bin_from_description(description, True) 
		return effectbin
