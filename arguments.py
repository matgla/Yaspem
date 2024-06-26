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

from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Package manager for CMake projects")
    
    parser.add_argument(
        "-i", "--input", dest="input", action="store", nargs="+", default=["packages.json"],
        help="JSON file with dependencies (default: packages.json)",
    )
    
    parser.add_argument(
        "-o", "--output", dest="output", action="store", default="packages",
        help="directory where modules will be installed",
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

    parser.add_argument(
        "-n", "--no_network", action="store_true", help="Disable network operations, using only local cache"
    )

    parser.add_argument(
        "-f", "--force", action="store_true", help="Force fetch packages"
    )

    parser.add_argument(
        "-c", "--no_compatibility_check", action="store_true", help="Skips compatibility check, first requested version is used"
    )

    parser.add_argument(
        "-nc", "--no_cache", action="store_true", help="Ignores cache")
    
    args, _ = parser.parse_known_args()

    args.output = Path(args.output.strip()).absolute()
    inputs = [] 
    for input in args.input: 
        path = Path(input.strip()).absolute()
        if not path.exists():
            raise RuntimeError("Packages path not exists: " + str(path))
        inputs.append(path)
    args.input = inputs

    return args

