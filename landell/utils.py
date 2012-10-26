# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscópio Tecnologia
# Author: Samuel Ribeiro da Costa Vale <srcvale@holoscopio.com>
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


class Fract:

    @classmethod
    def fromdecimal(cls, f):
        den = 30
        num = int(round(float(f) * den))

        if (num % 30) == 0:
            comm = 30
        elif (num % 15) == 0:
            comm = 15
        elif (num % 10) == 0:
            comm = 10
        elif (num % 5) == 0:
            comm = 5
        elif (num % 3) == 0:
            comm = 3
        elif (num % 2) == 0:
            comm = 2
        else:
            comm = 1

        den /= comm
        num /= comm
        return num, den

