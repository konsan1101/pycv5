@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

rd build /s /q
rd dist /s /q
pause

set pyname=_v5__destroy
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause



