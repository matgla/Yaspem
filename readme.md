# Yaspem - Yet Another Simple PackagE Manager

![yaspem_logo](https://user-images.githubusercontent.com/10617824/227028304-21982572-b2c9-4364-8593-07b31e7c94bf.png)


The yaspem is tool to manage dependencies within CMake.
It allows to fetch sources automatically with specific version.
Also creates wrapping files to find packages with find_package command.

# Examples

Usage of yaspem can be found under:
[msos](https://github.com/matgla/msos)
[msboot](https://github.com/matgla/ms_boot)
.

# Requirements

Tool is written in Python3 and uses VirtualEnv package to setup environment.
Required software:
```
python3 pip3 virtualenv
```

# Quick-start in your project

These steps should let you easily integrate yaspem into your project.

1. Fetch yaspem into your project, for example with FetchExternal
```cmake
project(...)
...
include(FetchContent)

FetchContent_Declare(
    yaspem
    GIT_REPOSITORY https://github.com/matgla/yaspem.git
    GIT_TAG        master
)

FetchContent_MakeAvailable(yaspem)

```

2. Extend CMake modules with yaspem cmake scripts
```cmake
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${yaspem_SOURCE_DIR}/cmake)
```

3. Setup yaspem (in this step packages.json file is parsed and dependencies fetched)
```cmake
include(yaspem)
setup_yaspem(${yaspem_SOURCE_DIR})
```

4. Find required dependencies with ```find_package(<target_name>)```
```cmake
find_package(eul)
```

5. Create package.json file (currently, yaspem is searching in ```${PROJECT_SOURCE_DIR}```
```javascript
{
    "dependencies": [
        {
            "link": "https://github.com/matgla/EmbeddedUtilityLibraries.git",
            "type": "git",
            "version": "master",
            "target": "eul",
            "options": {
                "cmake_variables": {
                    "DISABLE_TESTS": "ON",
                    "DISABLE_SANITIZERS": "ON"
                }
            }
        }
    ]
}
```

# Packages file format

Format of ```package.json``` file:
```javascript
{
    "dependencies": [
        {<package_1>},
        {<package_2>}
    ]
}
```

Format of ```package object```:
```javascript
{
    "link": "<url_to_package>",
    "type": "<repository_type>",
    "version": "<repository_version>",
    "target": "<target_name>",
    "options": {<additional_options>}
}
```

Parameters:

**Mandatory**
```
<repository_type>: currently only git is supported
<repository_version>: repository version
    * For git:
        - tag
        - commit hash
        - branch name
<target>: name which will be used in find_package

```

**Optional**
```
<directory>: directory to fetch package
<cmake_variables>: array of variables to be setup in module, i.e
"cmake_variables": {
    "variable_1": "value_1",
    "variable_2": "value_2"
}
```

**Options**
```is_cmake_library```: generated module adds package to ```CMAKE_MODULE_PATH```
```create_library```: creates library before ```add_subdirectory``` call
Structure for ```create_library```
```javascript
"create_library": {
    "type": "[STATIC]",
    "sources_filter": ["*.cpp", "..."],
    "include_directories": ["include"],
    "sources_directory": "<path_to_source>"
    "compile_definitions": ["-DFLAG=1"]
}
```
Path in include_directories and source_filter/directory has root in ```${yaspem_SOURCE_DIR}/packages/sources/<package>```

# How this is working

With default options ```yaspem``` expects that provided repository has CMake package.

1. When ```setup_yaspem``` is called yaspem:
    1. parses ```packages.json``` and fetches sources to ```<path_to_yaspem>/packages/sources```
    1. generates CMake module files to ```<path_to_yaspem>/packages/modules```
1. When ```find_package``` is called package is searched and added to project.
    1. In default option module automatically calls add_subdirectory on fetched files
    1. When package is marked as ```cmake_library``` then package is added to CMAKE_MODULE_PATH
    1. When library generation is enabled then module searches source files and packages and creates library. After that
       add_subdirectory is called.

# API

Functions exported by yaspem.cmake

```cmake
setup_yaspem(<path to yaspem sources>)
```

Variables exported by module:
```cmake
${package_name_SOURCE_DIR}: directory to package sources
```

# Features to be implemented:

- [x] Add argument to specify path for packages

