@ECHO OFF

rem python
    SET PATH=%PATH%;C:\Python36;
rem SET PATH=%PATH%;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_86;

rem sox
rem SET PATH=%PATH%;C:\Program Files\sox-14-4-0;
    SET PATH=%PATH%;C:\Program Files (x86)\sox-14-4-0;
    SET AUDIODRIVER=waveaudio

rem julius
    SET PATH=%PATH%;C:\julius\win;

rem ffmpeg
    SET PATH=%PATH%;C:\ffmpeg\win\bin;

rem vlan
rem SET PATH=%PATH%;C:\Program Files\VideoLAN\VLC;
    SET PATH=%PATH%;C:\Program Files (x86)\VideoLAN\VLC;

C:
rem CD C:\pycv5
    CD C:\Users\kondou\Documents\GitHub\pycv5

IF NOT EXIST temp       MKDIR temp
IF NOT EXIST temp\_log  MKDIR temp\_log

