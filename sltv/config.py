# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
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

from configobj import ConfigObj
import os

class Config:

    def __init__(self):
        self.filename = os.path.expanduser("~/.sltv")
        self.config = ConfigObj(self.filename)

    def get_filename(self):
        return self.filename

    def set_filename(self, name):
        self.filename = name

    def insert_section(self, section):
        self.config[section] = {}
        self.save()

    def set_item(self, section, item_name, item_value):
        if section not in self.config.keys():
            self.insert_section(section)
        self.config[section][item_name] = item_value
        self.save()

    def remove_item(self, section, item_name):
        self.config[section].pop(item_name)
        self.save()

    def get_section(self, section):
        if section in self.config.keys():
            return self.config.as_list(section)
        else:
            return None

    def save(self):
        self.config.write()

config = Config()
