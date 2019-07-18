@echo off

rem ffmpeg -list_devices true -f dshow -i dummy
rem ffmpeg -f dshow -i video="UScreenCapture":audio="virtual-audio-capturer" -r 5 output.mp4

rem ffmpeg -list_devices true -f gdigrab -i desktop
rem ffmpeg -f gdigrab -i desktop -r 5 output.mp4



set ext=mp4

if exist "desktop.%ext%"  del "desktop.%ext%"

rem start "" /b ffmpeg -f gdigrab -i desktop -r 5 "desktop.%ext%"
                ffmpeg -f gdigrab -i desktop -r 5 "desktop.%ext%"

rem ping localhost -w 1000 -n 60 >nul

rem taskkill /im ffmpeg.exe /f /t


