@ECHO OFF

ECHO _close_>"temp\control_desktop.tmp"
rename "temp\control_desktop.tmp" "control_desktop.txt"

ECHO;
ping localhost -w 1000 -n 5 >nul

EXIT


