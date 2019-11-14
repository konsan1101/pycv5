@ECHO OFF
rem CALL __setpath.bat

rem brew install lame
rem brew install sox
rem brew install libsox-fmt-all
rem brew install ffmpeg
rem brew install zbar

rem brew install libopencv-dev
rem brew install python-opencv

rem brew cask install chromedriver
rem brew install geckodriver

PAUSE

ECHO;
ECHO -----
ECHO tools
ECHO -----
rem           pip  install --upgrade pip
    python -m pip  install --upgrade pip
    python -m pip  install --upgrade setuptools
    python -m pip  install --upgrade pyinstaller

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO -------------
ECHO communication
ECHO -------------
    python -m pip  install --upgrade requests
    python -m pip  install --upgrade requests_toolbelt
    python -m pip  install --upgrade uuid
    python -m pip  install --upgrade bs4
    python -m pip  install --upgrade pyopenssl
    python -m pip  install --upgrade grpcio
    python -m pip  install --upgrade grpcio-tools
    python -m pip  install --upgrade feedparser
    python -m pip  install --upgrade selenium

ECHO;
ECHO -----
ECHO audio
ECHO -----
rem python -m pip  install --upgrade pyaudio
    python -m pip  install --upgrade wave
    python -m pip  install --upgrade sounddevice
    python -m pip  install --upgrade speechrecognition

ECHO;
ECHO ------
ECHO vision
ECHO ------
rem python -m pip  install --upgrade pygame
rem python -m pip  install --upgrade pyqtgraph
rem python -m pip  install --upgrade pyqt5
    python -m pip  install --upgrade pillow
    python -m pip  install --upgrade numpy
    python -m pip  install --upgrade opencv-python
rem python -m pip  install --upgrade pyflakes
rem python -m pip  install --upgrade pylint
rem python -m pip  install --upgrade pep8
    python -m pip  install --upgrade matplotlib
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pyzbar

ECHO;
ECHO -----------
ECHO yolo3 keras
ECHO -----------
rem    python -m pip  install --upgrade tensorflow
rem    python -m pip  install --upgrade keras

ECHO;
ECHO -------------
ECHO yolo3 pytorch
ECHO -------------
rem python -m pip  install --upgrade torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
rem python -m pip  install --upgrade torchvision
rem python -m pip  install --upgrade pandas

ECHO;
ECHO ------------
ECHO deep larning
ECHO ------------
    python -m pip  install --upgrade gym
    python -m pip  install --upgrade atari-py
    python -m pip  install --upgrade scikit-image
    python -m pip  install --upgrade scikit-learn



ECHO;
ECHO ----------
ECHO IBM Watson
ECHO ----------
rem python -m pip  install --upgrade watson-developer-cloud==1.0.2
rem python -m pip  install --upgrade watson-developer-cloud
    python -m pip  install --upgrade ibm-watson
    python -m pip  install --upgrade ibm_cloud_sdk_core

ECHO;
ECHO ---------------
ECHO microsoft,azure
ECHO ---------------
rem python -m pip  install --upgrade mstranslator
    python -m pip  install --upgrade cognitive_face
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade azure-storage

ECHO;
ECHO ---------------
ECHO azureml
ECHO ---------------
    python -m pip  install --upgrade azureml-sdk
    python -m pip  install --upgrade azureml-dataprep

ECHO;
ECHO ------
ECHO google
ECHO ------
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



PAUSE



