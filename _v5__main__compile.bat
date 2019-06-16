@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

    pyinstaller _v5__main_camera.py --onefile
    pyinstaller _v5__main_audio.py  --onefile
rem pyinstaller _v5__main_video.py  --onefile

pause

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_camera.exe"  "_v5__main_camera.exe"
    del  "_v5__main_camera.spec"

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_audio.exe"   "_v5__main_audio.exe"
    del  "_v5__main_audio.spec"

rem copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_video.exe"   "_v5__main_video.exe"
rem del  "_v5__main_video.spec"

pause


