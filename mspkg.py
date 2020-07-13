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
    return False

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

    args, rest = parser.parse_known_args()
    
    input_file = "packages.json"
    output_directory = "packages"
    print("Dependencies list: ")

    if args.input: 
        input_file = args.input 
    
    if args.output:
        output_directory = args.output

    with open(input_file, "r") as input_data:
        input_json = json.loads(input_data.read())
        current_path = os.path.dirname(os.path.abspath(__file__))
        output_directory = current_path + "/" + output_directory
        generate_directory = output_directory + "/" + "cmake_modules"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for package in input_json["dependencies"]:
            print (" > " + package["name"]) 

            package_directory = output_directory + "/" + package["directory"]
            print ("package: ", package_directory)
            if package["type"] == "git":
                if not os.path.exists(package_directory):
                    # Fetch directory
                    git_clone(package["link"], package_directory)
                
                repo = Repo(package_directory)
                if not is_correct_tag(repo, package["version"]):
                    repo.git.checkout(package["version"])
                print (repo.git.describe())
            else:
                raise "Only git links are supported currently"
            
            if args.use_cmake:
                print ("Generate CMake target: ", package["target"])
                if not os.path.exists(generate_directory):
                    os.makedirs(generate_directory)
                
    # if (args)

main()