@ECHO OFF

ECHO;
ECHO python _v5__destroy.py
     python _v5__destroy.py

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO taskkill /im python.exe /f
     taskkill /im python.exe /f

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

EXIT


