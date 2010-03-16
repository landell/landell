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
from sltv.settings import UI_DIR

class OggTheoraVorbisEncodingUI(EncodingUI):

    def __init__(self):
        EncodingUI.__init__(self)
        self.interface.add_from_file(UI_DIR + "/encoding/theora.ui")
        self.box = self.interface.get_object("theora_box")
        self.quality_entry = self.interface.get_object("quality_entry")
        self.keyframe_entry = self.interface.get_object("keyframe_entry")
        self.bitrate_entry = self.interface.get_object("bitrate_entry")

    def get_widget(self):
        return self.box

    def get_name(self):
        return "theora"

    def get_description(self):
        return "Theora encoding"

    def update_config(self):
        self.quality_entry.set_text(self.config["quality"])
        self.keyframe_entry.set_text(self.config["keyframe"])
        self.bitrate_entry.set_text(self.config["bitrate"])

    def get_config(self):
        self.config["quality"] = self.quality_entry.get_text()
        self.config["keyframe"] = self.keyframe_entry.get_text()
        self.config["bitrate"] = self.bitrate_entry.get_text()
        return self.config
