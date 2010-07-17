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
        self.artist_entry = self.interface.get_object("artist_entry")
        self.genre_entry = self.interface.get_object("genre_entry")
        self.calendar = self.interface.get_object("calendar")
        self.location_entry = self.interface.get_object("location_entry")
        self.organization_entry = self.interface.get_object("organization_entry")
        self.copyright_entry = self.interface.get_object("copyright_entry")
        self.contact_entry = self.interface.get_object("contact_entry")
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
        taglist[gst.TAG_ARTIST] = self.artist_entry.get_text()
        taglist[gst.TAG_GENRE] = self.genre_entry.get_text()
        (year, month, day) = self.calendar.get_date()
        month +=1
        date = "%d-%d-%d" % (year, month, day)
        taglist[gst.TAG_DATE] = date
        taglist[gst.TAG_LOCATION] = self.location_entry.get_text()
        taglist[gst.TAG_ORGANIZATION] = self.organization_entry.get_text()
        taglist[gst.TAG_COPYRIGHT] = self.copyright_entry.get_text()
        taglist[gst.TAG_CONTACT] = self.contact_entry.get_text()
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
        artist = self.artist_entry.get_text()
        self.config.set_item(self.section, "artist", artist)
        genre = self.genre_entry.get_text()
        self.config.set_item(self.section, "genre", genre)
        location = self.location_entry.get_text()
        self.config.set_item(self.section, "location", location)
        organization = self.organization_entry.get_text()
        self.config.set_item(self.section, "organization", organization)
        copyright = self.copyright_entry.get_text()
        self.config.set_item(self.section, "copyright", copyright)
        contact = self.contact_entry.get_text()
        self.config.set_item(self.section, "contact", contact)

        buffer = self.textview.get_buffer()
        text = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter(), True
        )
        self.config.set_item(self.section, "description", text)

    def _load(self):
        title = self.config.get_item(self.section, "title")
        if title:
            self.title_entry.set_text(title)
        artist = self.config.get_item(self.section, "artist")
        if artist:
            self.artist_entry.set_text(artist)
        genre = self.config.get_item(self.section, "genre")
        if genre:
            self.genre_entry.set_text(genre)
        location = self.config.get_item(self.section, "location")
        if location:
            self.location_entry.set_text(location)
        organization = self.config.get_item(self.section, "organization")
        if organization:
            self.organization_entry.set_text(organization)
        copyright = self.config.get_item(self.section, "copyright")
        if copyright:
            self.copyright_entry.set_text(copyright)
        contact = self.config.get_item(self.section, "contact")
        if contact:
            self.contact_entry.set_text(contact)

        year = self.config.get_item(self.section, "year")
        month = self.config.get_item(self.section, "month")
        if year and month:
            self.calendar.select_month(int(month), int(year))
        day = self.config.get_item(self.section, "day")
        if day:
            self.calendar.select_day(int(day))

        description = self.config.get_item(self.section, "description")
        if description:
            buffer = gtk.TextBuffer()
            buffer.set_text(description)
            self.textview.set_buffer(buffer)
