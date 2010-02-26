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
        self.capabilities = None 
    def get_config(self):
        return self.config
    def get_id(self):
        return self.id
    def get_ui(self):
        return self.ui.get_widget()
    def get_name(self):
        return self.ui.get_name()
    def get_description(self):
        return self.ui.get_description()
    def get_capabilities(self):
        return self.capabilities

class FileInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.fileinput.CAPABILITIES
        self.id = "file"
        self.ui = ui.input.fileinput.FileInputUI()

    def new_input(self):
        inp = input.fileinput.FileInput()
        inp.config(self.get_config())
        return inp

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class V4L2InputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.v4l2input.CAPABILITIES
        self.id = "v4l2"
        self.ui = ui.input.v4l2input.V4L2InputUI()

    def new_input(self):
        inp = input.v4l2input.V4L2Input()
        inp.config(self.get_config())
        return inp

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.xinput.CAPABILITIES
        self.id = "x"
        self.ui = ui.input.xinput.XInputUI()

    def new_input(self):
        inp = input.xinput.XInput()
        inp.config(self.get_config())
        return inp

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class TestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.testinput.CAPABILITIES
        self.id = "test"
        self.ui = ui.input.testinput.TestInputUI()

    def new_input(self):
        inp = input.testinput.TestInput()
        inp.config(self.get_config())
        return inp

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class DVInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.dvinput.CAPABILITIES
        self.id = "dv"
        self.ui = ui.input.dvinput.DVInputUI()

    def new_input(self):
        inp = input.dvinput.DVInput()
        inp.config(self.get_config())
        return inp

    def get_config(self):
        self.config = self.ui.get_config()
        return self.config

class ALSAInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self)
        self.capabilities = input.alsainput.CAPABILITIES
        self.id = "alsa"
        self.ui = ui.input.alsainput.ALSAInputUI()
    def new_input(self):
        inp = input.alsainput.ALSAInput()
        inp.config(self.get_config())
        return inp
    def get_config(self):
        self.config = self.ui.get_config()
        return self.config
