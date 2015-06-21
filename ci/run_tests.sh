#!/usr/bin/env bash

echo -e "### Adding SDK to Python path"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine/lib/yaml-3.10"
echo "Current PYTHONPATH: ${PYTHONPATH}"

echo -e "\n### Running unit tests"
python -m unittest discover

echo -e "\n### Running pylint"
pylint c3po --disable=no-member --disable too-few-public-methods --disable unused-argument
pylint tests --disable=no-member --disable too-few-public-methods --disable unused-argument --disable missing-docstring --disable protected-access
