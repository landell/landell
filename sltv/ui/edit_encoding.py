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
from sltv.settings import UI_DIR
import sltv.registry
import sltv.outputitem
from edit import Edit
import sltv.factory

class EditEncoding(Edit):
    def __init__(self, window, encodings):
        Edit.__init__(self, window, encodings)
        label = self.interface.get_object("name_label")
        label.set_label("Encoding name:")
        self.dialog.set_title("Edit Encoding")

        self.converter_factory = self.registry.get_factories("converter")[0]

        self.setting_box = self.converter_factory.get_ui().get_widget()
        self.container_box.add(self.setting_box)

    def set_media_item(self, media_item):
        self.media_item = media_item
        if self.media_item:
            self.set_factory(self.media_item.factory)
            self.name_entry.set_text(self.media_item.name)
            self.media_item.factory.get_ui().set_config(media_item.get_config())
            self.media_item.converter.get_ui().set_config(
                    media_item.get_config()
            )

    def _merge_dict(self, dict1, dict2):
        dict1.update(dict2)
        return dict1

    def save(self):
        if self.media_item == None:
            name = self.name_entry.get_text()
            if name == None or name == "":
                return False
            if not self.media_list.get_item(name):
                media_item = sltv.outputitem.OutputItem(name, self.factory)
                merged_config = self._merge_dict(
                        self.factory.get_ui().get_config(),
                        media_item.converter.get_ui().get_config()
                )
                media_item.set_config(merged_config)
                self.media_list.add_item(name, media_item)
        else:
            merged_config = self._merge_dict(
                    self.factory.get_ui().get_config(),
                    self.media_item.converter.get_ui().get_config()
            )
            self.media_item.set_config(merged_config)
        self.media_list.save()
