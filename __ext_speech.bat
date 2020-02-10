@ECHO OFF

rem ECHO;
ECHO;@%1@%2@%3
rem ECHO;
rem ping localhost -w 1000 -n 3 >nul

start /b python __ext_speech.py %1 %2 %3

EXIT
