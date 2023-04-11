#!/bin/bash

case "$(uname -sr)" in
    CYGWIN*|MINGW*|MINGW32*|MSYS*)
        python_exec=test_env/Scripts/python.exe;;
    *)
        python_exec=test_env/bin/python3;;
esac

cd tests/bdd && ../../$python_exec -m behave;
