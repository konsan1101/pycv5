@ECHO OFF

ECHO;
ECHO taskkill /im msaccess.exe /f
     taskkill /im msaccess.exe /f

ECHO;
ECHO python _v5__destroy.py
     python _v5__destroy.py

ping localhost -w 1000 -n 5 >nul

EXIT


