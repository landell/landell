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
import sltv.mediaitem
from edit import Edit

class EditSource(Edit):
    def __init__(self, window, sources):
        Edit.__init__(self, window, sources)
        label = self.interface.get_object("name_label")
        label.set_label("Source name")

        factories = self.registry.get_factories("input")

        for factory in factories:
            self.elements_liststore.append((factory.get_name(),))
            self.factories[factory.get_name()] = factory

        self.elements_combobox.set_active(0)
        self.set_factory(factories[0])

    def save(self):
        config = self.factory.get_ui().get_config()
        if self.media_item == None:
            name = self.name_entry.get_text()
            if name == None or name == "":
                return False
            if not self.media_list.config.has_item("Sources", name):
                media_item = sltv.mediaitem.MediaItem(name, self.factory)
                media_item.set_config(self.factory.get_ui().get_config())
                self.media_list.add_item(name, media_item)
        else:
            self.media_item.set_config(config)
        self.media_list.save()
