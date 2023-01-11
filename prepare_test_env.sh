#!/bin/bash

case "$(uname -sr)" in
    CYGWIN*|MINGW*|MINGW32*|MSYS*)
        pip_exec=test_env/Scripts/pip3.exe;;
    *)
        pip_exec=test_env/bin/pip3;;
esac

panic() { echo "$*" >&2; exit 2; }

remove_test_env() { rm -rf test_env; }

install_packages() { $pip_exec install -r tests/bdd/requirements.txt --upgrade; }

prepare_virtual_env() {
    if [ -f test_env/pyvenv.cfg ]; then
        echo "-- Virtual env exists, creation skipped.";
    else
        virtualenv --python=python3 test_env;
    fi
}

while getopts cr-: OPT
do
    # support long options: https://stackoverflow.com/a/28466267/519360
    if [ "$OPT" = "-" ]; then
        OPT="${OPTARG%%=*}"
    fi
    case "${OPT}" in
        r | remove )    remove_test_env;;
        c | clear )     remove_test_env && exit 0;;
        ??* )           panic "Unknown argument --$OPT";;
        ? )             exit 2;;
    esac
done
shift $((OPTIND-1))

echo "-- Remove test env"
echo "-- Prepare virtual env"
prepare_virtual_env;
echo "-- Install python packages"
install_packages;
