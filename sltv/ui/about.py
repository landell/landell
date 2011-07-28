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

import gtk
from sltv.settings import VERSION, ICON

class About:

    def __init__(self, ui):
        self.about = gtk.AboutDialog()
        self.about.set_transient_for(ui.main_window)
        self.about.set_destroy_with_parent(True)
        self.about.connect("response", self.on_close_dialog)
        self.about.connect("delete_event", self.on_close_dialog)
        self.create_about()

    def create_about(self):
        self.about.set_name("Landell")
        self.about.set_copyright("Copyright (c) 2010 Holoscópio Tecnologia")
        self.about.set_version(VERSION)
        self.about.set_logo(gtk.gdk.pixbuf_new_from_file(ICON))
        self.about.set_website("http://landell.holoscopio.com/")
        self.about.set_wrap_license(False)
        self.about.set_license(
            "This program is free software; you can redistribute it and/or modify\n"
            "it under the terms of the GNU General Public License as published by\n"
            "the Free Software Foundation; either version 2 of the License, or\n"
            "(at your option) any later version.\n"
            "\n"
            "This program is distributed in the hope that it will be useful,\n"
            "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
            "GNU General Public License for more details.\n"
            "\n"
            "You should have received a copy of the GNU General Public License along\n"
            "with this program; if not, write to the Free Software Foundation, Inc.,\n"
            "51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.\n"
        )
        authors = [
            "Luciana Fujii Pontello <luciana@holoscopio.com>",
            "Marcelo Jorge Vieira <marcelo@holoscopio.com>",
            "Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>"
        ]
        self.about.set_authors(authors)
        artists = [
            "Valessio Brito <contato@valessiobrito.info>"
        ]
        self.about.set_artists(artists)

    def show_window(self):
        self.about.show_all()
        self.about.run()

    def on_close_dialog(self, dialog, response):
        if response == gtk.RESPONSE_CANCEL or \
           response == gtk.RESPONSE_DELETE_EVENT:
            dialog.hide_all()
