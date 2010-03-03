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
import source

class Sources:
    def __init__(self):
        self.liststore = gtk.ListStore(str, object)
        self.config = config.config
        self.registry = registry.registry

    def _find_source(self, name):
        for row in self.liststore:
            if row[0] == name:
                return row
        return None

    def get_source(self, name):
        row = self._find_source(name)
        return row[1]

    def remove_source(self, name):
        row = self._find_source(name)
        if row != None:
            self.liststore.remove(row.iter)
        self.config.remove_item("Sources", name)

    def add_source(self, name, source):
        self.liststore.append((name, source))
        factory = source.get_factory()
        items = source.get_config()
        items["type"] = factory.get_id()
        self.config.set_item("Sources", name, items)

    def get_store(self):
        return self.liststore

    def load(self):
        config_sources = self.config.get_section("Sources")
        if config_sources != None:
            # FIXME dict to list
            sources = [(v, k) for (k, v) in config_sources[0].iteritems()]
            for value, key in sources:
                if value and key:
                    factory = self.registry.get_factory_by_id(value["type"])
                    src = source.Source(key, factory)
                    src.set_config(value)
                    self.add_source(key, src)
