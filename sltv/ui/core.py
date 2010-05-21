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


import gobject
import gtk
from sltv.output import *
from sltv.audio import *
from sltv.sltv import *
from sltv.settings import UI_DIR

import about
import sources
import message
import outputs
import encoders
import sources_view
import outputs_view

from previewarea import PreviewArea
import preview
import effects
import overlay
import volume
import settings as settings
import pip_widget

class SltvUI:

    def __init__(self):
        self.interface = gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/sltv.ui")
        self.main_window = self.interface.get_object("window1")
        self.main_window.show_all()
        self.about = about.About(self)

        self.sltv = Sltv()
        self.sltv.connect("stopped", self.stopped)
        self.sltv.connect("playing", self.playing)
        self.sltv.connect("preplay", self.preplay)
        self.sltv.connect("error", self.error)
        self.sltv.connect("pipeline-ready", self.on_pipeline_ready)

        self.preview_frame = self.interface.get_object("preview_frame")
        self.preview_box = self.interface.get_object("preview_vbox")
        self.preview = preview.PreviewUI(self, self.sltv)
        self.preview_box.pack_start(self.preview.get_widget(), False, False)
        self.preview_area = PreviewArea()
        self.preview_frame.add(self.preview_area)
        self.preview_area.show()

        self.box = self.interface.get_object("paned")
        self.settings = settings.SettingsUI(self, self.sltv)
        self.box.add(self.settings.get_widget())

        self.play_button = self.interface.get_object("play_button")
        self.stop_button = self.interface.get_object("stop_button")

        self.settings_dialog = gtk.Dialog('Settings', self.main_window)
        self.settings_dialog.set_default_size(400, 400)

        self.encoders = self.sltv.encoders
        self.videoconverters = self.sltv.videoconverters
        self.encoders_ui = encoders.Encoders(
                self, self.encoders, self.videoconverters
        )

        # pip

        pip_box = self.interface.get_object("pip_box")
        self.pip_selector = pip_widget.PIPSelector()
        self.pip_selector.connect("changed", self.on_pip_changed)
        pip_box.add(self.pip_selector)
        pip_box.show_all()

        # sources

        self.sources = self.sltv.sources
        self.audioconvs = self.sltv.audioconvs
        self.sources_ui = sources.Sources(self, self.sources, self.audioconvs)
        self.video_source_box = self.interface.get_object("video_source_box")
        self.sources_view = sources_view.SourcesView(self.sltv, self.sources)
        self.sources_view.show_all()
        self.video_source_box.pack_start(self.sources_view, False, False)

        # audio combobox

        self.audio_sources_combobox = self.interface.get_object(
                "audio_sources_combobox"
        )
        self.audio_sources_combobox.set_model(
                sources.AudioModel(self.sources).model
        )
        cell = gtk.CellRendererText()
        self.audio_sources_combobox.pack_start(cell, True)
        self.audio_sources_combobox.add_attribute(cell, "text", 0)
        self.audio_sources_combobox.connect(
                "changed", self.on_select_audio_source
        )
        self.audio_sources_combobox.set_active(0)

        # outputs

        self.outputs = self.sltv.outputs
        self.outputs_ui = outputs.Outputs(self, self.outputs, self.encoders)
        self.outputs_box = self.interface.get_object("outputs_box")
        self.outputs_view = outputs_view.OutputsView( self.sltv, self.outputs)
        self.outputs_view.show_all()
        self.outputs_box.pack_start(self.outputs_view, False, False)

        # settings dialog

        self.settings_dialog.set_has_separator(False)
        self.settings_dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        self.settings_dialog.connect('delete-event', self.hide_settings)
        self.settings_dialog.connect('response', self.hide_settings)

        vbox = self.settings_dialog.get_content_area()
        vbox.set_border_width(12)

        notebook = gtk.Notebook()
        self.settings_notebook = notebook
        vbox.add(notebook)

        vbox = gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.sources_ui.get_widget())
        notebook.append_page(vbox, gtk.Label('Sources'))

        vbox = gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.encoders_ui.get_widget())
        notebook.append_page(vbox, gtk.Label('Encoders'))

        vbox = gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.outputs_ui.get_widget())
        notebook.append_page(vbox, gtk.Label('Outputs'))

        #menu

        self.settings_menuitem = self.interface.get_object("settings_menuitem")
        self.quit_menuitem = self.interface.get_object("quit_menuitem")
        self.about_menu = self.interface.get_object("about_menu")

        self.play_button.connect("clicked", self.on_play_press)
        self.stop_button.connect("clicked", self.on_stop_press)
        self.main_window.connect("delete_event", self.on_window_closed)

        self.settings_menuitem.connect("activate", self.show_settings)
        self.quit_menuitem.connect("activate", gtk.main_quit)
        self.about_menu.connect("activate", self.show_about)

    def on_pipeline_ready(self, sltv):
        sltv_preview = self.sltv.get_preview()
        self.preview_area.connect(sltv_preview)

    def stopped(self, sltv):
        self.stop_button.set_sensitive(False)
        self.play_button.set_sensitive(True)
        self.audio_sources_combobox.set_sensitive(True)
        self.settings_menuitem.set_sensitive(True)

    def playing(self, sltv):
        self.play_button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        self.settings_menuitem.set_sensitive(False)

    def preplay(self, sltv):
        self.audio_sources_combobox.set_sensitive(False)

    def error(self, sltv, msg):
        message.MessageError(msg, self)

    def selected_audio_source(self):
        model = self.audio_sources_combobox.get_model()
        iter = self.audio_sources_combobox.get_active_iter()
        if iter == None:
            return None
        return model.get_value(iter, 0)

    def on_select_audio_source(self, combobox):
        source_name = self.selected_audio_source()
        self.sltv.set_audio_source(source_name)

    def on_pip_changed(self, widget, selected):
        self.sltv.set_pip_position(selected)

    def on_play_press(self, event):
        if not self.sources_view.has_item_a_selected():
            message.MessageInfo(
                "Please, choose or add a video source.", self
            )
            return False

        self.play_button.set_sensitive(False)
        self.play()

    def play(self):
        if not self.sltv.playing():
            self.sltv.play()

    def show_settings(self, menuitem = None):
        self.settings_dialog.show_all()

    def hide_settings(self, *args):
        self.settings_dialog.hide()
        self.settings_notebook.set_current_page(0)
        return True

    def show_about(self, menuitem):
        self.about.show_window()

    def on_stop_press(self, event):
        self.stop_button.set_sensitive(False)
        self.stop()

    def stop(self):
        if self.sltv.playing():
            self.sltv.stop()

    def on_window_closed(self, event, data):
        gtk.main_quit()
