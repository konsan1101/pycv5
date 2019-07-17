@echo off

start "rec" vlc screen:// :screen-fps=5 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=flv,dst=test.flv} --qt-start-minimized

ping localhost -w 1000 -n 30 >nul

taskkill /im vlc.exe

PAUSE


