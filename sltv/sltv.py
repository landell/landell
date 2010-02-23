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
import gtk
from output import *
from encoding import *
from audio import *
from preview import *
from effects import *
from video_switch import *
from swap import *


class Sltv:

    def __init__(self, preview_area, window):
        self.player = None
        self.preview = Preview(preview_area)

        self.encoding = Encoding(window)
        self.output = Output(window)
        self.audio = Audio()
        self.video_switch = VideoSwitch(window)

        self.effect_enabled = "False"
        self.effect = {}
        self.effect_name = {}

    def show_encoding(self):
        self.encoding.show_window()

    def show_output(self):
        self.output.show_window()

    def show_video_switch(self):
        self.video_switch.show_window()

    def play(self, overlay_text, video_effect_name,
            audio_effect_name, liststore, source_name):

        self.player = gst.Pipeline("player")

        self.queue_video = gst.element_factory_make("queue", "queue_video")
        self.queue_audio = gst.element_factory_make("queue", "queue_audio")
        self.player.add(self.queue_video, self.queue_audio)

        self.convert = gst.element_factory_make("audioconvert", "convert")
        self.player.add(self.convert)

        # Source selection

        iter = liststore.get_iter_first()
        while iter != None:
            if liststore.get_value(iter, 0) == source_name:
                self.input = liststore.get_value(iter, 1)
                break
            iter = liststore.iter_next(iter)
        self.player.add(self.input)
        self.input.audio_pad.link(self.queue_audio.get_pad("sink"))
        self.input.video_pad.link(self.queue_video.get_pad("sink"))

        self.overlay = gst.element_factory_make("textoverlay", "overlay")
        self.tee = gst.element_factory_make("tee", "tee")
        queue1 = gst.element_factory_make("queue", "queue1")
        queue2 = gst.element_factory_make("queue", "queue2")
        self.videorate = gst.element_factory_make("videorate", "videorate")
        self.videoscale = gst.element_factory_make("videoscale", "videoscale")
        self.mux = self.encoding.get_mux()
        self.sink = self.output.get_output()
        self.preview_element = self.preview.get_preview()
        self.colorspace = gst.element_factory_make(
            "ffmpegcolorspace", "colorspacesink"
        )
        self.videoscale.set_property("method",1)

        if self.effect_enabled:
            self.effect_name['video'] = video_effect_name
            self.effect_name['audio'] = audio_effect_name
        else:
            self.effect_name['video'] = "identity"
            self.effect_name['audio'] = "identity"
        self.effect['video'] = Effect.make_effect(self.effect_name['video'], "video")
        self.effect['audio'] = Effect.make_effect(self.effect_name['audio'], "audio")
        self.player.add(self.effect['video'], self.effect['audio'])

        self.player.add(
            self.overlay, self.tee, queue1, self.videorate, self.videoscale,
            self.colorspace, self.mux, self.sink
        )
        gst.element_link_many(self.queue_video, self.effect['video'], self.overlay)

        err = gst.element_link_many(
            self.overlay, self.tee, queue1, self.videorate,
            self.videoscale, self.colorspace, self.mux, self.sink
        )
        if err == False:
            print "Error conecting elements"

        gst.element_link_many(
                self.queue_audio, self.effect['audio'], self.convert, self.mux
        )

        if self.preview_enabled:
            self.player.add(queue2, self.preview_element)
            err = gst.element_link_many(self.tee, queue2, self.preview_element)
            if err == False:
                print "Error conecting preview"

        self.overlay.set_property("text", overlay_text)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.player.send_event(gst.event_new_eos())

    def set_effects(self, state):
        self.effect_enabled = state

        # If state is disabled and pipeline is playing, disable effects now

        if not self.effect_enabled:
            if self.player and self.player.get_state()[1] == gst.STATE_PLAYING:
                self.change_effect("identity", "video")
                self.change_effect("identity", "audio")

    def change_effect(self, effect_name, effect_type):
        if self.player.get_state()[1] == gst.STATE_PLAYING:
            print "PLAYING"
            Effect.change(
                    self.effect[effect_type], self.effect_name[effect_type],
                    effect_name
            )
            self.effect_name[effect_type] = effect_name

    def set_preview(self, state):
        self.preview_enabled = state

    def on_window_closed(self, event, data):
        gtk.main_quit()

    def change_overlay(self, overlay_text):
        self.overlay.set_property("text", overlay_text)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        print "sync_message received"
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            previewsink = message.src
            self.preview.set_display(previewsink)
            previewsink.set_property("sync", "false")
            previewsink.set_property("force-aspect-ratio", "true")
