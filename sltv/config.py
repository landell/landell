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

    def remove_section(self, section):
        if self.has_section(section):
            self.config.pop(section)
            self.save()

    def get_section(self, section):
        if self.has_section(section):
            # FIXME: change it to as_list in configobj 4.7
            return list([self.config.get(section)])
        else:
            return None

    def has_section(self, section):
        if section in self.config.keys():
            return True
        else:
            return False

    def has_item(self, section, item_name):
        if self.has_section(section):
            if item_name in self.config[section].keys():
                return True
            else:
                return False
        return False

    def get_item(self, section, item_name):
        return config[section][item_name]

    def save(self):
        self.config.write()

config = Config()
