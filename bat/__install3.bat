@ECHO OFF
CALL __setpath.bat

rem brew install lame
rem brew install sox

PAUSE

ECHO;
ECHO �c�[��
rem        pip  install --upgrade pip
python3 -m pip  install --upgrade pip --user
python3 -m pip  install --upgrade setuptools --user

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >>dummyPing.txt
if exist dummyPing.txt    del dummyPing.txt

ECHO;
ECHO �ʐM
python3 -m pip  install --upgrade requests --user
python3 -m pip  install --upgrade requests_toolbelt --user
python3 -m pip  install --upgrade uuid --user
python3 -m pip  install --upgrade bs4 --user
python3 -m pip  install --upgrade pyopenssl --user
python3 -m pip  install --upgrade grpcio --user
python3 -m pip  install --upgrade grpcio-tools --user
python3 -m pip  install --upgrade feedparser --user

ECHO;
ECHO �摜
python3 -m pip  install --upgrade pygame --user
python3 -m pip  install --upgrade pyqtgraph --user
python3 -m pip  install --upgrade pyqt5 --user
python3 -m pip  install --upgrade pillow --user
python3 -m pip  install --upgrade numpy --user
python3 -m pip  install --upgrade opencv-python --user
python3 -m pip  install --upgrade pyflakes --user
python3 -m pip  install --upgrade pylint --user
python3 -m pip  install --upgrade pep8 --user

ECHO;
ECHO ����
python3 -m pip  install --upgrade pyaudio --user
python3 -m pip  install --upgrade wave --user
python3 -m pip  install --upgrade sounddevice --user
python3 -m pip  install --upgrade speechrecognition --user

ECHO;
ECHO �}�C�N���\�t�g
python3 -m pip  install --upgrade mstranslator --user
python3 -m pip  install --upgrade cognitive_face --user
python3 -m pip  install --upgrade pywin32 --user

ECHO;
ECHO �O�[�O��
python3 -m pip  install --upgrade google-cloud-speech --user
python3 -m pip  install --upgrade google-cloud-translate --user
python3 -m pip  install --upgrade google-cloud-vision --user
python3 -m pip  install --upgrade google-api-python-client --user
python3 -m pip  install --upgrade gtts --user
python3 -m pip  install --upgrade googletrans --user
python3 -m pip  install --upgrade goslate --user
python3 -m pip  install --upgrade ggtrans --user
python3 -m pip  uninstall gtts-token --user
python3 -m pip  install --upgrade gtts-token --user

ECHO;
ECHO IBM Watson
rem pip  install --upgrade watson-developer-cloud==1.0.2
python3 -m pip  install --upgrade watson-developer-cloud --user



PAUSE



