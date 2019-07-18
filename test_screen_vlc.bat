@echo off

set ext=mp4

if exist "desktop.%ext%"  del "desktop.%ext%"

start "" /b vlc screen:// :screen-fps=5 :live-caching=300 --sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=%ext%,dst="desktop.%ext%"} --qt-start-minimized

ping localhost -w 1000 -n 30 >nul

vlc vlc://quit

ping localhost -w 1000 -n 5 >nul

taskkill /im vlc.exe /f


