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

import gobject
import gtk
from landell.settings import UI_DIR
import landell.registry
from landell.registry import REGISTRY_VIDEO_CONVERTER
from edit import Edit
import landell.factory

class EditEncoding(Edit):
    def __init__(self, window, encodings, converters):
        Edit.__init__(self, window, encodings)
        for (name1, encoder) in encodings.liststore:
            for (name2, converter) in converters.liststore:
                if name1 == name2:
                    encoder.set_parent(converter)

        label = self.interface.get_object("name_label")
        label.set_label("Encoding name:")
        self.dialog.set_title("Edit Encoding")

        self.converter_factory = self.registry.get_factories(
            REGISTRY_VIDEO_CONVERTER
        )[0]

        self.setting_box = self.converter_factory.get_ui().get_widget()
        self.container_box.add(self.setting_box)

        self.converter_list = converters

    def set_media_item(self, media_item):
        self.media_item = media_item
        if self.media_item:
            self.converter = media_item.parent
            self.set_factory(self.media_item.factory)
            self.name_entry.set_text(self.media_item.name)
            self.media_item.factory.get_ui().set_config(media_item.get_config())
            self.converter.factory.get_ui().set_config(
                    self.converter.get_config()
            )

    def save(self):
        if self.media_item == None:
            name = self.name_entry.get_text()
            if name == None or name == "":
                return False
            if not self.media_list.get_item(name):
                media_item = landell.mediaitem.MediaItem(name, self.factory)
                converter = landell.mediaitem.MediaItem(
                        name, self.converter_factory
                )
                media_item.set_config(self.factory.get_ui().get_config().copy())
                converter.set_config(
                        self.converter_factory.get_ui().get_config().copy()
                )
                media_item.set_parent(converter)
                converter.set_parent(None)
                self.media_list.add_item(name, media_item)
                self.converter_list.add_item(name, converter)
        else:
            self.media_item.set_config(
                    self.factory.get_ui().get_config().copy()
            )
            self.converter.set_config(
                    self.converter_factory.get_ui().get_config().copy()
            )
        self.media_list.save()
        self.converter_list.save()
