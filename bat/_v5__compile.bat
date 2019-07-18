@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

    pyinstaller _v5__main_audio.py  --onefile

    pyinstaller _v5__main_video.py  --onefile

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_audio.exe"   "_v5__main_audio.exe"
    del  "_v5__main_audio.spec"

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_video.exe"   "_v5__main_video.exe"
    del  "_v5__main_video.spec"

rd build /s /q
rd dist /s /q

pause


