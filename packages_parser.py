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
import sys
import shutil

from pathlib import Path

from cache import LocalCache

from fetcher.git import GitFetch
from generator.cmake import CMakeModuleGenerator
from distutils.dir_util import copy_tree

class PackagesParser:
    fetched = {}
    def __init__(self, cache_directory, args):
        self.max_name = 0 
        self.line_chars = 0
        self.cache_directory = cache_directory
        self.force = args.force 
        self.nosync = args.no_network
        self.nocompatibility_check = args.no_compatibility_check
        self.generator = None 
        self.no_cache = args.no_cache

        if args.use_cmake:
            self.generator = CMakeModuleGenerator()

    def __print_progress(self, package, color, status, end = False, success = True):
        end_char = "\r" 
        if end:
            end_char = "\n"
        name_format = "{name:<" + str(self.max_name + 1) + "}"
        delimiter = " | "
        if end:
            if success:
                delimiter = color + " ✔  " + colorama.Style.RESET_ALL
            else:
                delimiter = colorama.Fore.RED + " ✘  " + colorama.Style.RESET_ALL
        warning = " "
        if self.warning:
            warning = "!"
        text = "" + colorama.Style.BRIGHT + color + warning + "   -> " + colorama.Style.RESET_ALL \
            + " " + name_format + delimiter + status
        text = text.format(name=package["target_name"])
        print(" " * self.line_chars, end="\r") 
        self.line_chars = len(text)
        print(text, end=end_char)

    def __copy_package(self, package, output_directory):
        target_path = output_directory / package["target_name"]
        if target_path.exists():
            shutil.rmtree(target_path, ignore_errors=False)
        copy_tree(Path(self.cache_directory) / package["target_name"], str(output_directory / package["target_name"]))

    def __process_dependency(self, file, package, output_directory):
        self.final_msg = "" 
        self.warning = False
        self.__print_progress(package, colorama.Fore.BLUE, "")
        if LocalCache.contains(package) and not (self.force or self.no_cache):
            self.final_msg = "Already fetched: {}".format(LocalCache.get(package))
            PackagesParser.fetched[package["target_name"]] = {"version": package["version"]}

        else:
            self.__print_progress(package, colorama.Fore.BLUE, "fetching - [  0%]")
            
            if package["target_name"] in PackagesParser.fetched:
                cache = PackagesParser.fetched[package["target_name"]]
                color = colorama.Fore.GREEN
                
                if cache["version"] == package["version"]:
                    self.__print_progress(package, color, "Fetched {}".format(package["version"]), True)
                    return
                elif self.nocompatibility_check:
                    self.warning = True 
                    color = colorama.Fore.YELLOW
                    self.__print_progress(package, color, "Fetched by parent: {}, requested: {}".format(cache["version"], package["version"]), True, True)
                    return  
                else:
                    color = colorama.Fore.RED
                    self.__print_progress(package, color, "Incompatible versions requested: {} != {}".format(package["version"], cache["version"]), True)
                    return 

            self.__fetch_package(package, output_directory) 
            PackagesParser.fetched[package["target_name"]] = {"version": package["version"]}

            self.__copy_package(package, output_directory / "sources")
            if self.generator:
                self.generator.generate(package, output_directory / "sources" / package["target_name"], output_directory / "modules")
            
            LocalCache.update_cache_entry(package)
        color = colorama.Fore.GREEN
        if self.warning:
            color = colorama.Fore.YELLOW
        
        self.__print_progress(package, color, self.final_msg, True)
       
    def __progress_callback(self, package, status):
        if status != "":
            status = " - " + status
        self.__print_progress(package, colorama.Fore.BLUE, status)   

    def __submodule_update_callback(self, package, submodule):
        self.__print_progress(package, colorama.Fore.BLUE, " submodule: " + submodule)

    def __fetch_package(self, package, output_directory):
        if package["type"] == "git":
            fetch = GitFetch(self.cache_directory, self.__progress_callback, self.__submodule_update_callback, self.force, self.nosync, self.nocompatibility_check)
            result = fetch.fetch(package)
            if not result.success:
                self.__print_progress(package, colorama.Fore.RED, result.message, True, False)
                sys.exit(-1)
            
            self.warning = result.warning
            self.final_msg = result.message

    def __process_file(self, input, output_directory):
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + "  -> " + colorama.Style.RESET_ALL + str(input))
        with open(input, "r") as file:
            data = json.loads(file.read())
            
            self.max_name = 0 
            self.line_chars = 0
            for dep in data["dependencies"]:
                if not "target_name" in dep:
                    target_name = dep["link"].split("/")[-1]
                    target_name = target_name.removesuffix(".git")
                    dep["target_name"] = target_name
                if not "target" in dep:
                    dep["target"] = dep["target_name"]
                if len(dep["target"]) > self.max_name:
                    self.max_name = len(dep["target"])
    
            for dep in data["dependencies"]:
                self.__process_dependency(str(input), dep, output_directory)

    def parse_packages(self, args):
        for input in args.input:
            self.__process_file(input, args.output)
        LocalCache.store()
