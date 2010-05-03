# -*- coding: utf-8 -*-
# Copyright (C) 2009 Holoscópio Tecnologia
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
import pygst
pygst.require("0.10")
import gst
from audio import *
from preview import *
from swap import Swap

import medialist
import effect
import volume

MEDIA_AUDIO = 1
MEDIA_VIDEO = 2

class Sltv(gobject.GObject):

    def __init__(self):
        gobject.GObject.__init__(self)
        gobject.signal_new("stopped", Sltv, gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE, ())
        gobject.signal_new("playing", Sltv, gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE, ())
        gobject.signal_new("preplay", Sltv, gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE, ())
        gobject.signal_new("error", Sltv, gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE, (gobject.TYPE_STRING,))
        gobject.signal_new("sync-message", Sltv, gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE, (gobject.type_from_name("GstBus"),
                                               gobject.type_from_name("GstMessage")))


        self.player = None
        self.preview = Preview(self)
        self.preview_enabled = False

        self.outputs = medialist.MediaList("Outputs", "output")
        self.outputs.load()

        self.sources = medialist.MediaList("Sources", "input")
        self.sources.load()

        self.encoders = medialist.MediaList("Encoders", "encoding")
        self.encoders.load()

        self.videoconverters = medialist.MediaList(
                "VideoConverters", "videoconverter"
        )
        self.videoconverters.load()

        self.audio = Audio()

        self.effect_enabled = False
        self.effect = {}
        self.effect_name = {MEDIA_VIDEO: "identity", MEDIA_AUDIO: "identity"}

        self.video_source = None
        self.audio_source = None

        self.overlay_text = None
        self.volume = None
        self.volume_value = None

        self.pending_state = None

        self.input_type = 0

    def set_overlay_text(self, overlay_text):
        self.overlay_text = overlay_text
        if self.playing():
            self.overlay.set_property("text", overlay_text)

    def set_effect_name(self, effect_type, effect_name):
        if effect_name == "none":
            effect_name = "identity"
        self.effect_name[effect_type] = effect_name

    def play(self):

        self.emit("preplay")

        self.player = gst.Pipeline("player")

        self.queue_video = gst.element_factory_make("queue", "queue_video")
        self.player.add(self.queue_video)

        self.input_type = 0

        # Source selection

        self.video_input_selector = gst.element_factory_make(
                "input-selector", "video_input_selector"
        )
        self.player.add(self.video_input_selector)
        self.source_pads = {}

        type = 0

        for row in self.sources.get_store():
            (name, source) = row
            element = source.create()

            if element.does_audio():
                if name == self.audio_source:
                    self.player.add(element)
                    self.queue_audio = gst.element_factory_make("queue", "queue_audio")
                    self.player.add(self.queue_audio)
                    pad = self.queue_audio.get_static_pad("sink")
                    element.audio_pad.link(pad)
                    self.input_type |= MEDIA_AUDIO
                elif element.does_video():

                        # If element does audio and video, it will be added.
                        # If audio is not chosen, it should be dropped

                        self.player.add(element)
                        fakesink = gst.element_factory_make("fakesink", None)
                        fakesink.set_property("silent", True)
                        fakesink.set_property("sync", False)
                        self.player.add(fakesink)
                        element.audio_pad.link(fakesink.get_static_pad("sink"))

            if element.does_video():
                self.input_type |= MEDIA_VIDEO
                if not element.does_audio():
                    self.player.add(element)
                self.source_pads[name] = \
                    self.video_input_selector.get_request_pad("sink%d")
                element.video_pad.link(self.source_pads[name])

            if name == self.video_source:
                type |= element.get_type()
            if name == self.audio_source:
                type |= element.get_type()

        self.video_input_selector.link(self.queue_video)
        self.video_input_selector.set_property(
                "active_pad", self.source_pads[self.video_source]
        )

        self.effect[MEDIA_VIDEO] = effect.video_effect.VideoEffect(
                self.effect_name[MEDIA_VIDEO]
        )
        self.player.add(self.effect[MEDIA_VIDEO])

        self.overlay = gst.element_factory_make("textoverlay", "overlay")
        self.overlay.set_property("font-desc", "Sans Bold 14")
        self.player.add(self.overlay)

        gst.element_link_many(
                self.queue_video, self.effect[MEDIA_VIDEO], self.overlay
        )

        self.preview_tee = gst.element_factory_make("tee", "tee")
        self.player.add(self.preview_tee)

        self.overlay.link(self.preview_tee)

        if self.input_type & MEDIA_AUDIO:
            self.convert = gst.element_factory_make("audioconvert", "convert")
            self.player.add(self.convert)

            self.effect[MEDIA_AUDIO] = effect.audio_effect.AudioEffect(
                    self.effect_name[MEDIA_AUDIO]
            )
            self.player.add(self.effect[MEDIA_AUDIO])

            self.audio_tee = gst.element_factory_make("tee", "audio_tee")
            self.player.add(self.audio_tee)

            self.volume = volume.Volume()
            self.player.add(self.volume)

            gst.element_link_many(
                    self.queue_audio, self.volume, self.effect[MEDIA_AUDIO],
                    self.convert, self.audio_tee
            )
        added_encoders = {}

        for row in self.outputs.get_store():
            (name, output) = row

            sink = output.create()
            self.player.add(sink)

            encoder_name = output.get_config()["parent"]
            encoder_item = self.encoders.get_item(encoder_name)
            if encoder_item is None:
                pass

            if added_encoders.has_key(encoder_name):
                tee = added_encoders[encoder_name]

                tee_queue = gst.element_factory_make("queue", None)
                self.player.add(tee_queue)

                gst.element_link_many(tee, tee_queue, sink)
            else:
                queue_output = gst.element_factory_make("queue", None)
                self.player.add(queue_output)

                tee = gst.element_factory_make("tee", None)
                self.player.add(tee)

                converter = encoder_item.parent.create()
                self.player.add(converter)

                encoder = encoder_item.factory.create(type)
                encoder.config(encoder_item.config)
                self.player.add(encoder)

                tee_queue = gst.element_factory_make("queue", None)
                self.player.add(tee_queue)

                added_encoders[encoder_name] = tee
                gst.element_link_many(
                        self.preview_tee, queue_output, converter, encoder, tee,
                        tee_queue, sink
                )

                if self.input_type & MEDIA_AUDIO:
                    audio_queue = gst.element_factory_make("queue", None)
                    self.player.add(audio_queue)

                    gst.element_link_many(self.audio_tee, audio_queue, encoder)

        if self.preview_enabled:
            queue_preview = gst.element_factory_make("queue", "queue_preview")
            self.player.add(queue_preview)
            self.preview_element = self.preview.get_preview()
            self.player.add(self.preview_element)
            err = gst.element_link_many(
                    self.preview_tee, queue_preview, self.preview_element
            )
            if err == False:
                print "Error conecting preview"

        self.overlay.set_property("text", self.overlay_text)
        if self.volume_value is not None:
            self.volume.set_property("volume", self.volume_value)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        cr = self.player.set_state(gst.STATE_PLAYING)
        if cr == gst.STATE_CHANGE_SUCCESS:
            self.emit("playing")
        elif cr == gst.STATE_CHANGE_ASYNC:
            self.pending_state = gst.STATE_PLAYING

    def stop(self):
        cr = self.player.set_state(gst.STATE_NULL)
        if cr == gst.STATE_CHANGE_SUCCESS:
            self.emit("stopped")
        elif cr == gst.STATE_CHANGE_ASYNC:
            self.pending_state = gst.STATE_NULL

    def playing(self):
        return self.player and self.player.get_state()[1] == gst.STATE_PLAYING

    def _swap_effect(self, effect_type):
            if effect_type == MEDIA_VIDEO:
                new_effect = effect.video_effect.VideoEffect(
                        self.effect_name[effect_type]
                )
                Swap.swap_element(
                        self.player, self.queue_video, self.overlay,
                        self.effect[effect_type], new_effect
                )
                self.effect[effect_type] = new_effect
            else:
                new_effect = effect.audio_effect.AudioEffect(
                        self.effect_name[effect_type]
                )
                Swap.swap_element(
                        self.player, self.volume, self.convert,
                        self.effect[effect_type], new_effect
                )
                self.effect[effect_type] = new_effect

    def set_effects(self, state):

        self.effect_enabled = state

        # If state is disabled and pipeline is playing, disable effects now

        if not self.effect_enabled:
            if self.playing():
                self.change_effect("identity", MEDIA_VIDEO)
                self.change_effect("identity", MEDIA_AUDIO)

    def change_effect(self, effect_name, effect_type):

        # If that input doesn't exist, then there is no effect to change.

        if not self.input_type & effect_type:
            return

        if self.playing():
            self.set_effect_name(effect_type, effect_name)
            self._swap_effect(effect_type)

    def switch_source(self):
        self.video_input_selector.set_property(
                "active-pad", self.source_pads[self.video_source]
        )

    def set_video_source(self, source_name):
        self.video_source = source_name
        if self.playing():
            self.switch_source()

    def set_audio_source(self, source_name):
        self.audio_source = source_name

    def set_preview(self, state):
        self.preview_enabled = state

    def set_volume(self, value):
        self.volume_value = value
        if self.volume:
            self.volume.set_property("volume", value)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            cr = self.player.set_state(gst.STATE_NULL)
            if cr == gst.STATE_CHANGE_SUCCESS:
                self.emit("stopped")
            elif cr == gst.STATE_CHANGE_ASYNC:
                self.pending_state = gst.STATE_NULL
        elif t == gst.MESSAGE_ERROR:
            (gerror, debug) = message.parse_error()
            self.emit("error", gerror.message)
            print debug
            cr = self.player.set_state(gst.STATE_NULL)
            if cr == gst.STATE_CHANGE_SUCCESS:
                self.emit("stopped")
            elif cr == gst.STATE_CHANGE_ASYNC:
                self.pending_state = gst.STATE_NULL
        elif t == gst.MESSAGE_ASYNC_DONE:
            if self.pending_state == gst.STATE_NULL:
                self.emit("stopped")
            elif self.pending_state == gst.STATE_PLAYING:
                self.emit("playing")
            self.pending_state = None

    def on_sync_message(self, bus, message):
        self.emit("sync-message", bus, message)
