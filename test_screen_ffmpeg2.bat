@echo off

rem ====================draw_mouse====================
set /p draw_mouse=マウスポインタ[0:描画しない、1:描画する]:

rem ====================映像入力====================
set /p ask_input_video=映像入力[Enter:全画面、tl:左上、bl:左下、tr:右上、br:右下、m:マニュアル領域、w:ウィンドウ領域]:
if "%ask_input_video%" == "tl" (
    set "input_video=-video_size 960x540 -offset_x 0 -offset_y 0 -i desktop"
) else if "%ask_input_video%" == "bl" (
    set "input_video=-video_size 960x540 -offset_x 0 -offset_y 540 -i desktop"
) else if "%ask_input_video%" == "tr" (
    set "input_video=-video_size 960x540 -offset_x 960 -offset_y 0 -i desktop"
) else if "%ask_input_video%" == "br" (
    set "input_video=-video_size 960x540 -offset_x 960 -offset_y 540 -i desktop"
) else if "%ask_input_video%" == "m" (
    echo 例:-video_size 960x540 -offset_x 961 -offset_y 541 -i desktop
    set /p input_video=[サイズ、オフセットオフセット、入力]:
) else if "%ask_input_video%" == "w" (
    echo 例:-i chrome.exe
    set /p input_video=[ウィンドウのタイトル]:
) else if "%ask_input_video%" == "" (
    set "input_video=-i desktop"
)
echo %input_video%

rem ====================音声入力====================
set /p ask_input_audio=音声入力[Enter:音声なし、a:AG03]:
if "%ask_input_audio%" == "a" (
    set "input_audio=-f dshow -i audio^=^"ライン ^(AG06^/AG03^)^" -c:a aac -b:a 320k -ar 44100"
) else if "%ask_input_audio%" == "" (
    set "input_audio=-an"
)
echo %input_audio%

rem ====================vf====================
set /p ask_vf=リサイズ[Enter:しない、解像度:する]:
if "%ask_vf%" == "" (
    set vf=
) else (
    set "vf=-vf scale^=%ask_vf%"
)

rem ====================quality====================
set /p quality=品質[int、Enter:27]:
if not defined quality (
    set quality=27
)

rem ====================ファイル名の日付時刻====================
rem yyMMdd_Hmm
rem 自分用(17/08/30 (水) 17:35->170830_1735)
set mydate=%date:~0,2%%date:~3,2%%date:~6,2%_%time:~0,2%%time:~3,2%
rem 初期設定(2017/08/30 17:35 -> 170830_1735)
rem set mydate=%date:~2,2%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
rem スペースを0に置き換える
set mydate=%mydate: =0%

rem ====================エンコ====================
rem 録画開始するか聞く
set /p hoge=録画を開始するには何かキーを押してください . . .
rem 別プロセスで最小化でffmpegを起動する
:encode
timeout /t 1
start /high /min ffmpeg -y -hide_banner -fflags +discardcorrupt -f gdigrab -r 30000/1001 -draw_mouse %draw_mouse% -show_region 1 %input_video% %input_audio% %vf% -global_quality %quality% -c:v h264_qsv -preset slow -g 15 -bf 2 -refs 4 -b_strategy 1 -look_ahead 1 -pix_fmt nv12 -movflags +faststart "C:\Users\Shibanyan\Desktop\ffrec_%mydate%.mp4"
rem 終了コード1の場合ループ
if %errorlevel% equ 1 (
    goto :encode
)
exit


