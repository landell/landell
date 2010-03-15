# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
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

import registry
from mediaitem import MediaItem

class OutputItem(MediaItem):
    def __init__(self, name, factory):
        MediaItem.__init__(self, name, factory)
        self.converter = registry.registry.get_factories("converter")[0]
        self.encoding = registry.registry.get_factories("encoding")[0]
    def create_converter(self):
        item = self.converter.create()
        item.config(self.config)
        return item
    def create_encoding(self, type):
        item = self.encoding.create(type)
        item.config(self.config)
        return item
