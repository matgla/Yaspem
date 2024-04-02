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
    def set_cache_output_directory(path):
        LocalCache.file = path / "cache.json"
        if LocalCache.file.exists():
            with open(cache, "r") as file:
                LocalCache.data = json.loads(file.read())
            if not "timestamps" in LocalCache.data:
                LocalCache.data["timestamps"] = {} 
        
    def update_cache_entry(package):
        if not package["target"] in LocalCache.data:
            LocalCache.data[package["target"]] = {
                "timestamp" = datetime.timestamp(datetime.now()),
                "version" = package["version"] 
            }


    def store():
        if LocalCache.data != None and LocalCache.file != None:
            with open(cache_file, "w") as file:
                file.write(json.dumps(LocalCache.data))
    

