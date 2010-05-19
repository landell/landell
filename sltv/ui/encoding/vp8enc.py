# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Copyright (C) 2010 Gustavo Noronha Silva <gns@gnome.org>
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

class VP8EncodingUI(EncodingUI):

    def get_widget(self):
        return None

    def get_name(self):
        return "vp8"

    def get_description(self):
        return "VP8 encoding"
