@ECHO OFF

c:
cd c:\pycv5

rem python _v5__main.py >nul
    python _v5__main.py

taskkill /im adintool-gui.exe /f >nul
taskkill /im adintool.exe /f     >nul
taskkill /im julius.exe /f       >nul

exit

