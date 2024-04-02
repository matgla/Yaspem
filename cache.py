#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# cache.py
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

import json
import datetime 

class LocalCache:
    @staticmethod
    def set_cache_output_directory(path):
        LocalCache.file = path / "cache.json"
        LocalCache.data = {} 
        if LocalCache.file.exists():
            with open(LocalCache.file, "r") as file:
                LocalCache.data = json.loads(file.read())
        if not "timestamps" in LocalCache.data:
            LocalCache.data["timestamps"] = {} 
    
    @staticmethod 
    def __get_package_entry_name(package):
        return package["target"] + "@" + package["version"] 
    
    @staticmethod
    def update_cache_entry(package):
        package_entry = LocalCache.__get_package_entry_name(package)
        if not package["target"] in LocalCache.data:
            LocalCache.data[package_entry] = datetime.timestamp(datetime.now())

    @staticmethod 
    def contains(package):
        package_entry = LocalCache.__get_package_entry_name(package)
        if package_entry in LocalCache.data:
            return True 
        return False 
            
    @staticmethod
    def store():
        if LocalCache.data != None and LocalCache.file != None:
            with open(LocalCache.file, "w") as file:
                file.write(json.dumps(LocalCache.data))
    

