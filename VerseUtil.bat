
@echo off
for /f "delims=" %%a in ('wmic OS Get localdatetime  ^| find "."') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"

set datestamp=%YYYY%%MM%%DD%
set obsPath=%systemdrive%%homepath%\AppData\Roaming\obs-studio\basic\scenes\
@echo on

copy "C:\Users\Open Arms\Sync\Open Arms\Resources\Scripture for Livestream.txt" verses.txt

copy "%obsPath%OA_-_Facebook_Live.json" .

start /wait "C:\Users\Open Arms\AppData\Local\Programs\Python\Python38-32\python.exe" VerseUtil.py

move OA_-_Facebook_Live.json OA__Facebook_Live_-_%datestamp%.json

move "OA__Facebook_Live_-_%datestamp%.json" "%obsPath%"

pause