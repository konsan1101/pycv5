@ECHO OFF
CALL __setpath.bat

ECHO;
ECHO ���̓t�@�C�����݊m�F
IF NOT EXIST "gijiroku\1.���͉���.mp3"  ECHO "Not Found Input File! gijiroku\1.���͉���.mp3"
IF NOT EXIST "gijiroku\1.���͉���.mp3"  GOTO BYE
ECHO OK

:API
ECHO;
ECHO API(free,google,watson,azure,nict,docomo)�I���i���͖�����free�j
SET api=
SET /P api="free,google,watson,azure,nict,docomo�F"
IF %api%@==@        SET api=free
IF %api%@==free@    GOTO APIGO
IF %api%@==google@  GOTO APIGO
IF %api%@==watson@  GOTO APIGO
IF %api%@==azure@   GOTO APIGO
IF %api%@==nict@    GOTO APIGO
IF %api%@==docomo@  GOTO APIGO
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
IF %api%@==docomo@  SET apii=docomo
IF %api%@==docomo@  SET apit=free
IF %api%@==docomo@  SET apio=winos



IF NOT EXIST "temp"                     MKDIR "temp"
IF NOT EXIST "temp\_log"                MKDIR "temp\_log"
IF NOT EXIST "temp\_cache"              MKDIR "temp\_cache"
IF NOT EXIST "gijiroku"                 MKDIR "gijiroku"
IF NOT EXIST "gijiroku\wav"             MKDIR "gijiroku\wav"
IF NOT EXIST "gijiroku\mp3"             MKDIR "gijiroku\mp3"
IF NOT EXIST "gijiroku\stt"             MKDIR "gijiroku\stt"
IF NOT EXIST "gijiroku\temp"            MKDIR "gijiroku\temp"
IF NOT EXIST "gijiroku\temp\wav_0n"     MKDIR "gijiroku\temp\wav_0n"
IF NOT EXIST "gijiroku\temp\wav_1eq3"   MKDIR "gijiroku\temp\wav_1eq3"
IF NOT EXIST "gijiroku\temp\wav_1eq6"   MKDIR "gijiroku\temp\wav_1eq6"
IF NOT EXIST "gijiroku\temp\wav_1eq9"   MKDIR "gijiroku\temp\wav_1eq9"
IF NOT EXIST "gijiroku\temp\wav_2nv"    MKDIR "gijiroku\temp\wav_2nv"
IF NOT EXIST "gijiroku\temp\wav_3eq3v"  MKDIR "gijiroku\temp\wav_3eq3v"
IF NOT EXIST "gijiroku\temp\wav_3eq6v"  MKDIR "gijiroku\temp\wav_3eq6v"
IF NOT EXIST "gijiroku\temp\wav_3eq9v"  MKDIR "gijiroku\temp\wav_3eq9v"



ECHO;
ECHO ���ʉ��������i1=mp3�c���^,2=ϲ����͋c���^,���͖����͍ĕϊ��j
SET volume=
SET /P volume="���͖����̓X�L�b�v�F"
IF %volume%@==1@  GOTO CPY
IF %volume%@==2@  GOTO REAL
IF %volume%@==@   GOTO SKIP
rem IF %volume%@==@   GOTO SEP
GOTO RERUN

:REAL

ECHO;
ECHO �t�@�C������

