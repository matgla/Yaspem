Feature: Fetching provided dependencies

    Scenario: fetch dependency from git
        Given we have YASPEM executable
        Given output directory
            """
            simple_dependency
            """
        When we execute with arguments
            | argument                                         |
            | -i ${data_dir}/simple_git_packages/packages.json |
        Then YASPEM will not print on stderr
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package | file     | content      |
            | simple  | data.txt | branch: main |
        Then CMake Modules are empty


    Scenario: fetch other version from git
        Given we have YASPEM executable
        Given output directory
            """
            other_version
            """
        When we execute with arguments
            | argument                                         |
            | -i ${data_dir}/package_other_version/packages.json |
        Then YASPEM will not print on stderr
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package | file     | content             |
            | simple  | data.txt | branch: some_branch |

    Scenario: generate CMake modules
        Given we have YASPEM executable
        Given output directory
            """
            simple_dependency
            """
        When we execute with arguments
            | argument                                         |
            | -i ${data_dir}/simple_git_packages/packages.json |
            | --cmake                                          |
        Then YASPEM will not print on stderr
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package | file     | content      |
            | simple  | data.txt | branch: main |
        Then Fetched module contains files
            | file                  |
            | Findsimple_test.cmake |
        Then CMake is able to find new module
