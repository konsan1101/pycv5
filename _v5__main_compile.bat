@echo off
cd C:\Users\kondou\Documents\GitHub\pycv5

pyinstaller _v5__main_video.py --onefile

pause

copy C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_video.exe _v5__main_video.exe

pause
