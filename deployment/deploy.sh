#!/bin/bash

BRANCH_NAME=${1}
STAGE_NAME=${2}

if [[ $# -ne 2 ]]; then
  echo "You need to provide the branch you want to deploy and the name of the stage."
  exit
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"

cd "${SCRIPT_DIR}"/..

git push "${STAGE_NAME}" "${BRANCH_NAME}":master
