@ECHO OFF
rem CALL __setpath.bat

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

rem  --------
     PAUSE
rem  --------



ECHO;
ECHO -------
ECHO etc
ECHO -------
rem python -m pip  install --upgrade pyaudio
rem python -m pip  install --upgrade grpcio
rem python -m pip  install --upgrade grpcio-tools
rem python -m pip  install --upgrade pygame
rem python -m pip  install --upgrade matplotlib
rem python -m pip  install --upgrade pyflakes
rem python -m pip  install --upgrade pep8

    python -m pip  install --upgrade matplotlib==3.0.3
    python -m pip  install --upgrade seaborn
    python -m pip  install --upgrade pylint

ECHO;
ECHO -------
ECHO jupyter
ECHO -------
    python -m pip  install --upgrade jupyter
rem python -m jupyter notebook --generate-config
rem c.NotebookApp.notebook_dir = 'C:/Users/kondou/notebook'
rem c.NotebookApp.open_browser = True

rem python -m jupyter notebook

ECHO;
ECHO -------------
ECHO DB
ECHO -------------
    python -m pip  install --upgrade pyodbc
    python -m pip  install --upgrade jaconv

ECHO;
ECHO ----------------------
ECHO bluetooth, nfc(felica)
ECHO ----------------------
    python -m pip  install --upgrade pybluez
    python -m pip  install --upgrade nfcpy

ECHO;
ECHO -------------
ECHO deep learning
ECHO -------------
    python -m pip  install --upgrade gym
    python -m pip  install --upgrade atari-py
    python -m pip  install --upgrade scikit-image
    python -m pip  install --upgrade scikit-learn

rem ECHO;
rem ECHO -----------
rem ECHO yolo3 keras
rem ECHO -----------
rem    python -m pip  install --upgrade tensorflow
rem    python -m pip  install --upgrade keras

rem ECHO;
rem ECHO -------------
rem ECHO yolo3 pytorch
rem ECHO -------------
rem python -m pip  install --upgrade torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
rem python -m pip  install --upgrade torchvision
rem python -m pip  install --upgrade pandas

ECHO;
ECHO ---------------
ECHO azureml
ECHO ---------------
    python -m pip  install --upgrade pandas
    python -m pip  install --upgrade azureml-sdk
    python -m pip  install --upgrade azureml-dataprep
    python -m pip  install --upgrade azureml-train-automl
    python -m pip  install --upgrade azureml.widgets
    python -m pip  install --ignore-installed azureml-train-automl-client
    python -m pip  install --upgrade scipy



rem  --------
     PAUSE
rem  --------



ECHO;
ECHO --------
ECHO pip list
ECHO --------
    python -m pip  list



rem  --------
     PAUSE
rem  --------
