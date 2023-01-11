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
            | argument                                           |
            | -i ${data_dir}/package_other_version/packages.json |
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package | file     | content             |
            | simple  | data.txt | branch: some_branch |
        Then CMake Modules are empty

    Scenario: generate CMake modules
        Given we have YASPEM executable
        Given output directory
            """
            simple_dependency_with_module
            """
        When we execute with arguments
            | argument                                         |
            | -i ${data_dir}/simple_git_packages/packages.json |
            | --cmake                                          |
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package | file     | content      |
            | simple  | data.txt | branch: main |
        Then Fetched module contains files
            | file                  |
            | Findsimple.cmake |
        Then CMake is able to find new module

    Scenario: fetch from more than one packages file
        Given we have YASPEM executable
        Given output directory
            """
            multiple_packages_list
            """
        When we execute with arguments
            | argument                                                                                          |
            | -i ${data_dir}/multiple_packages/a/packages.json, ${data_dir}/multiple_packages/b/packages.json   |
            | --cmake                                                                                           |
        Then YASPEM will return 0
        Then YASPEM will fetch it
        Then Fetched package contains files
            | package    | file     | content               |
            | package_a  | data.txt | branch: main          |
            | package_b  | data.txt | branch: some_branch   |
        Then Fetched module contains files
            | file                      |
            | Findpackage_a.cmake       |
            | Findpackage_b.cmake       |
        Then CMake is able to find new module
