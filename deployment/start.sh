#!/bin/bash

APP_NAME=${1}

if [[ $# -ne 1 ]]; then
  echo "You need to provide the name of the app you want to start."
  exit
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"


cd "${SCRIPT_DIR}"/..

heroku ps:scale web=1 --app="${APP_NAME}"
