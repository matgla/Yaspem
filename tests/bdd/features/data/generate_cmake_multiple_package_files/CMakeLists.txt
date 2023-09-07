cmake_minimum_required(VERSION 3.25)

project(cmake_test NONE)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${YASPEM_ROOT}/cmake)
include(yaspem)

message(STATUS "ROOT:  ${YASPEM_ROOT}")

setup_yaspem(
  YASPEM_SOURCE
  ${YASPEM_ROOT}
  OUTPUT_DIRECTORY
  ${CMAKE_CURRENT_BINARY_DIR}
  PACKAGE_FILES
  ${CMAKE_CURRENT_LIST_DIR}/packages_a.json
  ${CMAKE_CURRENT_LIST_DIR}/packages_b.json)

find_package(package_a REQUIRED)
find_package(package_b REQUIRED)
