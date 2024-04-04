#!/bin/python3

# This file is part of YASPEM project.
# Copyright (C) 2023 Mateusz Stadnik
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import os
import sys

from pathlib import Path
from platformdirs import user_cache_dir 

import configparser

from arguments import parse_arguments
from progress import GitRemoteProgress, GitUpdateProgress
from packages_parser import PackagesParser 

from git import Repo

import colorama

from cache import LocalCache

def git_clone(repository_link, path):
    Repo.clone_from(repository_link, path, progress=GitRemoteProgress())

def is_correct_tag(repo, required_tag):
    for tag in repo.tags:
        if tag.commit == repo.head.commit:
            if str(tag) == required_tag:
                return True
        try:
            if tag == repo.active_branch.name:
                return True
        except TypeError:
            pass
    return False


def submodules_update_required(package):
    if "options" in package:
        if "update_submodules" in package["options"]:
            return package["options"]["update_submodules"]


def main():
    colorama.init()
    print(colorama.Fore.CYAN + "YASPEM - Packages manager" + colorama.Style.RESET_ALL)
    args = parse_arguments() 

    LocalCache.set_cache_output_directory(args.output)
    cache_directory = user_cache_dir("yaspem", "Mateusz Stadnik")
    print(cache_directory)
    parser = PackagesParser(cache_directory, args) 
    parser.parse_packages(args)  


#                 if args.use_cmake:
#                     print("Generate CMake target: ", package["target"])
#                     target_path = modules_directory / (
#                         "Find" + package["target"] + ".cmake"
#                     )
#                     with open(target_path, "w") as module:
#                         module.write(
#                             "\
#     ###########################################################\n\
#     #          THIS FILE WAS AUTOMATICALLY GENERATED          #\n\
#     ###########################################################\n\
# \n"
#                         )
#                         package_source_variable = package["target"] + "_SOURCE_DIR"
#                         if "is_cmake_library" in package["options"]:
#                             if package["options"]["is_cmake_library"]:
#                                 module.write(
#                                     "    set ("
#                                     + package_source_variable
#                                     + ' "'
#                                     + str(package_directory.as_posix())
#                                     + '")\n'
#                                 )
#                                 module.write(
#                                     '    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "'
#                                     + str(package_directory.as_posix())
#                                     + '")\n'
#                                 )
#                                 continue
#                         module.write("if (NOT TARGET " + package["target"] + ")\n")
#                         module.write(
#                             "    set ("
#                             + package_source_variable
#                             + ' "'
#                             + str(package_directory.as_posix())
#                             + '")\n'
#                         )
#                         if "create_library" in package["options"]:
#                             sources_search = ""
#                             library_type = package["options"]["create_library"]["type"]
#                             for keyword in package["options"]["create_library"][
#                                 "sources_filter"
#                             ]:
#                                 sources_search += (
#                                     " "
#                                     + str(package_directory.as_posix())
#                                     + "/"
#                                     + package["options"]["create_library"][
#                                         "sources_directory"
#                                     ]
#                                     + "/"
#                                     + keyword
#                                 )
#                             module.write(
#                                 "    file(GLOB_RECURSE SRCS " + sources_search + ")\n"
#                             )
#                             module.write(
#                                 '    message(STATUS "'
#                                 + package["target"]
#                                 + ' sources: ${SRCS}")\n'
#                             )
#                             module.write(
#                                 "    set (" + package["target"] + "_sources ${SRCS})\n"
#                             )
#                             module.write(
#                                 "    add_library("
#                                 + package["target"]
#                                 + " "
#                                 + library_type
#                                 + " ${SRCS})\n"
#                             )
#                             include_type = ""
#                             if library_type == "STATIC":
#                                 include_type = "PUBLIC"
#                             elif library_type == "INTERFACE":
#                                 include_type = "INTERFACE"
#                             include_paths = ""
#                             for directory in package["options"]["create_library"][
#                                 "include_directories"
#                             ]:
#                                 include_paths += (
#                                     " "
#                                     + str(package_directory.as_posix())
#                                     + "/"
#                                     + directory
#                                 )
#                             if len(include_paths):
#                                 module.write(
#                                     "    target_include_directories("
#                                     + package["target"]
#                                     + " "
#                                     + include_type
#                                     + " "
#                                     + include_paths
#                                     + ")\n"
#                                 )
#                             if (
#                                 "compile_definitions"
#                                 in package["options"]["create_library"]
#                             ):
#                                 module.write(
#                                     "    target_compile_definitions("
#                                     + package["target"]
#                                     + " "
#                                     + include_type
#                                     + " "
#                                     + package["options"]["create_library"][
#                                         "compile_definitions"
#                                     ]
#                                     + ")\n"
#                                 )

#                             if "compile_options" in package["options"]["create_library"]:
#                                 options = package["options"]["create_library"]["compile_options"] 
#                                 module.write("    target_compile_options(\n")
#                                 for key in ["PUBLIC", "PRIVATE", "INTERFACE"]:
#                                     if key in module: 
#                                         module.write("        " + key)
#                                         for option in options[key]:
#                                             module.write("            " + option)
#                                 module.write("    )")

#                             module.write("endif ()\n")
#                             continue
#                         if "cmake_variables" in package["options"]:
#                             for variable in package["options"]["cmake_variables"]:
#                                 module.write(
#                                     "    set ("
#                                     + variable
#                                     + " "
#                                     + package["options"]["cmake_variables"][variable]
#                                     + ")\n"
#                                 )
#                         if (
#                             not "include" in package["options"]
#                             or package["options"]["include"]
#                         ):
#                             module.write(
#                                 "    add_subdirectory("
#                                 + str(package_directory.as_posix())
#                                 + " "
#                                 + str(
#                                     (
#                                         output_directory
#                                         / args.binary_dir
#                                         / package["target"]
#                                     ).as_posix()
#                                 )
#                                 + " SYSTEM)\n"
#                             )

#                         module.write("    if (NOT TARGET " + package["target"] + ")\n")
#                         module.write(
#                             "        add_library(" + package["target"] + " INTERFACE)\n"
#                         )
#                         module.write("    endif()\n")
#                         module.write("endif ()\n")
#                 with open(cache_file, "w") as file:
#                     file.write(json.dumps(cache))


main()
