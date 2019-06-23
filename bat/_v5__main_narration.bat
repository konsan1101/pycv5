@ECHO OFF
CALL __setpath.bat

ECHO;
ECHO ���̓t�@�C�����݊m�F
IF NOT EXIST "narration\1.���̓e�L�X�g_sjis.txt"  ECHO "Not Found Input File! narration\1.���̓e�L�X�g_sjis.txt"
IF NOT EXIST "narration\1.���̓e�L�X�g_sjis.txt"  GOTO BYE
ECHO OK

:API
ECHO;
ECHO API(free,google,watson,azure,nict,winos,macos)�I���i���͖�����free�j
SET api=
SET /P api="free,google,watson,azure,nict,winos,macos�F"
IF %api%@==@        SET api=free
IF %api%@==free@    GOTO APIGO
IF %api%@==google@  GOTO APIGO
IF %api%@==watson@  GOTO APIGO
IF %api%@==azure@   GOTO APIGO
IF %api%@==nict@    GOTO APIGO
IF %api%@==winos@   GOTO APIGO
IF %api%@==macos@   GOTO APIGO
GOTO API
:APIGO
ECHO %api%
                    SET apii=free
                    SET apit=free
                    SET apio=winos
IF %api%@==free@    SET apii=free
IF %api%@==free@    SET apit=free
IF %api%@==free@    SET apio=winos
IF %api%@==google@  SET apii=google
IF %api%@==google@  SET apit=google
IF %api%@==google@  SET apio=google
IF %api%@==watson@  SET apii=watson
IF %api%@==watson@  SET apit=watson
IF %api%@==watson@  SET apio=watson
IF %api%@==azure@   SET apii=azure
IF %api%@==azure@   SET apit=azure
IF %api%@==azure@   SET apio=azure
IF %api%@==nict@    SET apii=nict
IF %api%@==nict@    SET apit=nict
IF %api%@==nict@    SET apio=nict
IF %api%@==winos@   SET apii=free
IF %api%@==winos@   SET apit=free
IF %api%@==winos@   SET apio=winos
IF %api%@==macos@   SET apii=free
IF %api%@==macos@   SET apit=free
IF %api%@==macos@   SET apio=macos



IF NOT EXIST "temp"           MKDIR "temp"
IF NOT EXIST "temp\_log"      MKDIR "temp\_log"
IF NOT EXIST "temp\_cache"    MKDIR "temp\_cache"
IF NOT EXIST "narration"      MKDIR "narration"
IF NOT EXIST "narration\tts"  MKDIR "narration\tts"
IF NOT EXIST "narration\mp3"  MKDIR "narration\mp3"
IF NOT EXIST "narration\wav"  MKDIR "narration\wav"



ECHO;
ECHO �t�@�C������

IF EXIST "narration\tts\*.*"  DEL "narration\tts\*.*" /Q
IF EXIST "narration\mp3\*.*"  DEL "narration\mp3\*.*" /Q
IF EXIST "narration\wav\*.*"  DEL "narration\wav\*.*" /Q

