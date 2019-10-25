@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

rd build /s /q
rd dist /s /q
pause

echo ;
echo check hook file!
echo pyinstaller/hooks/hook-google.cloud.speech.py
echo pyinstaller/hooks/hook-grpc.py
pause

set pyname=speech_api_google
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=vision_api_google
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause

echo;
echo speech_api_google.exe
     speech_api_google.exe
pause

echo;
echo vision_api_google.exe
     vision_api_google.exe
pause
