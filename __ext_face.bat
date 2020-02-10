@ECHO OFF

rem ECHO;
rem ECHO;@%1@%2
rem ECHO;
rem ping localhost -w 1000 -n 3 >nul

start /b python __ext_face.py %1 %2

EXIT
