function(yaspem_initialize_packages source_directory output_directory
         package_files)
  find_package(Python3 COMPONENTS Interpreter)
  if(NOT Python3_FOUND)
    message(FATAL_ERROR "Can't find python3 executable")
  endif()
  include(yaspem)

  if(NOT yaspem_executable)
    set(yaspem_executable
        "${source_directory}/yaspem.py"
        CACHE INTERNAL "" FORCE)
  endif()

  set(yaspem_args "-o ${output_directory}")
  list(APPEND yaspem_args "--cmake")
  string(REPLACE ";" " " package_files "${package_files}")

  if(NOT "${package_files}" STREQUAL "")
    list(APPEND yaspem_args "-i ${package_files}")
  endif()

  message(
    STATUS
      "Command: '${python_executable} ${yaspem_executable} ${yaspem_args}' in ${CMAKE_BINARY_DIR}"
  )
  execute_process(
    COMMAND ${python_executable} ${yaspem_executable} ${yaspem_args}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND_ERROR_IS_FATAL ANY)
endfunction()

function(yaspem_setup_virtualenv source_directory)
  find_program(virtualenv_exec virtualenv)
  if(NOT virtualenv_exec)
    message(FATAL_ERROR, "Couldn't find virtualenv")
  endif()

  file(GLOB virtualenv_file_stamp
       ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
  if(NOT virtualenv_file_stamp)
    message(
      STATUS "Configure virtualenv: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv")
    execute_process(
      COMMAND ${virtualenv_exec} -p python3 yaspem_venv
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} COMMAND_ERROR_IS_FATAL ANY)

    if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/pip)
      set(yaspem_pip ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/pip)
    elseif(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/pip.exe)
      set(yaspem_pip ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/pip.exe)
    else()
      message(
        FATAL_ERROR
          "Can't find pip executable under: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv"
      )
    endif()

    execute_process(
      COMMAND ${yaspem_pip} install -r ${source_directory}/requirements.txt
              --upgrade -q -q -q WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                                                   COMMAND_ERROR_IS_FATAL ANY)

    execute_process(
      COMMAND cmake -E touch ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} COMMAND_ERROR_IS_FATAL ANY)

    file(GLOB virtualenv_file_stamp
         ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
    message(STATUS "Virtualenv created, stamp file: ${virtualenv_file_stamp}")
  endif()
  if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/python3)
    set(python_executable
        ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/python3
        CACHE INTERNAL "" FORCE)
  elseif(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/python.exe)
    set(python_executable
        ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/python.exe
        CACHE INTERNAL "" FORCE)
  else()
    message(
      FATAL_ERROR
        "Can't find python 3 executable under: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv"
    )
  endif()

endfunction()

macro(setup_yaspem)
  set(options "")
  set(oneValueArgs YASPEM_SOURCE OUTPUT_DIRECTORY)
  set(multipleValueArgs PACKAGE_FILES)
  cmake_parse_arguments(SETUP_YASPEM "" "${oneValueArgs}"
                        "${multipleValueArgs}" ${ARGN})
  yaspem_setup_virtualenv(${SETUP_YASPEM_YASPEM_SOURCE})
  if(NOT SETUP_YASPEM_PACKAGE_FILES)
    set(SETUP_YASPEM_PACKAGE_FILES "none")
  endif()
  yaspem_initialize_packages(
    ${SETUP_YASPEM_YASPEM_SOURCE} ${SETUP_YASPEM_OUTPUT_DIRECTORY}
    "${SETUP_YASPEM_PACKAGE_FILES}")
  message(STATUS "")
  set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
                        ${SETUP_YASPEM_OUTPUT_DIRECTORY}/modules)
endmacro()
