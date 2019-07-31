@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

    pyinstaller _v5__main_speech.py  --onefile

    pyinstaller _v5__main_vision.py  --onefile

    pyinstaller _v5__main_desktop.py --onefile

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_speech.exe"   "_v5__main_speech.exe"
    del  "_v5__main_speech.spec"

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_vision.exe"   "_v5__main_vision.exe"
    del  "_v5__main_vision.spec"

    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_desktop.exe"  "_v5__main_desktop.exe"
    del  "_v5__main_desktop.spec"

rd build /s /q
rd dist /s /q

pause



