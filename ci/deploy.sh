#!/usr/bin/env bash

echo -e "\n\n### Installing pip requirements to lib directory"
pip install -t lib -r requirements.txt

echo -e "\n\n### Deploying to App Engine"
cd ./ci/google_appengine
python appcfg.py update --oauth2_refresh_token=$AE_OAUTH_REFRESH ../../
