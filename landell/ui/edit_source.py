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

import gi
from gi.repository import Gtk
from landell.settings import UI_DIR
import landell.registry
import landell.mediaitem
from edit import Edit

class EditSource(Edit):
    def __init__(self, window, sources, audioconvs):
        Edit.__init__(self, window, sources)
        for (name1, source) in sources.liststore:
            source.set_parent(None)
            for (name2, audio) in audioconvs.liststore:
                if name1 == name2:
                    source.set_parent(audio)

        label = self.interface.get_object("name_label")
        label.set_label("Source name:")
        self.dialog.set_title("Edit Source")
        self.audio_list = audioconvs

    def set_media_item(self, media_item):
        self.media_item = media_item
        if self.media_item:
            if media_item.parent:
                self.audio = media_item.parent
                self.audio.factory.get_ui().set_config(
                        self.audio.get_config()
                )
            self.set_factory(self.media_item.factory)
            self.name_entry.set_text(self.media_item.name)
            self.media_item.factory.get_ui().set_config(media_item.get_config())


    def save(self):
        if self.media_item == None:
            name = self.name_entry.get_text()
            if name == None or name == "":
                return False
            if not self.media_list.get_item(name):
                media_item = landell.mediaitem.MediaItem(name, self.factory)
                media_item.set_config(self.factory.get_ui().get_config().copy())
                if self.audio_config:
                    audio = landell.mediaitem.MediaItem(
                            name, self.audio_factory
                    )
                    audio.set_config(
                            self.audio_factory.get_ui().get_config().copy()
                    )

                    media_item.set_parent(audio)
                    audio.set_parent(None)
                    self.audio_list.add_item(name, audio)
                else:
                    media_item.set_parent(None)
                self.media_list.add_item(name, media_item)
        else:
            self.media_item.set_config(
                    self.factory.get_ui().get_config().copy()
            )
            if self.audio_config:
                self.audio.set_config(
                        self.audio_factory.get_ui().get_config().copy()
                )
        self.media_list.save()
        if self.audio_config:
            self.audio_list.save()
