@ECHO OFF

ECHO;
rem -----------------------------------------------
ECHO start /b cmd /c _v5_proc_recorder.exe recorder
     start /b cmd /c _v5_proc_recorder.exe recorder
ECHO start /b cmd /c _v5_proc_blobup.exe   recorder
     start /b cmd /c _v5_proc_blobup.exe   recorder
rem -----------------------------------------------

ECHO;
ECHO bye!

ping localhost -w 1000 -n 5 >nul

EXIT


