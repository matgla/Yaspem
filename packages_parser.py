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

from cache import LocalCache

from git_fetch import GitFetch

class PackagesParser:
    def __init__(self, cache_directory):
        self.max_name = 0 
        self.line_chars = 0
        self.cache_directory = cache_directory

    def __print_progress(self, package, color, status, end = False):
        end_char = "\r" 
        if end:
            end_char = "\n"
        name_format = "{name:<" + str(self.max_name + 1) + "}"
        text = "" + colorama.Style.BRIGHT + color + "    -> " + colorama.Style.RESET_ALL \
            + " " + name_format + " | " + status
        text = text.format(name=package["target"])
        print(" " * self.line_chars, end="\r") 
        self.line_chars = len(text)
        print(text, end=end_char)

    def __process_dependency(self, package, output_directory):
        self.__print_progress(package, colorama.Fore.BLUE, "")
        if LocalCache.contains(package):
            self.__print_progress(package, colorama.Fore.BLUE, "already fetched")
        else:
            self.__print_progress(package, colorama.Fore.BLUE, "fetching - [  0%]")
            self.__fetch_package(package, output_directory) 
        self.__print_progress(package, colorama.Fore.GREEN, "", True)
        

    def __progress_callback(self, package, status):
        self.__print_progress(package, colorama.Fore.BLUE, status)   

    def __fetch_package(self, package, output_directory):
        if package["type"] == "git":
            fetch = GitFetch(self.cache_directory, self.__progress_callback)
            fetch.fetch(package)


    def __process_file(self, input, output_directory):
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + "  -> " + colorama.Style.RESET_ALL + str(input))
        with open(input, "r") as file:
            data = json.loads(file.read())
            
            self.max_name = 0 
            self.line_chars = 0
            for dep in data["dependencies"]:
                if len(dep["target"]) > self.max_name:
                    self.max_name = len(dep["target"])
    
            for dep in data["dependencies"]:
                self.__process_dependency(dep, output_directory)

    def parse_packages(self, args):
        print("Processing package file:")
        for input in args.input:
            self.__process_file(input, args.output)
