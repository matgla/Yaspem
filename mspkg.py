#!/bin/python3

# This file is part of MSModuleManager project.
# Copyright (C) 2020 Mateusz Stadnik
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
import subprocess
import os

from git import Repo
import configparser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def git_clone(repository_link, path):
    Repo.clone_from(repository_link, path)

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

def update_submodules_iter(gen):
    while True:
        try:
            yield next(gen)
        except StopIteration:
            break
        except configparser.NoOptionError:
            continue

def main():
    print(bcolors.HEADER + "Package manager" + bcolors.ENDC)

    parser = argparse.ArgumentParser(description = "Package manager for CMake projects")
    parser.add_argument("-i", "--input", dest="input", action="store", help="JSON file with dependencies (default: packages.json)")
    parser.add_argument("-o", "--output", dest="output", action="store", help="directory where modules will be installed (default: packages)")
    parser.add_argument("setup", action="store_true", help="configure project")
    parser.add_argument("install", action="store_true", help="install dependencies")
    parser.add_argument("update", action="store_true", help="update dependencies")
    parser.add_argument("clean", action="store_true", help="remove build and cache files")
    parser.add_argument("--prune", dest="prune", action="store_true", help="flag to clean command which also removes sources")
    parser.add_argument("add", action="store_true", help="interactive menu to add package")
    parser.add_argument("remove", nargs="?", action="store", default="", help="remove package with name")
    parser.add_argument("--cmake", dest="use_cmake", action="store_true", default="", help="prepare packages for cmake")
    parser.add_argument("-b", dest="binary_dir", action="store", default="", help="binary directory")
    args, rest = parser.parse_known_args()

    input_file = "packages.json"
    output_directory = "packages"
    print("Dependencies list: ")

    if args.input:
        input_file = args.input

    if args.output:
        output_directory = args.output + "/packages"

    cache_file = args.output + "/cache.json"
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            cache = json.loads(file.read())

    if not "timestamps" in cache:
        cache["timestamps"] = {}
    if not "package_file" in cache["timestamps"]:
        cache["timestamps"]["package_file"] = os.path.getmtime(input_file)

    with open(input_file, "r") as input_data:
        input_json = json.loads(input_data.read())
        current_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(output_directory):
            output_directory = current_path + "/" + output_directory
        sources_directory = output_directory + "/" + "sources"
        modules_directory = output_directory + "/" + "modules"
        if not os.path.exists(output_directory):
            print ("Creating output directory: ", output_directory)
            os.makedirs(output_directory)

        if not os.path.exists(sources_directory):
            print ("Creating sources directory: ", sources_directory)
            os.makedirs(sources_directory)

        if not os.path.exists(modules_directory):
            print ("Creating modules directory: ", modules_directory)
            os.makedirs(modules_directory)

        for package in input_json["dependencies"]:
            print (" > " + package["target"])

            package_directory = sources_directory + "/" + package["directory"]
            print ("directory: ", package_directory)
            if package["type"] == "git":

                if os.path.exists(package_directory):
                    repo = Repo(package_directory)
                else:
                    git_clone(package["link"], package_directory)

                repo = Repo(package_directory)

                if submodules_update_required(package):
                    print ("Submodules update")
                    for submodule in update_submodules_iter(repo.submodules.iter()):
                        print (" > " + str(submodule))
                        submodule.update(init=True)

                if not is_correct_tag(repo, package["version"]):
                    repo.git.checkout(package["version"])

            else:
                raise "Only git links are supported currently"

            if args.use_cmake:
                print ("Generate CMake target: ", package["target"])
                target_path = modules_directory + "/Find" + package["target"] + ".cmake"
                with open(target_path, "w") as module:
                    module.write("\
###########################################################\n\
#          THIS FILE WAS AUTOMATICALLY GENERATED          #\n\
###########################################################\n\
# This file is part of MSModuleManager project.\n\
# Copyright (C) 2021 Mateusz Stadnik\n\
#\n\
# This program is free software: you can redistribute it and/or modify\n\
# it under the terms of the GNU General Public License as published by\n\
# the Free Software Foundation, either version 3 of the License, or\n\
# (at your option) any later version.\n\
#\n\
# This program is distributed in the hope that it will be useful,\n\
# but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
# GNU General Public License for more details.\n\
#\n\
# You should have received a copy of the GNU General Public License\n\
# along with this program.  If not, see <https://www.gnu.org/licenses/>.\n\
")
                    if "is_cmake_library" in package["options"]:
                        if package["options"]["is_cmake_library"]:
                            module.write("set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} " + package_directory + ")")
                            continue
                    module.write("if (NOT TARGET " + package["target"] + ")\n")
                    if "create_library" in package["options"]:
                        sources_search = ""
                        library_type = package["options"]["create_library"]["type"]
                        for keyword in package["options"]["create_library"]["sources_filter"]:
                            sources_search += " " + package_directory + "/" + package["options"]["create_library"]["sources_directory"] + "/" + keyword
                        module.write("    file(GLOB_RECURSE SRCS " + sources_search + ")\n")
                        module.write("    message(STATUS \"" + package["target"] + " sources: ${SRCS}\")\n")
                        module.write("    set (" + package["target"] + "_sources ${SRCS})\n")
                        module.write("    add_library(" + package["target"] + " " + library_type + " ${SRCS})\n")
                        include_type = ""
                        if library_type == "STATIC":
                            include_type = "PUBLIC"
                        include_paths = ""
                        for directory in package["options"]["create_library"]["include_directories"]:
                            include_paths += " " + package_directory + "/" + directory
                        if len(include_paths):
                            module.write("    target_include_directories(" + package["target"] + " " + include_type + " " + include_paths + ")\n")
                        if "compile_definitions" in package["options"]["create_library"]:
                            module.write("    target_compile_definitions(" + package["target"] + " " + include_type + " " + package["options"]["create_library"]["compile_definitions"] + ")\n")
                        module.write("endif ()\n");
                        continue
                    if "cmake_variables" in package["options"]:
                        for variable in package["options"]["cmake_variables"]:
                            module.write("    set (" + variable + " " + package["options"]["cmake_variables"][variable] + ")\n")
                    if not "include" in package["options"] or package["options"]["include"]:
                        module.write("    add_subdirectory(" + package_directory + " " + args.binary_dir + "/" + package["target"] + ")\n")

                    module.write("endif ()\n")



    # if (args)
            with open(cache_file, "w") as file:
                file.write(json.dumps(cache))

main()