IF EXIST "gijiroku\temp\temp__giji*.*"  DEL "gijiroku\temp\temp__giji*.*" /Q
IF EXIST "gijiroku\wav\*.*"             DEL "gijiroku\wav\*.*"            /Q
IF EXIST "gijiroku\mp3\*.*"             DEL "gijiroku\mp3\*.*"            /Q
IF EXIST "gijiroku\temp\wav_0n\*.*"     DEL "gijiroku\temp\wav_0n\*.*"    /Q
IF EXIST "gijiroku\temp\wav_1eq3\*.*"   DEL "gijiroku\temp\wav_1eq3\*.*"  /Q
IF EXIST "gijiroku\temp\wav_1eq6\*.*"   DEL "gijiroku\temp\wav_1eq6\*.*"  /Q
IF EXIST "gijiroku\temp\wav_1eq9\*.*"   DEL "gijiroku\temp\wav_1eq9\*.*"  /Q
IF EXIST "gijiroku\temp\wav_2nv\*.*"    DEL "gijiroku\temp\wav_2nv\*.*"   /Q
IF EXIST "gijiroku\temp\wav_3eq3v\*.*"  DEL "gijiroku\temp\wav_3eq3v\*.*" /Q
IF EXIST "gijiroku\temp\wav_3eq6v\*.*"  DEL "gijiroku\temp\wav_3eq6v\*.*" /Q
IF EXIST "gijiroku\temp\wav_3eq9v\*.*"  DEL "gijiroku\temp\wav_3eq9v\*.*" /Q
GOTO SKIP

:CPY

ECHO;
ECHO ���ʉ��������imp3��wav�j

IF EXIST "gijiroku\temp\temp__giji*.*"  DEL "gijiroku\temp\temp__giji*.*" /Q

ECHO sox "gijiroku/1.���͉���.mp3" -r 16000 -b 16 -c 1 "gijiroku/temp/temp__gijiroku16_0n.wav"
     sox "gijiroku/1.���͉���.mp3" -r 16000 -b 16 -c 1 "gijiroku/temp/temp__gijiroku16_0n.wav"

ECHO sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_hilo.wav" highpass 50
     sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_hilo.wav" highpass 50

ECHO sox "gijiroku/temp/temp__gijiroku16_hilo.wav" "gijiroku/temp/temp__gijiroku16_2nv.wav" --norm
     sox "gijiroku/temp/temp__gijiroku16_hilo.wav" "gijiroku/temp/temp__gijiroku16_2nv.wav" --norm

ECHO sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq3a.wav" equalizer 500 1.0q 2
     sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq3a.wav" equalizer 500 1.0q 2
ECHO sox "gijiroku/temp/temp__gijiroku16_eq3a.wav" "gijiroku/temp/temp__gijiroku16_eq3b.wav" equalizer 400 1.0q 2
     sox "gijiroku/temp/temp__gijiroku16_eq3a.wav" "gijiroku/temp/temp__gijiroku16_eq3b.wav" equalizer 400 1.0q 2
ECHO sox "gijiroku/temp/temp__gijiroku16_eq3b.wav" "gijiroku/temp/temp__gijiroku16_eq3c.wav" equalizer 600 1.0q 2
     sox "gijiroku/temp/temp__gijiroku16_eq3b.wav" "gijiroku/temp/temp__gijiroku16_eq3c.wav" equalizer 600 1.0q 2
ECHO sox "gijiroku/temp/temp__gijiroku16_eq3c.wav" "gijiroku/temp/temp__gijiroku16_1eq3.wav" highpass 50
     sox "gijiroku/temp/temp__gijiroku16_eq3c.wav" "gijiroku/temp/temp__gijiroku16_1eq3.wav" highpass 50

ECHO sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq6a.wav" equalizer 500 1.0q 4
     sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq6a.wav" equalizer 500 1.0q 4
ECHO sox "gijiroku/temp/temp__gijiroku16_eq6a.wav" "gijiroku/temp/temp__gijiroku16_eq6b.wav" equalizer 400 1.0q 4
     sox "gijiroku/temp/temp__gijiroku16_eq6a.wav" "gijiroku/temp/temp__gijiroku16_eq6b.wav" equalizer 400 1.0q 4
ECHO sox "gijiroku/temp/temp__gijiroku16_eq6b.wav" "gijiroku/temp/temp__gijiroku16_eq6c.wav" equalizer 600 1.0q 4
     sox "gijiroku/temp/temp__gijiroku16_eq6b.wav" "gijiroku/temp/temp__gijiroku16_eq6c.wav" equalizer 600 1.0q 4
