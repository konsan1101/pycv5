@echo off

rem ====================draw_mouse====================
set /p draw_mouse=�}�E�X�|�C���^[0:�`�悵�Ȃ��A1:�`�悷��]:

rem ====================�f������====================
set /p ask_input_video=�f������[Enter:�S��ʁAtl:����Abl:�����Atr:�E��Abr:�E���Am:�}�j���A���̈�Aw:�E�B���h�E�̈�]:
if "%ask_input_video%" == "tl" (
    set "input_video=-video_size 960x540 -offset_x 0 -offset_y 0 -i desktop"
) else if "%ask_input_video%" == "bl" (
    set "input_video=-video_size 960x540 -offset_x 0 -offset_y 540 -i desktop"
) else if "%ask_input_video%" == "tr" (
    set "input_video=-video_size 960x540 -offset_x 960 -offset_y 0 -i desktop"
) else if "%ask_input_video%" == "br" (
    set "input_video=-video_size 960x540 -offset_x 960 -offset_y 540 -i desktop"
) else if "%ask_input_video%" == "m" (
    echo ��:-video_size 960x540 -offset_x 961 -offset_y 541 -i desktop
    set /p input_video=[�T�C�Y�A�I�t�Z�b�g�I�t�Z�b�g�A����]:
) else if "%ask_input_video%" == "w" (
    echo ��:-i chrome.exe
    set /p input_video=[�E�B���h�E�̃^�C�g��]:
) else if "%ask_input_video%" == "" (
    set "input_video=-i desktop"
)
echo %input_video%

rem ====================��������====================
set /p ask_input_audio=��������[Enter:�����Ȃ��Aa:AG03]:
if "%ask_input_audio%" == "a" (
    set "input_audio=-f dshow -i audio^=^"���C�� ^(AG06^/AG03^)^" -c:a aac -b:a 320k -ar 44100"
) else if "%ask_input_audio%" == "" (
    set "input_audio=-an"
)
echo %input_audio%

rem ====================vf====================
set /p ask_vf=���T�C�Y[Enter:���Ȃ��A�𑜓x:����]:
if "%ask_vf%" == "" (
    set vf=
) else (
    set "vf=-vf scale^=%ask_vf%"
)

rem ====================quality====================
set /p quality=�i��[int�AEnter:27]:
if not defined quality (
    set quality=27
)

rem ====================�t�@�C�����̓��t����====================
rem yyMMdd_Hmm
rem �����p(17/08/30 (��) 17:35->170830_1735)
set mydate=%date:~0,2%%date:~3,2%%date:~6,2%_%time:~0,2%%time:~3,2%
rem �����ݒ�(2017/08/30 17:35 -> 170830_1735)
rem set mydate=%date:~2,2%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
rem �X�y�[�X��0�ɒu��������
set mydate=%mydate: =0%

rem ====================�G���R====================
rem �^��J�n���邩����
set /p hoge=�^����J�n����ɂ͉����L�[�������Ă������� . . .
rem �ʃv���Z�X�ōŏ�����ffmpeg���N������
:encode
timeout /t 1
start /high /min ffmpeg -y -hide_banner -fflags +discardcorrupt -f gdigrab -r 30000/1001 -draw_mouse %draw_mouse% -show_region 1 %input_video% %input_audio% %vf% -global_quality %quality% -c:v h264_qsv -preset slow -g 15 -bf 2 -refs 4 -b_strategy 1 -look_ahead 1 -pix_fmt nv12 -movflags +faststart "C:\Users\Shibanyan\Desktop\ffrec_%mydate%.mp4"
rem �I���R�[�h1�̏ꍇ���[�v
if %errorlevel% equ 1 (
    goto :encode
)
exit


