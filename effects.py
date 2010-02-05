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

class Effect:

	effects = {}
	effects["none"] = ("identity", "rgb")
	effects["noir_blank"] = ("videobalance saturation=0", "yuv")
	effects["saturation"] = ("videobalance saturation=2", "yuv")
	effects["aging"] = ("agingtv", "rgb")

	@classmethod
	def get_types(klass):
		return klass.effects.keys()
	
	@classmethod
	def make_effect(klass, effect_type):
		if klass.effects[effect_type][1] == "yuv":
			description = klass.effects[effect_type][0]
		elif klass.effects[effect_type][1] == "rgb":
			description = "ffmpegcolorspace ! " + klass.effects[effect_type][0] + " ! ffmpegcolorspace"
		else:
			print "Cannot create that effect"
			return None
		print description
		effectbin = gst.parse_bin_from_description(description, True) 
		return effectbin
