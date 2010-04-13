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

import gtk

class SaveButton(gtk.HBox):

    def __init__(self):
        gtk.HBox.__init__(self)

        self.entry = gtk.Entry()
        self.entry.set_editable(False)

        self.browse = gtk.Button("Browse")
        self.browse.connect("clicked", self.on_browse_press)

        self.pack_start(self.entry)
        self.pack_start(self.browse)

        self.file_chooser = gtk.FileChooserDialog(
            title = "Save",
            action = gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons = (
                gtk.STOCK_CANCEL,
                gtk.RESPONSE_CANCEL,
                gtk.STOCK_OPEN,
                gtk.RESPONSE_OK
            )
        )
        self.file_chooser.set_local_only(True)

        self.show_all()

    def on_browse_press(self, event):
        self.file_chooser.set_current_name(self.entry.get_text())
        response = self.file_chooser.run()
        if response == gtk.RESPONSE_OK:
            selected = self.file_chooser.get_filename()
            self.entry.set_text(selected)
        self.file_chooser.hide()

    def get_filename(self):
        return self.file_chooser.get_filename()

    def set_filename(self, filename):
        self.file_chooser.set_filename(filename)
        self.entry.set_text(filename)
