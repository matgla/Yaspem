Feature: CMake fetches from multiple packages

    Scenario: Generate modules for multiple package lists 
        Given we have CMake
        Given output directory
            """
            cmake_multiple_package_files
            """
        When we configure project
            """
            generate_cmake_multiple_package_files
            """
        Then stdout contains 
            """
            Called CMakeLists from main
            """
        Then stdout contains 
            """
            Generate CMake target:  package_a 
            """
        Then stdout contains 
            """
            Generate CMake target:  package_b 
            """
 
