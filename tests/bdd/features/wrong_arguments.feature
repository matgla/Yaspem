Feature: React to wrong usage

    Scenario: Show error when output directory not provided
        Given we have YASPEM executable
        When we execute with arguments
            | argument |
        Then YASPEM will show usage text
        Then YASPEM will show required argument
            | argument    |
            | -o/--output |
        Then YASPEM will return error code

    Scenario: Show error when default input file not found
        Given we have YASPEM executable
        When we execute with arguments
            | argument    |
            | -o test_dir |
        Then YASPEM will show error
            | text                                        |
            | error: input file 'packages.json' not found |
        Then YASPEM will return error code


    Scenario: Show error when provided input file not found
        Given we have YASPEM executable
        When we execute with arguments
            | argument          |
            | -i test_file.json |
            | -o test_dir       |
        Then YASPEM will show error
            | text                                         |
            | error: input file 'test_file.json' not found |
        Then YASPEM will return error code