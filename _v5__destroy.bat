@ECHO OFF

rem ECHO;
rem ECHO taskkill /im python.exe /f
rem      taskkill /im python.exe /f

ECHO;
ECHO python _v5__destroy.py
     python _v5__destroy.py

ping localhost -w 1000 -n 5 >nul

EXIT


