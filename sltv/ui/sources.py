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
import edit_source

from sltv.input.core import INPUT_TYPE_VIDEO, INPUT_TYPE_AUDIO
from sltv.registry import REGISTRY_INPUT

class VideoModel:
    def __init__(self, sources):
        self.model = sources.get_store().filter_new()
        self.model.set_visible_func(self.filter)
    def filter(self, model, iter):
        source = model.get_value(iter, 1)
        return source != None and \
            source.factory.get_capabilities() & INPUT_TYPE_VIDEO > 0

class AudioModel:
    def __init__(self, sources):
        self.model = sources.get_store().filter_new()
        self.model.set_visible_func(self.filter)
    def filter(self, model, iter):
        source = model.get_value(iter, 1)
        return source != None and \
            source.factory.get_capabilities() & INPUT_TYPE_AUDIO > 0

class Sources(MediaListUI):
    def __init__(self, ui, sources, audioconvs):
        MediaListUI.__init__(self, ui, sources)
        self.audioconvs = audioconvs
        self.edit_item = edit_source.EditSource(
                self.dialog, self.media_list, self.audioconvs
        )

        # Adding types to combobox

        factories = self.registry.get_factories(REGISTRY_INPUT)

        for factory in factories:
            self.elements_liststore.append((factory.get_name(),))
            self.factories[factory.get_name()] = factory

        self.elements_combobox.set_active(0)
