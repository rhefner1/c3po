#!/usr/bin/env bash

if [[ $RUN_TESTS == true ]]
then
    echo -e "### Adding SDK to Python path"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine/lib/yaml-3.10"
    echo "Current PYTHONPATH: ${PYTHONPATH}"

    echo -e "\n### Running unit tests"
    nosetests  --with-coverage --cover-package=c3po
fi
