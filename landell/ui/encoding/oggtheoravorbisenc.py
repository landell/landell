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

from core import EncodingUI
from landell.settings import UI_DIR

class OggTheoraVorbisEncodingUI(EncodingUI):

    def __init__(self):
        EncodingUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/encoding/theora.ui")
        self.theora_vorbis_box = self.interface.get_object("theora_vorbis_box")
        self.theora_quality_entry = self.interface.get_object("theora_quality_entry")
        self.keyframe_entry = self.interface.get_object("keyframe_entry")
        self.theora_bitrate_entry = self.interface.get_object("theora_bitrate_entry")
        self.vorbis_quality_entry = self.interface.get_object("vorbis_quality_entry")
        self.vorbis_bitrate_entry = self.interface.get_object("vorbis_bitrate_entry")

    def get_widget(self):
        return self.theora_vorbis_box

    def get_name(self):
        return "theora vorbis"

    def get_description(self):
        return "Theora + Vorbis encoding"

    def update_config(self):
        self.theora_quality_entry.set_text(self.config["theora_quality"])
        self.keyframe_entry.set_text(self.config["keyframe"])
        self.theora_bitrate_entry.set_text(self.config["theora_bitrate"])
        self.vorbis_quality_entry.set_text(self.config["vorbis_quality"])
        self.vorbis_bitrate_entry.set_text(self.config["vorbis_bitrate"])

    def get_config(self):
        self.config["theora_quality"] = self.theora_quality_entry.get_text()
        self.config["keyframe"] = self.keyframe_entry.get_text()
        self.config["theora_bitrate"] = self.theora_bitrate_entry.get_text()
        self.config["vorbis_quality"] = self.vorbis_quality_entry.get_text()
        self.config["vorbis_bitrate"] = self.vorbis_bitrate_entry.get_text()
        return self.config
