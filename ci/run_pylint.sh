#!/usr/bin/env bash

if [[ $RUN_PYLINT == true ]]
then
    echo -e "### Adding SDK to Python path"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine"
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine/lib/yaml-3.10"
    echo "Current PYTHONPATH: ${PYTHONPATH}"

    echo -e "\n### Running pylint"
    pylint c3po --ignore tests --disable=no-member --disable too-few-public-methods --disable unused-argument --disable too-many-return-statements --disable too-many-arguments
    pylint c3po/tests --disable=no-member --disable too-few-public-methods --disable unused-argument --disable missing-docstring --disable protected-access --disable duplicate-code --disable too-many-arguments
fi
