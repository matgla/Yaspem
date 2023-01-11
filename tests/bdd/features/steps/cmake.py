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

import pathlib
import platform
import subprocess
import os

from behave import *

working_dir = pathlib.Path(__file__).parent.parent.parent.parent.parent
test_dir = pathlib.Path(__file__).parent.parent

cmake_executable = "Scripts/cmake.exe" if platform.system() == "Windows" else "bin/cmake"

def execute_cmake(context, args):
    cmake_path = working_dir.resolve() / "test_env" / cmake_executable
    call_args = [str(cmake_path)]
    call_args.extend(args)
    context.output = subprocess.run(call_args, cwd=context.output_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if context.output_dir:
        with open(context.output_dir / "cmake.log", "w") as f:
            f.write(context.output.stdout)
    context.stdout = context.output.stdout

@given("we have CMake")
def step_impl(context):
    context.cmake_exec = execute_cmake

@when("we configure project")
def step_impl(context):
    os.makedirs(context.output_dir)
    cmake_args = []
    if context.text:
        cmake_args = [pathlib.Path(test_dir / "data" / context.text.strip()), "-DYASPEM_ROOT="+str(working_dir.as_posix())]
    context.cmake_exec(context, cmake_args)

@then("stdout contains")
def step_impl(context):
    assert context.text.strip() in context.stdout, "'" + context.text.strip() + "'"