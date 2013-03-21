# -*- coding: utf-8 -*-
# Copyright (C) 2013 Collabora Ltda
# Author: Luciana Fujii Pontello <luciana.fujii@collabora.com>
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
from gi.repository import Gst, Gtk, GLib
from landell.settings import UI_DIR
import datetime
from landell.config import config

class GeneralUI:
    def __init__(self, landell, parent_dialog):
        self.landell = landell
        self.interface = Gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/general.ui")
        self.content_area = self.interface.get_object("content_area")

        self.audiorate_entry = self.interface.get_object("audiorate_entry")

        self.config = config
        self.section = "General"

        self._load()

        self.landell.connect("preplay", self._preplay)
        parent_dialog.connect('delete-event', self._save)
        parent_dialog.connect('response', self._save)

    def get_widget(self):
        return self.content_area

    def _preplay(self, landell):
        audiorate = self.audiorate_entry.get_text()
        self.landell.set_audiorate(audiorate)

    def _save(self, *args):
        self.config.remove_section(self.section)

        audiorate = self.audiorate_entry.get_text()
        self.config.set_item(self.section, "audiorate", audiorate)

    def _load(self):
        audiorate = self.config.get_item(self.section, "audiorate")
        if audiorate:
            self.audiorate_entry.set_text(audiorate)
