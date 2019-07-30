@ECHO OFF

ECHO _start_>"temp\control_recorder.txt"

ECHO;
rem ------------------------------------
ECHO python _v5__main_recorder.py camera
     python _v5__main_recorder.py camera
rem ------------------------------------

ECHO;
ECHO bye!
ping localhost -w 1000 -n 5 >nul

EXIT


