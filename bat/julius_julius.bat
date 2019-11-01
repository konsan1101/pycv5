@ECHO OFF
cd "C:\Users\kondou\Documents\GitHub\pycv5"

rem -----------
rem stand alone
rem -----------
rem       julius -input mic     -C julius/_jconf_20180313dnn.jconf -dnnconf julius/julius.dnnconf -charconv utf-8 sjis

rem PAUSE

rem -----------
rem net run
rem -----------
rem start julius -input adinnet -C julius/_jconf_20180311gmm.jconf -charconv utf-8 sjis -logfile temp/temp_julius.log -quiet
rem start julius -input adinnet -C julius/_jconf_20180313dnn.jconf -dnnconf julius/julius.dnnconf -charconv utf-8 sjis -logfile temp/temp_julius.log -quiet

rem start julius -input adinnet -C julius/_jconf_20180311gmm.jconf -charconv utf-8 sjis
    start julius -input adinnet -C julius/_jconf_20180313dnn.jconf -dnnconf julius/julius.dnnconf -charconv utf-8 sjis

ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

    adintool -in mic -out adinnet -server localhost -rewind 555 -headmargin 333 -tailmargin 444 -lv 777

PAUSE

