#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# packages_parser.py
#
# Copyright (C) 2024 Mateusz Stadnik <matgla@live.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General
# Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
#

import colorama

import json

def __process_file(input, output_directory):
    print(colorama.Fore.YELLOW + "  -> " + colorama.Style.RESET_ALL + str(input))
    
    
def parse_packages(args):
    print("Processing package file:")
    for input in args.input:
        __process_file(input, args.output)
