@ECHO OFF

ECHO;
ECHO python _v5__destroy.py
     python _v5__destroy.py

ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO python _v5__main__handsfree.py
     python _v5__main__handsfree.py

ECHO;
ECHO python _v5__destroy.py
     python _v5__destroy.py

ping localhost -w 1000 -n 5 >nul

EXIT


