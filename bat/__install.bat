@ECHO OFF
rem CALL __setpath.bat

rem brew install lame
rem brew install sox
rem brew install libsox-fmt-all

rem brew install libopencv-dev
rem brew install python-opencv


PAUSE

ECHO;
ECHO ツール
rem       pip  install --upgrade pip
python -m pip  install --upgrade pip
python -m pip  install --upgrade setuptools

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >>dummyPing.txt
if exist dummyPing.txt    del dummyPing.txt

ECHO;
ECHO 通信
python -m pip  install --upgrade requests
python -m pip  install --upgrade requests_toolbelt
python -m pip  install --upgrade uuid
python -m pip  install --upgrade bs4
python -m pip  install --upgrade pyopenssl
python -m pip  install --upgrade grpcio
python -m pip  install --upgrade grpcio-tools
python -m pip  install --upgrade feedparser

ECHO;
ECHO 画像
python -m pip  install --upgrade pygame
python -m pip  install --upgrade pyqtgraph
python -m pip  install --upgrade pyqt5
python -m pip  install --upgrade pillow
python -m pip  install --upgrade numpy
python -m pip  install --upgrade opencv-python
python -m pip  install --upgrade pyflakes
python -m pip  install --upgrade pylint
python -m pip  install --upgrade pep8
python -m pip  install --upgrade matplotlib

ECHO;
ECHO 音声
python -m pip  install --upgrade pyaudio
python -m pip  install --upgrade wave
python -m pip  install --upgrade sounddevice
python -m pip  install --upgrade speechrecognition

ECHO;
ECHO マイクロソフト
python -m pip  install --upgrade mstranslator
python -m pip  install --upgrade cognitive_face
python -m pip  install --upgrade pywin32

ECHO;
ECHO グーグル
python -m pip  install --upgrade google-cloud-core
python -m pip  install --upgrade google-cloud-speech
python -m pip  install --upgrade google-cloud-translate
python -m pip  install --upgrade google-cloud-vision
python -m pip  install --upgrade google-api-python-client
python -m pip  install --upgrade gtts
python -m pip  install --upgrade googletrans
python -m pip  install --upgrade goslate
python -m pip  install --upgrade ggtrans
python -m pip  uninstall gtts-token
python -m pip  install --upgrade gtts-token

ECHO;
ECHO IBM Watson
rem pip  install --upgrade watson-developer-cloud==1.0.2
rem python -m pip  install --upgrade watson-developer-cloud
python -m pip  install --upgrade ibm-watson

ECHO;
ECHO yolo keras
python -m pip  install --upgrade keras
python -m pip  install --upgrade tensorflow

ECHO;
ECHO yolo pytorch
python -m pip  install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-win_amd64.whl
python -m pip  install pandas


PAUSE



