echo off

set key=%1
set token=%2

if "%~1" == "" (
 echo ERROR: You need to pass a key and token to start your app. For testing use any strings.
 GOTO:eof
)

set FLASK_ENV=development
set FLASK_APP=app.py
set SECRET_KEY=%key%
set OPENAI_API_TOKEN=%token%
python app.py
pause
