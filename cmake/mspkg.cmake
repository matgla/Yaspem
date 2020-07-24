function (initialize_packages)
    find_package (Python3 COMPONENTS Interpreter)
    if (NOT Python3_FOUND)
        message (FATAL_ERROR "Can't find python3 executable")
    endif ()
    message (STATUS "Initializing packages")
    file(GLOB_RECURSE mspkg_executable mspkg.py)
    execute_process(COMMAND ${python_executable} ${mspkg_executable} -o ${CMAKE_CURRENT_BINARY_DIR} --cmake
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    )

    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_BINARY_DIR}/packages/modules PARENT_SCOPE)
endfunction()

function (setup_virtualenv source_directory)
    find_program(virtualenv_exec virtualenv)
    if (NOT virtualenv_exec)
        message (FATAL_ERROR, "Couldn't find virtualenv")
    endif ()

    file (GLOB virtualenv_file_stamp ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
    if (NOT virtualenv_file_stamp)
        message (STATUS "Configure virtualenv: ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv")
        execute_process(
            COMMAND ${virtualenv_exec} -p python3 mspkg_venv
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        )
        execute_process(
            COMMAND mspkg_venv/bin/pip install -r ${source_directory}/requirements.txt --upgrade -q -q -q
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        )

        execute_process(
            COMMAND cmake -E touch ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        )

        set (python_executable ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/bin/python3 CACHE INTERNAL "" FORCE)
        file (GLOB virtualenv_file_stamp ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
        message (STATUS "Virtualenv created, stamp file: ${virtualenv_file_stamp}")
    endif ()
endfunction ()

function (setup_mspkg source_directory)
    message(STATUS "Setup of mspkg started")
    setup_virtualenv(${source_directory})
    initialize_packages()
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/packages/cmake PARENT_SCOPE)
endfunction ()
