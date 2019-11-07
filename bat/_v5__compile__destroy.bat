@echo off
cd ".."

rd build /s /q
rd dist /s /q
pause

set pyname=_v5__destroy
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile --icon="_icons/RiKi_stop.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause



