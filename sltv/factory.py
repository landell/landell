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

import input
import ui.input

class InputFactory:
    def __init__(self):
        self.config = {}
        self.id = ""
    def get_config(self):
        return self.config
    def get_id(self):
        return self.id
    def get_ui(self):
        return self.ui.get_widget()

class FileInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "file"
        self.ui = ui.input.fileinput.FileInputUI()

    def new_input(self):
        inp = input.fileinput.FileInput()
        inp.config(self.get_config())
        return inp

    def get_name(self):
        return "File"

    def get_description(self):
        return "Get Video from file"

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class V4L2InputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "v4l2"
        self.ui = ui.input.v4l2input.V4L2InputUI()

    def new_input(self):
        inp = input.v4l2input.V4L2Input()
        inp.config(self.get_config())
        return inp

    def get_name(self):
        return "V4L2 + autoaudio"

    def get_description(self):
        return "Get Video from V4L2 and Audio from autoaudio"

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "x"
        self.ui = ui.input.xinput.XInputUI()

    def new_input(self):
        inp = input.xinput.XInput()
        inp.config(self.get_config())
        return inp

    def get_name(self):
        return "XImageSrc"

    def get_description(self):
        return "Get Video from Desktop and Audio from ALSA"

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class TestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "test"
        self.ui = ui.input.testinput.TestInputUI()

    def new_input(self):
        inp = input.testinput.TestInput()
        inp.config(self.get_config())
        return inp

    def get_name(self):
        return "Test"

    def get_description(self):
        return "Video and Audio from test sources"

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class DVInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.id = "dv"
        self.ui = ui.input.dvinput.DVInputUI()

    def new_input(self):
        inp = input.dvinput.DVInput()
        inp.config(self.get_config())
        return inp

    def get_name(self):
        return "DV Firewire"

    def get_description(self):
        return "Get video and audio from Firewire DV"

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config