ECHO sox "gijiroku/temp/temp__gijiroku16_eq6c.wav" "gijiroku/temp/temp__gijiroku16_1eq6.wav" highpass 50
     sox "gijiroku/temp/temp__gijiroku16_eq6c.wav" "gijiroku/temp/temp__gijiroku16_1eq6.wav" highpass 50

ECHO sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq9a.wav" equalizer 500 1.0q 6
     sox "gijiroku/temp/temp__gijiroku16_0n.wav"   "gijiroku/temp/temp__gijiroku16_eq9a.wav" equalizer 500 1.0q 6
ECHO sox "gijiroku/temp/temp__gijiroku16_eq9a.wav" "gijiroku/temp/temp__gijiroku16_eq9b.wav" equalizer 400 1.0q 6
     sox "gijiroku/temp/temp__gijiroku16_eq9a.wav" "gijiroku/temp/temp__gijiroku16_eq9b.wav" equalizer 400 1.0q 6
ECHO sox "gijiroku/temp/temp__gijiroku16_eq9b.wav" "gijiroku/temp/temp__gijiroku16_eq9c.wav" equalizer 600 1.0q 6
     sox "gijiroku/temp/temp__gijiroku16_eq9b.wav" "gijiroku/temp/temp__gijiroku16_eq9c.wav" equalizer 600 1.0q 6
ECHO sox "gijiroku/temp/temp__gijiroku16_eq9c.wav" "gijiroku/temp/temp__gijiroku16_1eq9.wav" highpass 50
     sox "gijiroku/temp/temp__gijiroku16_eq9c.wav" "gijiroku/temp/temp__gijiroku16_1eq9.wav" highpass 50

ECHO sox "gijiroku/temp/temp__gijiroku16_1eq3.wav" "gijiroku/temp/temp__gijiroku16_3eq3v.wav" --norm
     sox "gijiroku/temp/temp__gijiroku16_1eq3.wav" "gijiroku/temp/temp__gijiroku16_3eq3v.wav" --norm
ECHO sox "gijiroku/temp/temp__gijiroku16_1eq6.wav" "gijiroku/temp/temp__gijiroku16_3eq6v.wav" --norm
     sox "gijiroku/temp/temp__gijiroku16_1eq6.wav" "gijiroku/temp/temp__gijiroku16_3eq6v.wav" --norm
ECHO sox "gijiroku/temp/temp__gijiroku16_1eq9.wav" "gijiroku/temp/temp__gijiroku16_3eq9v.wav" --norm
     sox "gijiroku/temp/temp__gijiroku16_1eq9.wav" "gijiroku/temp/temp__gijiroku16_3eq9v.wav" --norm

:SEP

ECHO;
ECHO �œK�l�������f�iwav��list�j

set rewd=555
set head=333
set tail=444
set lv=1111

IF EXIST "gijiroku\temp\wav_0n\*.*"     DEL "gijiroku\temp\wav_0n\*.*"    /Q
IF EXIST "gijiroku\temp\wav_1eq3\*.*"   DEL "gijiroku\temp\wav_1eq3\*.*"  /Q
IF EXIST "gijiroku\temp\wav_1eq6\*.*"   DEL "gijiroku\temp\wav_1eq6\*.*"  /Q
IF EXIST "gijiroku\temp\wav_1eq9\*.*"   DEL "gijiroku\temp\wav_1eq9\*.*"  /Q
IF EXIST "gijiroku\temp\wav_2nv\*.*"    DEL "gijiroku\temp\wav_2nv\*.*"   /Q
IF EXIST "gijiroku\temp\wav_3eq3v\*.*"  DEL "gijiroku\temp\wav_3eq3v\*.*" /Q
IF EXIST "gijiroku\temp\wav_3eq6v\*.*"  DEL "gijiroku\temp\wav_3eq6v\*.*" /Q
IF EXIST "gijiroku\temp\wav_3eq9v\*.*"  DEL "gijiroku\temp\wav_3eq9v\*.*" /Q

