function (initialize_packages)
    find_package (Python3 COMPONENTS Interpreter)
    if (NOT Python3_FOUND)
        message (FATAL_ERROR "Can't find python3 executable")
    endif ()
    include (mspkg)

    if (NOT mspkg_executable)
        set (mspkg_executable "${mspkg_SOURCE_DIR}/mspkg.py" CACHE INTERNAL "")
    endif()

    message (STATUS "Command: ${python_executable} ${mspkg_executable} -o ${mspkg_SOURCE_DIR} --cmake")
    execute_process(COMMAND ${python_executable} ${mspkg_executable} -o ${mspkg_SOURCE_DIR} -b ${mspkg_BINARY_DIR} --cmake
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
        COMMAND_ERROR_IS_FATAL ANY
    )

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
            COMMAND_ERROR_IS_FATAL ANY
        )

        if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/bin/pip)
            set (mspkg_pip ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/bin/pip)
        else if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/Scripts/pip.exe) 
            set (mspkg_pip ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/Scripts/pip.exe) 
        else () 
            message (FATAL_ERROR "Can't find pip executable under: ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv")
        endif ()

        execute_process(
            COMMAND ${mspkg_pip} install -r ${source_directory}/requirements.txt --upgrade -q -q -q
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        execute_process(
            COMMAND cmake -E touch ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/bin/python3)
            set (python_executable ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/bin/python3 CACHE INTERNAL "" FORCE)
            else if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/Scripts/python) 
            set (python_executable ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv/Scripts/python CACHE INTERNAL "" FORCE)
        else () 
            message (FATAL_ERROR "Can't find python 3 executable under: ${CMAKE_CURRENT_BINARY_DIR}/mspkg_venv")
        else ()


        file (GLOB virtualenv_file_stamp ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
        message (STATUS "Virtualenv created, stamp file: ${virtualenv_file_stamp}")
    endif ()
endfunction ()

function (setup_mspkg source_directory)
    setup_virtualenv(${source_directory})
    initialize_packages()
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${mspkg_SOURCE_DIR}/packages/modules PARENT_SCOPE)
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${mspkg_SOURCE_DIR}/packages/modules)

endfunction ()
