cmake_minimum_required(VERSION 3.17)
project (MSPKGTest CXX)


set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/cmake)
include(mspkg)

setup_mspkg()

find_package(sml)


add_executable(main main.cpp)