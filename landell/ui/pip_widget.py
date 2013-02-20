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
import gtk
from gtk import gdk
from landell.log import Log

class PIPSelector(gtk.DrawingArea):

    __gproperties__ = {
            'selected' : (GObject.TYPE_INT,               # type
                        'selected',                       # nick name
                        'selected',                       # description
                        0,                                # minimum value
                        3,                                # maximum value
                        0,                                # default value
                        GObject.PARAM_READWRITE)          # flags
    }

    __gsignals__ = {
            'changed' : (
                GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                (GObject.TYPE_INT,)
            )
    }

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.on_expose_event)
        self.connect("realize", self.on_realize)
        self.connect("button-release-event", self.on_button_release)
        self.connect("size-request", self.on_size_request)

        self.selected = 0

    def on_expose_event(self, widget, event):
        context = self.window.cairo_create()
        context.scale(self.allocation.width, self.allocation.height)

        context.set_source_rgb(0.447, 0.623, 0.812)
        context.rectangle(0, 0, 1, 1)
        context.fill()

        context.set_source_rgb(0.204, 0.396, 0.643)
        context.set_line_width(0.015)
        context.move_to(0, 0.5)
        context.line_to(1, 0.5)
        context.move_to(0.5, 0)
        context.line_to(0.5, 1)
        context.stroke()

        x_offset = y_offset = 0
        if self.selected == 1:
            x_offset = 0.5
        elif self.selected == 2:
            y_offset = 0.5
        elif self.selected == 3:
            x_offset = 0.5
            y_offset = 0.5

        context.rectangle(x_offset, y_offset, x_offset + 0.5, y_offset + 0.5)
        context.fill()

    def on_realize(self, widget):
        self.add_events(gdk.BUTTON_PRESS_MASK|gdk.BUTTON_RELEASE_MASK);

    def on_button_release(self, widget, event):
        x, y = event.get_coords()
        width = self.allocation.width
        height = self.allocation.height
        TOP = 0
        BOTTOM = 1
        LEFT = 0
        RIGHT = 1

        horizontal = RIGHT
        if x < width/2:
            horizontal = LEFT
        vertical = BOTTOM
        if y < height/2:
            vertical = TOP

        if horizontal == LEFT and vertical == TOP:
            self.selected = 0
        elif horizontal == RIGHT and vertical == TOP:
            self.selected = 1
        elif horizontal == LEFT and vertical == BOTTOM:
            self.selected = 2
        else:
            self.selected = 3

        self.emit("changed", self.selected)
        self.queue_draw()

    def on_size_request(self, widget, requisition):
        requisition.width = 50
        requisition.height = 50

    def do_get_property(self, property):
        if property.name == "selected":
            value = self.selected
            return value
        else:
            Log.warning('PIPSelector unknown property %s' % property.name)

    def do_set_property(self, property, value):
        if property.name == "selected":
            self.selected = value
        else:
            Log.warning('PIPSelector unknown property %s' % property.name)

GObject.type_register(PIPSelector)
