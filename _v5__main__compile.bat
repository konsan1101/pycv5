@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

pyinstaller _v5__main_camera.py --onefile
pyinstaller _v5__main_audio.py  --onefile

pause

del  "_v5__main_camera.spec"
del  "_v5__main_audio.spec"
copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_camera.exe"  "_v5__main_camera.exe"
copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_audio.exe"   "_v5__main_audio.exe"

pause


