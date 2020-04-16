
@echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime  ^| find "."') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"

set datestamp=%YYYY%%MM%%DD%
set obsPath=%systemdrive%%homepath%\AppData\Roaming\obs-studio\basic\scenes\
@echo on

copy "%obsPath%OA_-_Facebook_Live.json" .

start /wait python3 VerseUtil.py

move OA_-_Facebook_Live.json OA_-_Facebook_Live_-_%datestamp%.json

move "OA_-_Facebook_Live_-_%datestamp%.json" "%obsPath%"