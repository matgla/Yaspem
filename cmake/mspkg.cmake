function (initialize_packages)
    find_package (Python3 COMPONENTS Interpreter)
    if (NOT Python3_FOUND)
        message (FATAL_ERROR "Can't find python3 executable")
    endif ()
    execute_process(COMMAND ${Python3_EXECUTABLE} mspkg.py --cmake
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    )

endfunction ()

function (setup_mspkg)
    message(STATUS "Setup of mspkg started")
    initialize_packages()
    set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/packages/cmake)
endfunction ()