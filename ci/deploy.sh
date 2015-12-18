#!/usr/bin/env bash

if [[ $TRAVIS_BRANCH == "master" && $TRAVIS_PULL_REQUEST == false && $RUN_TESTS == true ]]
then
    echo -e "### Installing pip requirements to lib directory"
    pip install -t lib -r requirements.txt

    echo -e "\n### Deploying to App Engine"
    python ./ci/google_appengine/appcfg.py update --oauth2_refresh_token=$AE_OAUTH_REFRESH app.yaml analytics_app.yaml history_upload_app.yaml
fi
