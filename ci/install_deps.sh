#!/usr/bin/env sh

echo -e "\n\n### Installing App Engine SDK"
cd ci
curl -o ./appengine_sdk.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.22.zip
unzip -q ./appengine_sdk.zip
cd ..

echo -e "\n\n### Installing pip requirements"
pip install -t lib -r requirements.txt
