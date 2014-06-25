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


import gi
from gi.repository import Gtk
from landell.output import *
from landell.audio import *
from landell.landell import *
from landell.settings import UI_DIR

import about
import sources
import message
import outputs
import encoders
import sources_view
import outputs_view

from previewarea import PreviewArea
import effects
import overlay
import volume
import settings as settings
import pip_widget
import metadata
import general

class SltvUI:

    def __init__(self):
        self.interface = Gtk.Builder()
        self.interface.add_from_file(UI_DIR + "/landell.ui")
        self.main_window = self.interface.get_object("window1")
        self.main_window.show_all()
        self.about = about.About(self)

        self.landell = Sltv()
        self.landell.connect("stopped", self.stopped)
        self.landell.connect("playing", self.playing)
        self.landell.connect("error", self.error)
        self.landell.connect("pipeline-ready", self.on_pipeline_ready)

        self.preview_frame = self.interface.get_object("preview_frame")
        self.preview_area = PreviewArea()
        self.preview_frame.add(self.preview_area)
        self.preview_area.show()

        self.box = self.interface.get_object("paned")
        self.settings = settings.SettingsUI(self, self.landell)
        self.box.add(self.settings.get_widget())

        self.play_button = self.interface.get_object("play_button")
        self.stop_button = self.interface.get_object("stop_button")

        self.settings_dialog = Gtk.Dialog('Settings', self.main_window)
        self.settings_dialog.set_default_size(400, 400)

        self.encoders = self.landell.encoders
        self.videoconverters = self.landell.videoconverters
        self.encoders_ui = encoders.Encoders(
                self, self.encoders, self.videoconverters
        )
        self.metadata_ui = metadata.MetadataUI(self.landell, self.settings_dialog)
        self.general_ui = general.GeneralUI(self.landell, self.settings_dialog)

        self.hbuttonbox = self.interface.get_object("hbuttonbox1")
        self.volume = volume.VolumeUI(self, self.landell)
        self.volume_button = self.volume.get_widget()
        self.volume_button.show()
        self.hbuttonbox.pack_start(self.volume_button, False, False, 0)

        # pip

        pip_box = self.interface.get_object("pip_box")
        self.pip_selector = pip_widget.PIPSelector()
        self.pip_selector.connect("changed", self.on_pip_changed)
        pip_box.add(self.pip_selector)
        pip_box.show_all()

        # sources

        self.sources = self.landell.sources
        self.audioconvs = self.landell.audioconvs
        self.sources_ui = sources.Sources(self, self.sources, self.audioconvs)
        self.video_source_box = self.interface.get_object("video_source_box")
        self.sources_view = sources_view.SourcesView(self.landell, self.sources)
        self.sources_view.show_all()
        self.video_source_box.pack_start(self.sources_view, False, False, 0)

        # audio combobox

        self.audio_sources_combobox = self.interface.get_object(
                "audio_sources_combobox"
        )
        self.audio_sources_combobox.set_model(
                sources.AudioModel(self.sources).model
        )
        cell = Gtk.CellRendererText()
        self.audio_sources_combobox.pack_start(cell, True)
        self.audio_sources_combobox.add_attribute(cell, "text", 0)
        self.audio_sources_combobox.connect(
                "changed", self.on_select_audio_source
        )
        self.audio_sources_combobox.set_active(0)

        # outputs

        self.outputs = self.landell.outputs
        self.outputs_ui = outputs.Outputs(self, self.outputs, self.encoders)
        self.outputs_box = self.interface.get_object("outputs_box")
        self.outputs_view = outputs_view.OutputsView( self.landell, self.outputs)
        self.outputs_view.show_all()
        self.outputs_box.pack_start(self.outputs_view, False, False, 0)

        # settings dialog

        self.settings_dialog.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        self.settings_dialog.connect('delete-event', self.hide_settings)
        self.settings_dialog.connect('response', self.hide_settings)

        vbox = self.settings_dialog.get_content_area()
        vbox.set_border_width(12)

        notebook = Gtk.Notebook()
        self.settings_notebook = notebook
        vbox.add(notebook)

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.sources_ui.get_widget(), True, False, 0)
        notebook.append_page(vbox, Gtk.Label('Sources'))

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.encoders_ui.get_widget(), True, False, 0)
        notebook.append_page(vbox, Gtk.Label('Encoders'))

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.outputs_ui.get_widget(), True, False, 0)
        notebook.append_page(vbox, Gtk.Label('Outputs'))

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.metadata_ui.get_widget(), True, False, 0)
        notebook.append_page(vbox, Gtk.Label('Metadata'))

        vbox = Gtk.VBox()
        vbox.set_border_width(12)
        vbox.pack_start(self.general_ui.get_widget(), True, False, 0)
        notebook.append_page(vbox, Gtk.Label('General'))

        #menu

        self.settings_menuitem = self.interface.get_object("settings_menuitem")
        self.quit_menuitem = self.interface.get_object("quit_menuitem")
        self.about_menu = self.interface.get_object("about_menu")

        self.play_button.connect("clicked", self.on_play_press)
        self.stop_button.connect("clicked", self.on_stop_press)
        self.main_window.connect("delete_event", self.on_window_closed)

        self.settings_menuitem.connect("activate", self.show_settings)
        self.quit_menuitem.connect("activate", Gtk.main_quit)
        self.about_menu.connect("activate", self.show_about)

    def on_pipeline_ready(self, landell):
        landell_preview = self.landell.get_preview()
        self.preview_area.connect(landell_preview)

    def stopped(self, landell):
        self.stop_button.set_sensitive(False)
        self.play_button.set_sensitive(True)
        self.settings_menuitem.set_sensitive(True)

    def playing(self, landell):
        self.play_button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        self.settings_menuitem.set_sensitive(False)

    def error(self, landell, msg):
        message.MessageError(msg, self)

    def selected_audio_source(self):
        model = self.audio_sources_combobox.get_model()
        iter = self.audio_sources_combobox.get_active_iter()
        if iter is None:
            return None
        return model.get_value(iter, 0)

    def on_select_audio_source(self, combobox):
        source_name = self.selected_audio_source()
        self.landell.set_audio_source(source_name)

    def on_pip_changed(self, widget, selected):
        self.landell.set_pip_position(selected)

    def on_play_press(self, event):
        if not self.sources_view.has_item_a_selected():
            message.MessageInfo(
                "Please, choose or add a video source.", self
            )
            return False

        self.play_button.set_sensitive(False)
        self.play()

    def play(self):
        if not self.landell.playing():
            self.landell.play()

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
        if self.landell.playing():
            self.landell.stop()

    def on_window_closed(self, event, data):
        Gtk.main_quit()
