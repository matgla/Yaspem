#!/bin/bash

case "$(uname -sr)" in
    CYGWIN*|MINGW*|MINGW32*|MSYS*)
        python_exec=test_env/Scripts/python3.exe;;
    *)
        python_exec=test_env/bin/python3;;
esac

pwd;
ls ../../test_env;
ls ../../test_env/Scripts;
cd tests/bdd && ../../$python_exec -m behave;
