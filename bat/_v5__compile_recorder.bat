@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

set pyname=_v5_proc_recorder
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_proc_uploader
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q

pause



