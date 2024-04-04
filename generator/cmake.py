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

from pathlib import Path

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

            if "cmake_variables" in options:
                for var, key in options["cmake_variables"].items():
                    module.write('set ({name} {value})\n'.format(name=var, value=key))

            module.write(
"""

if (NOT TARGET {target_name})
""".format(target_name=package["target"]))
 

            if "create_library" in options:
                self.__append_library(package, package_source_directory, module)
            elif not "is_cmake_library" in options:
                module.write(
"""
    add_subdirectory ({target} {binary_dir})

""".format(target=package_source_directory, binary_dir="${PROJECT_BINARY_DIR}/yaspem_packages/" + package["target"]))

           

            module.write(
"""
endif ()
""")
            

    def __append_target_property(self, data, property, file):
        file.write("    target_{property} (\n".format(property=property))
        for scope in data:
            file.write("        " + scope + "\n")
            for e in data[scope]:
                file.write("            " + e + "\n")
        file.write("    )\n\n")

    def __append_target_include_directories(self, package, package_sources, file):
        if "include_directories" in package["options"]["create_library"]:
            config = package["options"]["create_library"]["include_directories"]  
            new_include_directories = {} 
            for scope in config:
                new_include_directories[scope] = []
                for p in config[scope]:
                    p = Path(p)
                    if not p.is_absolute():
                        p = package_sources / p 
                    new_include_directories[scope].append('"' + str(p) + '"')

            self.__append_target_property(new_include_directories, "include_directories", file)

    def __append_target_sources(self, package, package_sources, file):
        files = []
        lib = package["options"]["create_library"]
        for scope in lib["sources"]:
            name = package["target"] + "_" + scope.lower() + "_sources"
            files.append({"scope": scope, "name": name})
            file.write("    file (GLOB_RECURSE " + name + "\n")
            for source in lib["sources"][scope]:
                p = Path(source) 
                if not p.is_absolute():
                    p = package_sources / p 
                file.write('        "' + str(p) + '"\n')
            file.write("    )\n\n")

        file.write("    target_sources (" + package["target"] + "\n")
        for f in files:
            file.write("        " + f["scope"] + " ${" + f["name"] + "}\n")
        file.write("    )\n\n") 

    def __append_library(self, package, package_sources, file):
        lib = package["options"]["create_library"] 
        file.write(
"""    add_library ({name} {library_type})
""".format(name=package["target"], library_type=lib["type"]))
        self.__append_target_sources(package, package_sources, file)
        self.__append_target_include_directories(package, package_sources, file)

        supported_props = ["compile_definitions", "link_libraries", "link_directories"]
        for prop in supported_props: 
            if prop in lib:
                self.__append_target_property(lib[prop], prop, file)
        
        
