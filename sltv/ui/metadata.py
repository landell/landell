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

import gtk
import gst
from sltv.settings import UI_DIR
import datetime
from sltv.config import config

class MetadataUI:
    def __init__(self, sltv, parent_dialog):
        self.sltv = sltv
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/metadata.ui")
        self.content_area = self.interface.get_object("content_area")

        self.title_entry = self.interface.get_object("title_entry")
        self.calendar = self.interface.get_object("calendar")
        self.textview = self.interface.get_object("description_textview")

        self.config = config
        self.section = "Metadata"

        self._load()

        self.sltv.connect("preplay", self._preplay)
        parent_dialog.connect('delete-event', self._save)
        parent_dialog.connect('response', self._save)

    def get_widget(self):
        return self.content_area

    def _preplay(self, sltv):
        taglist = gst.TagList()
        taglist[gst.TAG_TITLE] = self.title_entry.get_text()
        (year, month, day) = self.calendar.get_date()
        date = "%d-%d-%d" % (year, month, day)
        taglist[gst.TAG_DATE] = date
        buffer = self.textview.get_buffer()
        text = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter(), True
        )
        taglist[gst.TAG_DESCRIPTION] = text
        self.sltv.set_metadata(taglist)

    def _save(self, *args):
        self.config.remove_section(self.section)
        (year, month, day) = self.calendar.get_date()
        self.config.set_item(self.section, "year", year)
        self.config.set_item(self.section, "month", month)
        self.config.set_item(self.section, "day", day)

        title = self.title_entry.get_text()
        self.config.set_item(self.section, "title", title)

        buffer = self.textview.get_buffer()
        text = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter(), True
        )
        self.config.set_item(self.section, "description", text)

    def _load(self):
        title = self.config.get_item(self.section, "title")
        self.title_entry.set_text(title)

        year = self.config.get_item(self.section, "year")
        month = self.config.get_item(self.section, "month")
        self.calendar.select_month(int(month), int(year))
        day = self.config.get_item(self.section, "day")
        self.calendar.select_day(int(day))

        description = self.config.get_item(self.section, "description")
        buffer = gtk.TextBuffer()
        buffer.set_text(description)
        self.textview.set_buffer(buffer)
