#!/bin/bash

APP_NAME=${1}
STAGE_NAME=${2}

if [[ $# -ne 2 ]]; then
  echo "You need to provide name and stage of your app."
  exit
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"

# shellcheck disable=SC2164
cd "${SCRIPT_DIR}"/..

heroku create "${APP_NAME}" --remote "${STAGE_NAME}"
