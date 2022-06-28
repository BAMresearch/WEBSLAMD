echo off

set key=%1

if "%~1" == "" (
 echo ERROR: You need to pass a key to start your app. For testing use any string.
 GOTO:eof
)

set FLASK_ENV=development
set FLASK_APP=app.py
set SECRET_KEY=%key%
python app.py
pause
