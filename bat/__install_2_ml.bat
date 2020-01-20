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

PAUSE



rem ECHO;
rem ECHO -------
rem ECHO jupyter
rem ECHO -------
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
ECHO ---------
ECHO bluetooth
ECHO ---------
    python -m pip  install --upgrade pybluez



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
ECHO ---------------
ECHO azureml
ECHO ---------------
    python -m pip  install --upgrade pandas
    python -m pip  install --upgrade azureml-sdk
    python -m pip  install --upgrade azureml-dataprep
    python -m pip  install --upgrade azureml-train-automl
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
