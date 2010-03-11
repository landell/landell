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

class EditOutput(Edit):
    def __init__(self, window, outputs):
        Edit.__init__(self, window, outputs)
        label = self.interface.get_object("name_label")
        label.set_label("Output name:")
        self.dialog.set_title("Edit Output")

        self.output_label = self.interface.get_object("output_label")
        self.output_label.show()
        self.output_separator = self.interface.get_object("output_separator")
        self.output_separator.show()

        self.encoding_label = self.interface.get_object("encoding_label")
        self.encoding_label.show()
        self.encoding_separator = self.interface.get_object("encoding_separator")
        self.encoding_separator.show()

        self.output_box = self.interface.get_object("output_box")
        self.setting_interface = gtk.Builder()
        self.setting_interface.add_from_file(UI_DIR + "/output_setting.ui")
        self.setting_box = self.setting_interface.get_object("setting_box")
        self.output_box.add(self.setting_box)

        self.encoding_box = self.interface.get_object("encoding_box")
        self.encoding_interface = gtk.Builder()
        self.encoding_interface.add_from_file(UI_DIR + "/encoding/theora.ui")
        self.theora_box = self.encoding_interface.get_object("theora_box")
        self.encoding_box.add(self.theora_box)

        factories = self.registry.get_factories("output")

        for factory in factories:
            self.elements_liststore.append((factory.get_name(),))
            self.factories[factory.get_name()] = factory

        self.elements_combobox.set_active(0)
        self.set_current_factory()
