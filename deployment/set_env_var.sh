#!/bin/bash

APP_NAME=${1}
KEY=${2}
VALUE=${3}

if [[ $# -ne 3 ]]; then
  echo "You need to provide the name your app and key and value for the environment variable."
  exit
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"

# shellcheck disable=SC2164
cd "${SCRIPT_DIR}"/..

heroku config:set --app="${APP_NAME}" "${KEY}"="${VALUE}"
