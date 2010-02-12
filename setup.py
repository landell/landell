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

from setuptools import setup, find_packages

setup(
    name = "sltv",
    version = "0.1",
    author = "Holoscópio Tecnologia",
    author_email = "contato@holoscopio.com",
    description = "blah",
    license = "GPL-2+",
    keywords = "python gstreamer",
    url = "https://wiki.softwarelivre.org/TV/ProjetoSLTV",
    packages = ['sltv'],
    package_data = {'sltv':['ui/*.ui']},
    entry_points = {
        'console_scripts': [
            'sltv = sltv.sltv_ui:main',
        ],
    },
)
