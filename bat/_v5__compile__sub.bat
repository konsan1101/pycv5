@echo off
cd ".."

rd build /s /q
rd dist /s /q
pause

set pyname=_v5__sub_bgm
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__sub_browser
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__sub_player
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__sub_chatting
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5__sub_knowledge
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause



