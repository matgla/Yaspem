#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# arguments.py
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

import argparse 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Package manager for CMake projects")
    
    parser.add_argument(
        "-i", "--input", dest="input", action="store", nargs="+", default="packages.json",
        help="JSON file with dependencies (default: packages.json)",
    )
    
    parser.add_argument(
        "-o", "--output", dest="output", action="store",
        help="directory where modules will be installed", required=True,
    )

    parser.add_argument(
        "--cmake", dest="use_cmake", action="store_true",
        default="", help="prepare packages for cmake",
    )

    parser.add_argument(
        "-b", dest="binary_dir", action="store", default="", help="binary directory"
    )

    parser.add_argument(
        "-d", "--disable_cache", action="store_true", help="Disable cache usage"
    )

    args, _ = parser.parse_known_args()
    return args

