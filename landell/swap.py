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
gi.require_version("Gst", "1.0")
from gi.repository import Gst

def event_received(pad, event):
    print "event_received"
    return

class Swap:

    @classmethod
    def swap_element(klass, swap_bin, previous_element, next_element,
        old_element, new_element):

        previous_pad = previous_element.get_static_pad("src")

        #FIXME: Use the async method to work for paused state

        previous_pad.set_blocked(True)
        previous_element.unlink(old_element)

        #make sure data is flushed out of element2:

        old_pad = old_element.get_static_pad("src")
        handler_id = old_pad.add_event_probe(event_received)
        old_element.send_event(Gst.event_new_eos())
        old_pad.remove_event_probe(handler_id)

        previous_element.unlink(old_element)
        old_element.unlink(next_element)
        old_element.set_state(Gst.STATE_NULL)
        swap_bin.remove(old_element)
        swap_bin.add(new_element)
        new_element.link(next_element)
        previous_element.link(new_element)
        new_element.set_state(Gst.STATE_PLAYING)
        previous_pad.set_blocked(False)
        swap_bin.set_state(Gst.STATE_PLAYING)
        return
