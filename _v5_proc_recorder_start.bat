@ECHO OFF

ECHO;
rem ----------------------------------------
ECHO start "" _v5_proc_recorder.exe recorder
     start "" _v5_proc_recorder.exe recorder
ECHO start "" _v5_proc_blobup.exe   recorder
     start "" _v5_proc_blobup.exe   recorder
rem ----------------------------------------

ECHO;
ECHO bye!

ping localhost -w 1000 -n 5 >nul

EXIT


