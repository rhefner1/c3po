#!/usr/bin/env bash

echo -e "### Adding SDK to Python path"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine/lib/yaml-3.10"
echo "Current PYTHONPATH: ${PYTHONPATH}"

echo -e "\n### Running unit tests"
python -m unittest discover
pylint c3po
pylint tests
