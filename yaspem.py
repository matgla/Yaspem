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
import subprocess
import os
import sys

from pathlib import Path

from git import Repo,RemoteProgress,UpdateProgress
import configparser

from tqdm import tqdm
# from https://stackoverflow.com/a/65576165

class GitRemoteProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


class GitUpdateProgress(UpdateProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


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
    print(bcolors.HEADER + "Package manager" + bcolors.ENDC)

    parser = argparse.ArgumentParser(description = "Package manager for CMake projects")
    parser.add_argument("-i", "--input", dest="input", action="store", help="JSON file with dependencies (default: packages.json)")
    parser.add_argument("-o", "--output", dest="output", action="store", help="directory where modules will be installed", required=True)
    parser.add_argument("--cmake", dest="use_cmake", action="store_true", default="", help="prepare packages for cmake")
    parser.add_argument("-b", dest="binary_dir", action="store", default="", help="binary directory")
    args, rest = parser.parse_known_args()

    output_directory = "" if args.output else "packages"
    print("Dependencies list: ")
    print(args.input)
    if args.input:
        input_files = [s.strip() for s in args.input.split(",")]
    else:
        input_files = ["packages.json"]

    for i, n in enumerate(input_files):
        input_files[i] = Path(n) 

    for input_file in input_files:
        if not os.path.exists(input_file):
            print("error: input file '" + str(input_file) + "' not found", file=sys.stderr)
            sys.exit(1)

    if args.output:
        args.output = args.output.strip()
        output_directory = Path(args.output)

    cache_file = output_directory / "cache.json"
    print ("Output directory: ", output_directory)
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            cache = json.loads(file.read())

    if not "timestamps" in cache:
        cache["timestamps"] = {}
    if not "package_file" in cache["timestamps"]:
        cache["timestamps"]["package_file"] = {}
    for input_file in input_files:
        if not input_file in cache["timestamps"]["package_file"]:
            cache["timestamps"]["package_file"][str(input_file)] = os.path.getmtime(input_file)

    priority = len(Path(os.getcwd()).parts)
    print("Priority: ", priority)
    if not "priorities" in cache:
        cache["priorities"] = {}

    for input_file in input_files:
        with open(input_file, "r") as input_data:
            input_json = json.loads(input_data.read())
            current_path = os.path.dirname(os.path.abspath(__file__))
            if not os.path.isabs(output_directory):
                output_directory = current_path / output_directory
            sources_directory = output_directory / "sources"
            modules_directory = output_directory / "modules"

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
                if not package["target"] in cache["priorities"]:
                    cache["priorities"][package["target"]] = priority

                elif priority > cache["priorities"][package["target"]]:
                    print (" > " + package["target"] + " was fetched by parent packages.json")
                    continue

                print (" > " + package["target"])

                if not "directory" in package:
                    directory_suffix = package["target"]
                else:
                    directory_suffix = package["directory"]
                package_directory = (Path(sources_directory) / directory_suffix).resolve()
                print ("directory: ", package_directory, file=sys.stderr)
                if package["type"] == "git":

                    if os.path.exists(package_directory):
                        repo = Repo(package_directory)
                    else:
                        git_clone(package["link"], package_directory)


                    repo = Repo(package_directory)

                    if submodules_update_required(package):
                        print ("Submodules update")
                        try:
                            for submodule in repo.submodules:
                                print (" > " + str(submodule))
                                submodule.update(init=True, progress=GitUpdateProgress())
                        except configparser.NoOptionError:
                            print ("Can't update submodules, invalid entry")
                    if not is_correct_tag(repo, package["version"]):
                        print("Checkout version: ", package["version"])
                        repo.git.checkout(package["version"])

                    update_request = os.environ.get("UPDATE_PACKAGES")
                    if update_request != None and update_request == "1":
                        print ("Update package: ", package["target"])
                        repo.git.fetch()
                        all_branches = repo.git.branch("--all").split()
                        if package["version"] in all_branches:
                            repo.git.rebase()


                else:
                    raise "Only git links are supported currently"

                if args.use_cmake:
                    print ("Generate CMake target: ", package["target"])
                    target_path = modules_directory / ("Find" + package["target"] + ".cmake")
                    with open(target_path, "w") as module:
                        module.write("\
    ###########################################################\n\
    #          THIS FILE WAS AUTOMATICALLY GENERATED          #\n\
    ###########################################################\n\
    ")
                        package_source_variable = package["target"] + "_SOURCE_DIR"
                        if "is_cmake_library" in package["options"]:
                            if package["options"]["is_cmake_library"]:
                                module.write("set (" + package_source_variable + " \"" + str(package_directory)  + "\")\n")
                                module.write("set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} \"" + str(package_directory) + "\")")
                                continue
                        module.write("if (NOT TARGET " + package["target"] + ")\n")
                        module.write("    set (" + package_source_variable + " \"" + str(package_directory)  + "\")\n")
                        if "create_library" in package["options"]:
                            sources_search = ""
                            library_type = package["options"]["create_library"]["type"]
                            for keyword in package["options"]["create_library"]["sources_filter"]:
                                sources_search += " " + str(package_directory) + "/" + package["options"]["create_library"]["sources_directory"] + "/" + keyword
                            module.write("    file(GLOB_RECURSE SRCS " + sources_search + ")\n")
                            module.write("    message(STATUS \"" + package["target"] + " sources: ${SRCS}\")\n")
                            module.write("    set (" + package["target"] + "_sources ${SRCS})\n")
                            module.write("    add_library(" + package["target"] + " " + library_type + " ${SRCS})\n")
                            include_type = ""
                            if library_type == "STATIC":
                                include_type = "PUBLIC"
                            elif library_type == "INTERFACE":
                                include_type = "INTERFACE"
                            include_paths = ""
                            for directory in package["options"]["create_library"]["include_directories"]:
                                include_paths += " " + str(package_directory) + "/" + directory
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
                            module.write("    add_subdirectory(" + str(package_directory) + " " + str((output_directory / args.binary_dir / package["target"])) + ")\n")

                        module.write("    if (NOT TARGET " + package["target"] + ")\n")
                        module.write("        add_library(" + package["target"] + " INTERFACE)\n")
                        module.write("    endif()\n")
                        module.write("endif ()\n")
                with open(cache_file, "w") as file:
                    file.write(json.dumps(cache))

main()
