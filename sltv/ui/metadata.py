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

class MetadataUI:
    def __init__(self, ui, sltv):
        self.sltv = sltv
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/metadata.ui")
        self.content_area = self.interface.get_object("content_area")

        self.title_entry = self.interface.get_object("title_entry")
        self.calendar = self.interface.get_object("calendar")
        self.textview = self.interface.get_object("description_textview")

        self.sltv.connect("preplay", self._preplay)

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
