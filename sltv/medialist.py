# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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
import registry
import config
import mediaitem
import outputitem
import factory

class MediaList:
    def __init__(self, section, type):
        self.liststore = gtk.ListStore(str, object)
        self.config = config.config
        self.registry = registry.registry
        self.section = section
        self.type = type

    def _find_item(self, name):
        for row in self.liststore:
            if row[0] == name:
                return row
        return None

    def get_item(self, name):
        row = self._find_item(name)
        if row == None:
            return None
        return row[1]

    def remove_item(self, name):
        row = self._find_item(name)
        if row != None:
            self.liststore.remove(row.iter)

    def _save_item(self, name, item):
        factory = item.get_factory()
        items = item.get_config()
        items["type"] = factory.get_id()
        self.config.set_item(self.section, name, items)

    def add_item(self, name, item):
        self.liststore.append((name, item))

    def get_store(self):
        return self.liststore

    def load(self):
        config_items = self.config.get_section(self.section)
        if config_items != None:
            # FIXME dict to list
            items = [(v, k) for (k, v) in config_items[0].iteritems()]
            for value, key in items:
                if value and key:
                    current_factory = self.registry.get_factory_by_id(
                            self.type, value["type"]
                    )
                    if "output" in self.type:
                        src = outputitem.OutputItem(key, current_factory)
                    else:
                        src = mediaitem.MediaItem(key, current_factory)
                    src.set_config(value)
                    self.add_item(key, src)

    def save(self):
        self.config.remove_section(self.section)
        for row in self.liststore:
            self._save_item(row[0], row[1])
