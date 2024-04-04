#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# cmake.py
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

import os

class CMakeModuleGenerator:
    def __init__(self):
        pass

    def test(self):
        pass

    def generate(self, package, package_source_directory, output_directory):
        target_path = output_directory / ("Find" + package["target"] + ".cmake")
        options = package["options"]
        if not output_directory.exists():
            os.mkdir(output_directory)
        with open(target_path, "w") as module:
            module.write(
"""#####################################################
#       THIS FILE WAS AUTOMATICALLY GENERATED       #
#####################################################

set ({package_name}_SOURCE_DIR "{package_sources}")
""".format(package_name=package["target"], package_sources=package_source_directory.as_posix()))

            if "is_cmake_library" in options:
                module.write('set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "' + package_source_directory.as_posix() + '")\n')

            module.write(
"""
if (NOT TARGET {target_name})
""".format(target_name=package["target"]))

            if "create_library" in options:
                self.__append_library(package, module)
            module.write(
"""
endif ()
""")


    def __append_library(self, package, file):
        lib = package["options"]["create_library"] 
        file.write(
"""    add_library({name} {library_type})
""".format(name=package["target"], library_type=lib["type"]))
       
        files = []
        for scope in lib["sources"]:
            name = package["target"] + scopt
            files_target = {"scope": scope, "name": target} 
            file.write("   ")

            for source in lib["sources"][scope]
                file.write("    ")
        
