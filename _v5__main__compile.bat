@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

pyinstaller _v5__main_camera.py --onefile

pause

del  "_v5__main_camera.spec"
copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\_v5__main_camera.exe"  "_v5__main_camera.exe"

pause


