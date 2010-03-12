# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Marcelo Jorge Vieira <metal@holoscopio.com>
# Author: Thadeu Lima de Souza Cascardo <cascardo@holoscopio.com>
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
import output
import encoding
import videoconverter
import ui.input
import ui.output
import ui.encoding
import ui.videoconverter
import registry

class SltvFactory:
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
    def create(self):
        return self.factory_class()

class FileInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "file")
        self.capabilities = input.fileinput.CAPABILITIES
        self.ui = ui.input.fileinput.FileInputUI()
        self.factory_class = input.fileinput.FileInput

class V4L2InputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "v4l2")
        self.capabilities = input.v4l2input.CAPABILITIES
        self.ui = ui.input.v4l2input.V4L2InputUI()
        self.factory_class = input.v4l2input.V4L2Input

class XInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "x")
        self.capabilities = input.xinput.CAPABILITIES
        self.ui = ui.input.xinput.XInputUI()
        self.factory_class = input.xinput.XInput

class VideoTestInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "videotest")
        self.capabilities = input.videotestinput.CAPABILITIES
        self.ui = ui.input.videotestinput.VideoTestInputUI()
        self.factory_class = input.videotestinput.VideoTestInput

class AudioTestInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "audiotest")
        self.capabilities = input.audiotestinput.CAPABILITIES
        self.ui = ui.input.audiotestinput.AudioTestInputUI()
        self.factory_class = input.audiotestinput.AudioTestInput

class DVInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "dv")
        self.capabilities = input.dvinput.CAPABILITIES
        self.ui = ui.input.dvinput.DVInputUI()
        self.factory_class = input.dvinput.DVInput

class ALSAInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "alsa")
        self.capabilities = input.alsainput.CAPABILITIES
        self.ui = ui.input.alsainput.ALSAInputUI()
        self.factory_class = input.alsainput.ALSAInput

class PulseInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "pulse")
        self.capabilities = input.pulseinput.CAPABILITIES
        self.ui = ui.input.pulseinput.PulseInputUI()
        self.factory_class = input.pulseinput.PulseInput

class AutoAudioInputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "auto")
        self.capabilities = input.autoaudioinput.CAPABILITIES
        self.ui = ui.input.autoaudioinput.AutoAudioInputUI()
        self.factory_class = input.autoaudioinput.AutoAudioInput

class IcecastOutputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "icecast")
        self.ui = ui.output.icecastoutput.IcecastOutputUI()
        self.factory_class = output.icecastoutput.IcecastOutput

class FileOutputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "file")
        self.ui = ui.output.fileoutput.FileOutputUI()
        self.factory_class = output.fileoutput.FileOutput

class FakeOutputFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "fake")
        self.ui = ui.output.fakeoutput.FakeOutputUI()
        self.factory_class = output.fakeoutput.FakeOutput

class VideoConverterFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "videoconv")
        self.ui = ui.videoconverter.VideoConverterUI()
        self.factory_class = videoconverter.VideoConverter

class OggTheoraVorbisEncodingFactory(SltvFactory):
    def __init__(self):
        SltvFactory.__init__(self, "encoding")
        self.ui = ui.encoding.oggtheoravorbisenc.OggTheoraVorbisEncodingUI()
        self.factory_class = encoding.oggtheoravorbisenc.OggTheoraVorbisEncoder

input_factories = [
        AudioTestInputFactory(), XInputFactory(), V4L2InputFactory(),
        FileInputFactory(), DVInputFactory(), ALSAInputFactory(),
        VideoTestInputFactory(), PulseInputFactory(), AutoAudioInputFactory()
]

for i in input_factories:
    registry.registry.register_factory("input", i)

output_factories = [
        IcecastOutputFactory(), FileOutputFactory(), FakeOutputFactory()
]

for i in output_factories:
    registry.registry.register_factory("output", i)
