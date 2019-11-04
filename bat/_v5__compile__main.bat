@echo off
cd ".."

rd build /s /q
rd dist /s /q
pause

set pyname=_v5__main__kernel
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icon/RiKi_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__main_speech
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icon/RiKi_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__main_vision
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icon/cam_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__main_desktop
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icon/rec_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause



