@echo off

rem start "rec" vlc screen:// :screen-fps=5 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=mp4,dst=test.mp4}
rem start "rec" vlc screen:// :screen-fps=5 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=mkv,dst=test.mkv}
    start "rec" vlc screen:// :screen-fps=5 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=flv,dst=test.flv}

ping localhost -w 1000 -n 20 >nul

TASKKILL /IM VLC.EXE

PAUSE