SET fn=0n
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=1eq3
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=1eq6
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=1eq9
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=2nv
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=3eq3v
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=3eq6v
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

SET fn=3eq9v
ECHO gijiroku/temp/temp__gijiroku16_%fn%.wav>gijiroku\temp\temp__filelist16.txt
ECHO adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt
     adintool -in file -filelist gijiroku/temp/temp__filelist16.txt -out file -filename gijiroku/temp/wav_%fn%/julius -startid 1 -rewind %rewd% -headmargin %head% -tailmargin %tail% -lv %lv% -zmean >gijiroku/temp/temp__gijilist16_%fn%.txt

:SKIP

ECHO;
ECHO �����f�[�^����

IF EXIST "gijiroku\wav\*.*"                    DEL "gijiroku\wav\*.*"                   /Q
IF EXIST "gijiroku\mp3\*.*"                    DEL "gijiroku\mp3\*.*"                   /Q
IF EXIST "gijiroku\temp\temp__gijiroku16.wav"  DEL "gijiroku\temp\temp__gijiroku16.wav" /Q
IF EXIST "gijiroku\temp\temp__gijiroku16.mp3"  DEL "gijiroku\temp\temp__gijiroku16.mp3" /Q
IF EXIST "gijiroku\temp\temp__gijilist16.txt"  DEL "gijiroku\temp\temp__gijilist16.txt" /Q

rem -------------------------------
    python _v5_speech__gijiroku1.py
rem -------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

IF NOT EXIST "gijiroku\temp\temp__gijilist16.txt"  ECHO "Not Found Input File! gijiroku\temp\temp__gijilist16.txt"
IF NOT EXIST "gijiroku\temp\temp__gijilist16.txt"  GOTO API

ECHO COPY "gijiroku\temp\temp__gijilist16.txt" "gijiroku\2.wav�ϊ����O.txt"
     COPY "gijiroku\temp\temp__gijilist16.txt" "gijiroku\2.wav�ϊ����O.txt"

ECHO;
ECHO �����̓N���E�h�ň�C�ɍs���܂��B
ECHO ���������s����܂��ɉ��ʂ� �� �K�� �� �m���߂Ă��������B�igijiroku/wav�t�H���_�j
PAUSE

ECHO;
ECHO ���ʂ͊m�F���܂����ˁH
ECHO �����̓N���E�h�ň�C�ɍs���܂��B�i�t�@�C�������O�D�T�~�j
PAUSE

:GO
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

IF NOT EXIST "temp\a5_1voice"  MKDIR "temp\a5_1voice"
ECHO XCOPY gijiroku\wav temp\a5_1voice /Q/R/Y
     XCOPY gijiroku\wav temp\a5_1voice /Q/R/Y

rem ---------------------------------------------------------------------InpTrn
    python _v5__main_audio.py speech file usb off 0 %apii% %apit% %apio% ja ja
rem ---------------------------------------------------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

IF EXIST "gijiroku\stt\*.*"           DEL "gijiroku\stt\*.*" /Q
IF EXIST "gijiroku\mp3\*.*"           DEL "gijiroku\mp3\*.*" /Q
ECHO XCOPY "temp\_recorder\*.txt" "gijiroku\stt" /Q/R/Y
     XCOPY "temp\_recorder\*.txt" "gijiroku\stt" /Q/R/Y
ECHO XCOPY "temp\_recorder\*.mp3" "gijiroku\mp3" /Q/R/Y
     XCOPY "temp\_recorder\*.mp3" "gijiroku\mp3" /Q/R/Y

rem -------------------------------
    python _v5_speech__gijiroku2.py
rem -------------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummyPing.txt
rem if exist dummyPing.txt    del dummyPing.txt

ECHO sox "gijiroku/temp/temp__gijiroku16.wav" "gijiroku/temp/temp__gijiroku16.mp3"
     sox "gijiroku/temp/temp__gijiroku16.wav" "gijiroku/temp/temp__gijiroku16.mp3"

ECHO;
ECHO %api% �̏����͏I�����܂����B
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
