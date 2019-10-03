@ECHO OFF

ECHO;
rem -----------------------------------------------
ECHO start /b cmd /c _v5_proc_adintool.exe  speech
     start /b cmd /c _v5_proc_adintool.exe  speech
ECHO start /b cmd /c _v5_proc_voice2wav.exe speech
     start /b cmd /c _v5_proc_voice2wav.exe speech
ECHO start /b cmd /c _v5_proc_coreSTT.exe   speech  azure
     start /b cmd /c _v5_proc_coreSTT.exe   speech  azure
ECHO start /b cmd /c _v5_proc_txtreader.exe sendkey
     start /b cmd /c _v5_proc_txtreader.exe sendkey
ECHO start /b cmd /c _v5_proc_coreTTS.exe   speech  azure
     start /b cmd /c _v5_proc_coreTTS.exe   speech  azure
ECHO start /b cmd /c _v5_proc_playvoice.exe speech
     start /b cmd /c _v5_proc_playvoice.exe speech
rem -----------------------------------------------

ECHO;
PING localhost -w 1000 -n 5 >nul

ECHO;
ECHO start!

ECHO;
ping localhost -w 1000 -n 5 >nul

EXIT


