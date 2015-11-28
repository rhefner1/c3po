#!/usr/bin/env bash

echo -e "### Installing App Engine SDK"
cd ci
curl -o ./appengine_sdk.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.28.zip
unzip -q ./appengine_sdk.zip
cd ..

echo -e "\n### Installing pip requirements"
pip install -r requirements.txt
