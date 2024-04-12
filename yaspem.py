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

from platformdirs import user_cache_dir 

from arguments import parse_arguments
from packages_parser import PackagesParser 


import colorama

from cache import LocalCache

def main():
    colorama.init()
    print(colorama.Fore.CYAN + "YASPEM - Packages manager" + colorama.Style.RESET_ALL)
    args = parse_arguments() 

    LocalCache.set_cache_output_directory(args.output)
    cache_directory = user_cache_dir("yaspem", "Mateusz Stadnik")
    parser = PackagesParser(cache_directory, args) 
    parser.parse_packages(args)  

main()
