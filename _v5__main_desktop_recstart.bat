@ECHO OFF

ECHO;
rem -------------------------------------
ECHO python _v5__main_desktop.py recorder
     python _v5__main_desktop.py recorder
rem -------------------------------------

ECHO;
ECHO bye!

ping localhost -w 1000 -n 5 >nul

EXIT


