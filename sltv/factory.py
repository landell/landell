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
import registry

class InputFactory:
    def __init__(self, id):
        self.id = id
        self.capabilities = None 
    def get_id(self):
        return self.id
    def get_ui(self):
        return self.ui
    def get_name(self):
        return self.ui.get_name()
    def get_description(self):
        return self.ui.get_description()
    def get_capabilities(self):
        return self.capabilities
    def new_input(self):
        return self.input_class()

class FileInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "file")
        self.capabilities = input.fileinput.CAPABILITIES
        self.ui = ui.input.fileinput.FileInputUI()
        self.input_class = input.fileinput.FileInput

class V4L2InputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "v4l2")
        self.capabilities = input.v4l2input.CAPABILITIES
        self.ui = ui.input.v4l2input.V4L2InputUI()
        self.input_class = input.v4l2input.V4L2Input

class XInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "x")
        self.capabilities = input.xinput.CAPABILITIES
        self.ui = ui.input.xinput.XInputUI()
        self.input_class = input.xinput.XInput

class VideoTestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "videotest")
        self.capabilities = input.videotestinput.CAPABILITIES
        self.ui = ui.input.videotestinput.VideoTestInputUI()
        self.input_class = input.videotestinput.VideoTestInput

class AudioTestInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "audiotest")
        self.capabilities = input.audiotestinput.CAPABILITIES
        self.ui = ui.input.audiotestinput.AudioTestInputUI()
        self.input_class = input.audiotestinput.AudioTestInput

class DVInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "dv")
        self.capabilities = input.dvinput.CAPABILITIES
        self.ui = ui.input.dvinput.DVInputUI()
        self.input_class = input.dvinput.DVInput

class ALSAInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "alsa")
        self.capabilities = input.alsainput.CAPABILITIES
        self.ui = ui.input.alsainput.ALSAInputUI()
        self.input_class = input.alsainput.ALSAInput

class PulseInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "pulse")
        self.capabilities = input.pulseinput.CAPABILITIES
        self.ui = ui.input.pulseinput.PulseInputUI()
        self.input_class = input.pulseinput.PulseInput

class AutoAudioInputFactory(InputFactory):
    def __init__(self):
        InputFactory.__init__(self, "auto")
        self.capabilities = input.autoaudioinput.CAPABILITIES
        self.ui = ui.input.autoaudioinput.AutoAudioInputUI()
        self.input_class = input.autoaudioinput.AutoAudioInput

factories = [
        AudioTestInputFactory(), XInputFactory(), V4L2InputFactory(),
        FileInputFactory(), DVInputFactory(), ALSAInputFactory(),
        VideoTestInputFactory(), PulseInputFactory(), AutoAudioInputFactory()
]

for i in factories:
    registry.registry.register_factory(i)
