@ECHO OFF

IF EXIST "temp\control_speech.txt"  DEL "temp\control_speech.txt" 
ECHO _end_>"temp\control_speech.tmp"
RENAME "temp\control_speech.tmp" "control_speech.txt"

ECHO;
PING localhost -w 1000 -n 5 >nul

ECHO;
ECHO bye!

ECHO;
ping localhost -w 1000 -n 5 >nul

EXIT



