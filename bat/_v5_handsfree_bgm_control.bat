@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp              MKDIR temp
IF NOT EXIST temp\_log         MKDIR temp\_log
IF NOT EXIST temp\a3_5tts_txt  MKDIR temp\a3_5tts_txt

start "" python _v5_handsfree_bgm_control.py debug temp/temp_bgm_control.txt

SET speech=bgm
ECHO;
ECHO %speech%
ECHO %speech%>temp\temp_bgm_control.txt

rem PAUSE

:LOOP

ECHO;
SET speech=
set /P speech="ˆ—‚µ‚½‚¢•¶Žš(ja)F"
IF %speech%@==@  SET speech=_close_
ECHO %speech%>temp\temp_bgm_control.txt

IF %speech%@==_close_@  GOTO ABEND

GOTO LOOP

:ABEND
PAUSE


