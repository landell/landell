# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Copyright (C) 2013 Collabora Ltda
# Author: Luciana Fujii Pontello <luciana@collabora.com>
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

def on_event(pad, info, data):
    (swap_bin, previous_element, next_element, old_element, new_element) = data

    if info.get_event().type != Gst.EventType.EOS:
        return Gst.PadProbeReturn.OK

    pad.remove_probe(info.id)

    old_element.set_state(Gst.State.NULL)

    # remove unlinks automatically
    swap_bin.remove(old_element)
    swap_bin.add(new_element)
    new_element.link(next_element)
    previous_element.link(new_element)
    new_element.set_state(Gst.State.PLAYING)
    swap_bin.set_state(Gst.State.PLAYING)

    return Gst.PadProbeReturn.DROP

def on_block(pad, info, data):

    # Pad is blocked now
    (swap_bin, previous_element, next_element, old_element, new_element) = data

    # Remove the probe
    pad.remove_probe(info.id)

    #make sure data is flushed out of element2:

    src_pad = old_element.get_static_pad("src")
    src_pad.add_probe (Gst.PadProbeType.BLOCK |
            Gst.PadProbeType.EVENT_DOWNSTREAM, on_event, data)
    old_element.send_event(Gst.Event.new_eos())
    sink_pad = old_element.get_static_pad("sink")
    sink_pad.send_event(Gst.Event.new_eos())

    return Gst.PadProbeReturn.OK




class Swap:

    @classmethod
    def swap_element(klass, swap_bin, previous_element, next_element,
        old_element, new_element):

        previous_pad = previous_element.get_static_pad("src")

        previous_pad.add_probe(Gst.PadProbeType.BLOCK_DOWNSTREAM, on_block,
                (swap_bin, previous_element, next_element, old_element, new_element))

        return
