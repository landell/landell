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
from medialist import MediaListUI
from sltv.settings import UI_DIR
import edit_output

class Outputs(MediaListUI):
    def __init__(self, ui, outputs, encoders):
        MediaListUI.__init__(self, ui, outputs)
        self.dialog.set_title("Outputs")
        self.edit_item = edit_output.EditOutput(self.dialog, self.media_list, encoders)

        # Adding types to combobox

        factories = self.registry.get_factories("output")

        for factory in factories:
            self.elements_liststore.append((factory.get_name(),))
            self.factories[factory.get_name()] = factory
        self.elements_combobox.set_active(0)
