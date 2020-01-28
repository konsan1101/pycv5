@echo off
cd ".."

rd build /s /q
rd dist /s /q
pause

set pyname=_v5__main_speech
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icons/speech_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_speech__gijiroku1
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icons/speech_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_speech__gijiroku2
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icons/speech_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_speech__narration1
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icons/speech_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_speech__narration2
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile  --icon="_icons/speech_start.ico"
    copy "dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause



