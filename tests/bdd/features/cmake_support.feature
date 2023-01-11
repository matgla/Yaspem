Feature: Generation of CMake modules

    Scenario: Generate module for Simple Package
        Given we have CMake
        Given output directory
            """
            cmake_simple_package
            """
        When we configure project
            """
            generate_cmake_target
            """
        Then stdout contains 
            """
            Called CMakeLists from main
            """
        Then stdout contains 
            """
            Generate CMake target:  simple
            """
        