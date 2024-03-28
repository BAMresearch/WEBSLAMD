#!/bin/bash

key=${1}
token=${2}

if [[ $# -ne 2 ]]; then
  echo "ERROR: You need to pass a key and token to start your app. For testing use any strings."
  exit
fi

export FLASK_ENV=development
export FLASK_APP=app.py
export SECRET_KEY=${key}
export OPENAI_API_TOKEN=${token}
python app.py
