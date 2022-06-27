#!/bin/bash

APP_NAME=${1}

if [[ $# -ne 1 ]]; then
  echo "You need to provide the name of your app."
  exit
fi

cd "${SCRIPT_DIR}"/..

heroku logs --app="${APP_NAME}" --tail
