#!/bin/bash

APP_NAME=${1}

if [[ $# -ne 1 ]]; then
  echo "You need to provide the name your app and key and value for the environment variable."
  exit
fi

cd "${SCRIPT_DIR}"/..

heroku logs --app="${APP_NAME}" --tail