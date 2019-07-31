@ECHO OFF

ECHO;
rem -------------------------------------------------
ECHO start "" /b python _v5__main_desktop.py recorder
     start "" /b python _v5__main_desktop.py recorder
rem -------------------------------------------------

ECHO;
ping localhost -w 1000 -n 10 >nul

ECHO _rec_start_
ECHO _rec_start_>"temp\control_desktop.tmp"
rename "temp\control_desktop.tmp" "control_desktop.txt"

EXIT


