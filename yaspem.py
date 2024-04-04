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
    parser = PackagesParser(cache_directory, args) 
    parser.parse_packages(args)  

main()
