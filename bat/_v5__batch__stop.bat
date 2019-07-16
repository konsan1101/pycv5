@ECHO OFF

ECHO terminate
taskkill /im python.exe /f       >nul
taskkill /im adintool-gui.exe /f >nul
taskkill /im adintool.exe /f     >nul
taskkill /im julius.exe /f       >nul

rem PAUSE

exit


