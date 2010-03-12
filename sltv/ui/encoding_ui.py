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

import sltv.encoding

class EncodingUI:

    def __init__(self, ui):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/encoding.ui")
        self.dialog = self.interface.get_object("dialog1")
        self.dialog.set_transient_for(ui.main_window)

        #Encoding selection
        dv_radiobutton = self.interface.get_object("dv_radiobutton")
        theora_radiobutton = self.interface.get_object("theora_radiobutton")
        encoding_action_group = gtk.ActionGroup("encoding_action_group")
        action_entries = [
            ("theora_action", None, "Ogg Theora", None,
                "Ogg Theora encoding", 0),
            ("dv_action", None, "DV", None, "Uncompressed DV", 1)
        ]
        encoding_action_group.add_radio_actions(
            action_entries, 0, self.encoding_changed, None
        )
        theora_action = encoding_action_group.get_action("theora_action")
        theora_action.connect_proxy(theora_radiobutton)
        dv_action = encoding_action_group.get_action("dv_action")
        dv_action.connect_proxy(dv_radiobutton)
        self.encoding_selection = "theora"

        close_button = self.interface.get_object("close_button")
        close_button.connect("clicked", self.close_dialog)
        self.dialog.connect("delete_event", self.close_dialog)

    def show_window(self):
        self.dialog.show_all()
        self.dialog.run()

    def get_mux(self, type):
        if self.encoding_selection == "theora":
            self.mux = sltv.encoding.oggtheoravorbisenc.OggTheoraVorbisEncoder(type)
        if self.encoding_selection == "dv":
            self.mux = sltv.encoding.dvenc.DVEncoder(type)
        return self.mux

    def close_dialog(self, button, data = None):
        self.dialog.hide_all()

    def encoding_changed(self, radioaction, current):
        if current.get_name() == "theora_action":
            self.encoding_selection = "theora"
        if current.get_name() == "dv_action":
            self.encoding_selection = "dv"
