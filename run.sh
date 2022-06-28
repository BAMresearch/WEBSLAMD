#!/bin/bash

key=${1}

if [[ $# -ne 1 ]]; then
  echo "ERROR: You need to pass a key to start your app. For testing use any string."
  exit
fi

export FLASK_ENV=development
export FLASK_APP=app.py
export SECRET_KEY=${key}
python app.py