ECHO;
ECHO �����f�[�^����

rem --------------------------------
    python _v5_speech__narration1.py
rem --------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

ECHO;
ECHO �����̓N���E�h�ň�C�ɍs���܂��B
ECHO ���������s����܂��Ƀe�L�X�g�� �� �K�� �� �m���߂Ă��������B�inarration/tts�t�H���_�j
PAUSE

ECHO;
ECHO �e�L�X�g�͊m�F���܂����ˁH
ECHO �����̓N���E�h�ň�C�ɍs���܂��B�i�t�@�C�������O�D�T�~�j
PAUSE

taskkill /im sox.exe          /f >dummyKill.txt
taskkill /im adintool.exe     /f >dummyKill.txt
taskkill /im adintool-gui.exe /f >dummyKill.txt
taskkill /im julius.exe       /f >dummyKill.txt
if exist dummyKill.txt        del dummyKill.txt

IF EXIST "temp\*.*"                DEL "temp\*.*"                /Q
IF EXIST "temp\a5_0control\*.*"    DEL "temp\a5_0control\*.*"    /Q
IF EXIST "temp\a5_1voice\*.*"      DEL "temp\a5_1voice\*.*"      /Q
IF EXIST "temp\a5_2wav\*.*"        DEL "temp\a5_2wav\*.*"        /Q
IF EXIST "temp\a5_3stt_julius\*.*" DEL "temp\a5_3stt_julius\*.*" /Q
IF EXIST "temp\a5_4stt_txt\*.*"    DEL "temp\a5_4stt_txt\*.*"    /Q
IF EXIST "temp\a5_5tts_txt\*.*"    DEL "temp\a5_5tts_txt\*.*"    /Q
IF EXIST "temp\a5_6tra_txt\*.*"    DEL "temp\a5_6tra_txt\*.*"    /Q
IF EXIST "temp\a5_7play\*.*"       DEL "temp\a5_7play\*.*"       /Q
IF EXIST "temp\_recorder\*.*"      DEL "temp\_recorder\*.*"      /Q
IF EXIST "temp\_work\*.*"          DEL "temp\_work\*.*"          /Q

IF NOT EXIST "temp\a5_5tts_txt"  MKDIR "temp\a5_5tts_txt"
ECHO XCOPY narration\tts\*.* temp\a5_5tts_txt /Q/R/Y
     XCOPY narration\tts\*.* temp\a5_5tts_txt /Q/R/Y

rem ---------------------------------------------------------------------InpTrn___TxtOut
rem ���{��o��
    python _v5__main_audio.py speech file usb off 0 %apii% %apit% %apio% ja ja,en ja ja
rem �p��o��
rem python _v5__main_audio.py speech file usb off 0 %apii% %apit% %apio% ja en,ja ja en
rem �L���b�V���w�K
rem python _v5__main_audio.py speech file usb off 0 %apii% %apit% %apio% ja en,fr,es,id,zh,ko,ja ja en
rem ------------------------------------------------------------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

IF EXIST "narration\mp3\*.*"      DEL "narration\mp3\*.*" /Q
ECHO XCOPY "temp\_recorder\*.mp3" "narration\mp3" /Q/R/Y
     XCOPY "temp\_recorder\*.mp3" "narration\mp3" /Q/R/Y

rem --------------------------------
    python _v5_speech__narration2.py
rem --------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

ECHO;
ECHO %api% �̏����͏I���B
ECHO ��ƃt�@�C���N���A���܂��B
PAUSE

IF EXIST "temp\*.*"                DEL "temp\*.*"                /Q
IF EXIST "temp\a5_0control\*.*"    DEL "temp\a5_0control\*.*"    /Q
IF EXIST "temp\a5_1voice\*.*"      DEL "temp\a5_1voice\*.*"      /Q
IF EXIST "temp\a5_2wav\*.*"        DEL "temp\a5_2wav\*.*"        /Q
IF EXIST "temp\a5_3stt_julius\*.*" DEL "temp\a5_3stt_julius\*.*" /Q
IF EXIST "temp\a5_4stt_txt\*.*"    DEL "temp\a5_4stt_txt\*.*"    /Q
IF EXIST "temp\a5_5tts_txt\*.*"    DEL "temp\a5_5tts_txt\*.*"    /Q
IF EXIST "temp\a5_6tra_txt\*.*"    DEL "temp\a5_6tra_txt\*.*"    /Q
IF EXIST "temp\a5_7play\*.*"       DEL "temp\a5_7play\*.*"       /Q
IF EXIST "temp\_recorder\*.*"      DEL "temp\_recorder\*.*"      /Q
IF EXIST "temp\_work\*.*"          DEL "temp\_work\*.*"          /Q

:BYE
PAUSE
