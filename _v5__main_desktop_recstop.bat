@ECHO OFF

IF EXIST "temp\control_desktop.txt"  DEL "temp\control_desktop.txt" 
ECHO _end_>"temp\control_desktop.tmp"
RENAME "temp\control_desktop.tmp" "control_desktop.txt"

ECHO;
PING localhost -w 1000 -n 5 >nul

EXIT


