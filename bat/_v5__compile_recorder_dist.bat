@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

rd "build" /s /q
rd "dist" /s /q
mkdir dist
mkdir dist\bin
pause

set pyname=_v5_proc_recorder
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py
    xcopy "dist\%pyname%\*.*" "dist\bin" /E /V /H /Y
    rd  "build\%pyname%" /s /q
    rd  "dist\%pyname%"  /s /q
    del "%pyname%.spec"

set pyname=_v5_proc_uploader
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py
    xcopy "dist\%pyname%\*.*" "dist\bin" /E /V /H /Y
    rd  "build\%pyname%" /s /q
    rd  "dist\%pyname%"  /s /q
    del "%pyname%.spec"

rd "build" /s /q
pause


