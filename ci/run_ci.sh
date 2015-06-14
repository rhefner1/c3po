#!/usr/bin/env sh

echo -e "\n\n### Installing App Engine SDK"
cd ci
curl -o ./appengine_sdk.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.22.zip
unzip -q ./appengine_sdk.zip
cd ..

echo -e "\n\n### Adding SDK to Python path"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/ci/google_appengine/lib/yaml-3.10"
echo "Current PYTHONPATH: ${PYTHONPATH}"

echo -e "\n\n### Installing pip requirements"
pip install -t lib -r requirements.txt

echo -e "\n\n### Running unit tests"
python -m unittest discover

echo -e  "\n\n### Cleaning up"
rm -rf ./ci/google_appengine
rm -f ./ci/appengine_sdk.zip
