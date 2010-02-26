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

class Message():

    def __init__(self, message="", ui=None, message_type=gtk.MESSAGE_INFO):
        self.ui = ui
        self.message_type = message_type
        self.message = message
        self.buttons = gtk.BUTTONS_OK

    def popup(self):
        dialog = gtk.MessageDialog(
            self.ui.main_window,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            self.message_type,
            self.buttons,
            self.message
        )
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def set_message(self, message):
        self.message = message

    def set_message_type(self, message_type):
        self.message_type = message_type

    def set_buttons(self, buttons):
        self.buttons = buttons

    def set_ui(self, ui):
        self.ui = ui

class MessageError(Message):
    def __init__(self, message, ui):
        Message.__init__(self, message, ui, gtk.MESSAGE_ERROR)
        self.popup()

class MessageWarning(Message):
    def __init__(self, message, ui):
        Message.__init__(self, message, ui, gtk.MESSAGE_WARNING)
        self.popup()

class MessageInfo(Message):
    def __init__(self, message, ui):
        Message.__init__(self, message, ui, gtk.MESSAGE_INFO)
        self.popup()

class MessageQuestion(Message):
    def __init__(self, message, ui):
        Message.__init__(self, message, ui, gtk.MESSAGE_QUESTION)
        self.popup()
