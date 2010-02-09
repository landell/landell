# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
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

class About:

    def __init__(self, window):
        self.about = gtk.AboutDialog()
        self.about.set_transient_for(window)
        self.about.connect("response", self.on_close_dialog)
        self.about.connect("delete_event", self.on_close_dialog)
        self.create_about()

    def create_about(self):
        self.about.set_name("SLTV")
        self.about.set_copyright("Copyright 2010 Holoscopio Tecnologia")
        self.about.set_version("0.1")
        self.about.set_website("https://wiki.softwarelivre.org/TV/ProjetoSLTV")
        self.about.set_wrap_license(True)
        self.about.set_license(
            "This program is free software; you can redistribute it and/or modify"
            "it under the terms of the GNU General Public License as published by"
            "the Free Software Foundation; either version 2 of the License, or"
            "(at your option) any later version."

            "This program is distributed in the hope that it will be useful,"
            "but WITHOUT ANY WARRANTY; without even the implied warranty of"
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
            "GNU General Public License for more details."

            "You should have received a copy of the GNU General Public License along"
            "with this program; if not, write to the Free Software Foundation, Inc.,"
            "51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."
        )
        authors = [
            "Luciana Fujii Pontello <luciana@holoscopio.com>",
            "Marcelo Jorge Vieira <marcelo@holoscopio.com>",
            "Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>"
        ]
        self.about.set_authors(authors)

    def show_window(self):
        self.about.show_all()
        self.about.run()

    def on_close_dialog(self, dialog, response):
        if response == gtk.RESPONSE_CANCEL or \
           response == gtk.RESPONSE_DELETE_EVENT:
            dialog.hide_all()
