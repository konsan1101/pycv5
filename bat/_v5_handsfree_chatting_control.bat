@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp              MKDIR temp
IF NOT EXIST temp\_log         MKDIR temp\_log
IF NOT EXIST temp\a3_5tts_txt  MKDIR temp\a3_5tts_txt

start "" python _v5_handsfree_chatting_control.py debug temp/temp_chatting.txt

SET speech=�P�H���m���Ă��܂���
ECHO;
ECHO %speech%
ECHO %speech%>temp\temp_chatting.txt

rem PAUSE

:LOOP

ECHO;
SET speech=
set /P speech="��������������(ja)�F"
IF %speech%@==@  SET speech=_close_
ECHO %speech%>temp\temp_chatting.txt

IF %speech%@==_close_@  GOTO ABEND

GOTO LOOP

:ABEND
PAUSE


