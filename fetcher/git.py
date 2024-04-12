#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# git_fetch.py
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

from git import Repo, RemoteProgress, GitCommandError

import shutil

from pathlib import Path

from fetch_result import FetchResult

class GitRemoteProgress(RemoteProgress):
    def __init__(self, parser_callback, package):
        super().__init__()
        self.package = package 
        self.callback = parser_callback
        
    def update(self, op_code, cur_count, max_count=None, message=""):
        if int(cur_count) != 0: 
            percent = int(float(cur_count)/float(max_count) * 100)
        else:
            if op_code & RemoteProgress.END:
                percent = 100
            else: 
                percent = 0

        text = ""
        if op_code & RemoteProgress.COUNTING:
            text = "   counting "
        elif op_code & RemoteProgress.COMPRESSING:
            text = "compressing "
        elif op_code & RemoteProgress.RECEIVING:
            text = "  receiving "
        elif op_code & RemoteProgress.RESOLVING:
            text = "  resolving "

        text += "[{:<3}%]".format(percent)
        
        self.callback(self.package, text)

class GitFetch:
    def __init__(self, cache_directory, progress_callback, submodule_update_callback, force, noupdate, nocompatibility_check):
        self.cache_directory = cache_directory
        self.progress_callback = progress_callback
        self.submodule_update_callback = submodule_update_callback
        self.force = force
        self.noupdate = noupdate
        self.nocompatibility_check = nocompatibility_check

    def fetch(self, package):
        package_path = Path(self.cache_directory) / package["target"] 
       
        msg = "" 
        if self.force:
            if package_path.exists():
                shutil.rmtree(package_path, ignore_errors = False)
        
        if not package_path.exists():
            Repo.clone_from(package["link"], package_path, progress=GitRemoteProgress(self.progress_callback, package))    
            
        repo = Repo(package_path)  
        if not self.noupdate:
            repo.git.fetch()
        try: 
            repo.git.checkout(package["version"])

        except GitCommandError as err:
            msg = "Can't find version: {}".format(package["version"])
            return FetchResult(False, msg)
        
        allBranches = repo.git.branch("--all").split()
        if package["version"] in allBranches:
            repo.git.pull()
  
        for submodule in repo.submodules:
            self.submodule_update_callback(package, str(submodule))
            repo.git.submodule("update", "--init", "--", str(submodule.path))
        msg = "Fetched " + package["version"]

        return FetchResult(True, msg)
