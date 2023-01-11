function (initialize_packages package_files)
    find_package (Python3 COMPONENTS Interpreter)
    if (NOT Python3_FOUND)
        message (FATAL_ERROR "Can't find python3 executable")
    endif ()
    include (yaspem)

    if (NOT yaspem_executable)
        set (yaspem_executable "${yaspem_SOURCE_DIR}/yaspem.py" CACHE INTERNAL "")
    endif()

    set (yaspem_command "${python_executable} ${yaspem_executable} -o ${yaspem_SOURCE_DIR} --cmake")
    if (package_files)
        set (yaspem_command "${yaspem_command} -i ${package_files}")
    endif ()

    message (STATUS "Command: ${yaspem_command}")
    execute_process(COMMAND ${yaspem_command}
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
        message (STATUS "Configure virtualenv: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv")
        execute_process(
            COMMAND ${virtualenv_exec} -p python3 yaspem_venv
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/pip)
            set (yaspem_pip ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/pip)
        elseif (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/pip.exe)
            set (yaspem_pip ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/pip.exe)
        else ()
            message (FATAL_ERROR "Can't find pip executable under: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv")
        endif ()

        execute_process(
            COMMAND ${yaspem_pip} install -r ${source_directory}/requirements.txt --upgrade -q -q -q
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        execute_process(
            COMMAND cmake -E touch ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMAND_ERROR_IS_FATAL ANY
        )

        if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/python3)
            set (python_executable ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/bin/python3 CACHE INTERNAL "" FORCE)
        elseif (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/python.exe)
            set (python_executable ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv/Scripts/python.exe CACHE INTERNAL "" FORCE)
        else ()
            message (FATAL_ERROR "Can't find python 3 executable under: ${CMAKE_CURRENT_BINARY_DIR}/yaspem_venv")
        endif ()


        file (GLOB virtualenv_file_stamp ${CMAKE_CURRENT_BINARY_DIR}/virtualenv_file.stamp)
        message (STATUS "Virtualenv created, stamp file: ${virtualenv_file_stamp}")
    endif ()
endfunction ()

function (setup_yaspem source_directory package_files)
    setup_virtualenv(${source_directory})
    initialize_packages(${package_files})
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${yaspem_SOURCE_DIR}/packages/modules PARENT_SCOPE)
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${yaspem_SOURCE_DIR}/packages/modules)

endfunction ()
