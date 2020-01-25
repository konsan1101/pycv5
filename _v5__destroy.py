#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs
import glob



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_chatting   = 'temp/control_chatting.txt'
qCtrl_control_knowledge  = 'temp/control_knowledge.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qPLATFORM       = qFunc.getValue('qPLATFORM'      )
qRUNATTR        = qFunc.getValue('qRUNATTR'       )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
qPath_cache     = qFunc.getValue('qPath_cache'    )
qPath_sounds    = qFunc.getValue('qPath_sounds'   )
qPath_icons     = qFunc.getValue('qPath_icons'    )
qPath_fonts     = qFunc.getValue('qPath_fonts'    )
qPath_log       = qFunc.getValue('qPath_log'      )
qPath_work      = qFunc.getValue('qPath_work'     )
qPath_rec       = qFunc.getValue('qPath_rec'      )

qPath_s_ctrl    = qFunc.getValue('qPath_s_ctrl'   )
qPath_s_inp     = qFunc.getValue('qPath_s_inp'    )
qPath_s_wav     = qFunc.getValue('qPath_s_wav'    )
qPath_s_jul     = qFunc.getValue('qPath_s_jul'    )
qPath_s_STT     = qFunc.getValue('qPath_s_STT'    )
qPath_s_TTS     = qFunc.getValue('qPath_s_TTS'    )
qPath_s_TRA     = qFunc.getValue('qPath_s_TRA'    )
qPath_s_play    = qFunc.getValue('qPath_s_play'   )
qPath_v_ctrl    = qFunc.getValue('qPath_v_ctrl'   )
qPath_v_inp     = qFunc.getValue('qPath_v_inp'    )
qPath_v_jpg     = qFunc.getValue('qPath_v_jpg'    )
qPath_v_detect  = qFunc.getValue('qPath_v_detect' )
qPath_v_cv      = qFunc.getValue('qPath_v_cv'     )
qPath_v_photo   = qFunc.getValue('qPath_v_photo'  )
qPath_v_msg     = qFunc.getValue('qPath_v_msg'    )
qPath_d_ctrl    = qFunc.getValue('qPath_d_ctrl'   )
qPath_d_play    = qFunc.getValue('qPath_d_play'   )
qPath_d_prtscn  = qFunc.getValue('qPath_d_prtscn' )
qPath_d_movie   = qFunc.getValue('qPath_d_movie'  )
qPath_d_upload  = qFunc.getValue('qPath_d_upload' )

qBusy_dev_cpu   = qFunc.getValue('qBusy_dev_cpu'  )
qBusy_dev_com   = qFunc.getValue('qBusy_dev_com'  )
qBusy_dev_mic   = qFunc.getValue('qBusy_dev_mic'  )
qBusy_dev_spk   = qFunc.getValue('qBusy_dev_spk'  )
qBusy_dev_cam   = qFunc.getValue('qBusy_dev_cam'  )
qBusy_dev_dsp   = qFunc.getValue('qBusy_dev_dsp'  )
qBusy_dev_scn   = qFunc.getValue('qBusy_dev_scn'  )
qBusy_s_ctrl    = qFunc.getValue('qBusy_s_ctrl'   )
qBusy_s_inp     = qFunc.getValue('qBusy_s_inp'    )
qBusy_s_wav     = qFunc.getValue('qBusy_s_wav'    )
qBusy_s_STT     = qFunc.getValue('qBusy_s_STT'    )
qBusy_s_TTS     = qFunc.getValue('qBusy_s_TTS'    )
qBusy_s_TRA     = qFunc.getValue('qBusy_s_TRA'    )
qBusy_s_play    = qFunc.getValue('qBusy_s_play'   )
qBusy_v_ctrl    = qFunc.getValue('qBusy_v_ctrl'   )
qBusy_v_inp     = qFunc.getValue('qBusy_v_inp'    )
qBusy_v_QR      = qFunc.getValue('qBusy_v_QR'     )
qBusy_v_jpg     = qFunc.getValue('qBusy_v_jpg'    )
qBusy_v_CV      = qFunc.getValue('qBusy_v_CV'     )
qBusy_d_ctrl    = qFunc.getValue('qBusy_d_ctrl'   )
qBusy_d_inp     = qFunc.getValue('qBusy_d_inp'    )
qBusy_d_QR      = qFunc.getValue('qBusy_d_QR'     )
qBusy_d_rec     = qFunc.getValue('qBusy_d_rec'    )
qBusy_d_play    = qFunc.getValue('qBusy_d_play'   )
qBusy_d_browser = qFunc.getValue('qBusy_d_browser')
qBusy_d_upload  = qFunc.getValue('qBusy_d_upload' )
qRdy__s_force   = qFunc.getValue('qRdy__s_force'  )
qRdy__s_fproc   = qFunc.getValue('qRdy__s_fproc'  )
qRdy__s_sendkey = qFunc.getValue('qRdy__s_sendkey')
qRdy__v_reader  = qFunc.getValue('qRdy__v_reader' )
qRdy__v_sendkey = qFunc.getValue('qRdy__v_sendkey')
qRdy__d_reader  = qFunc.getValue('qRdy__d_reader' )
qRdy__d_sendkey = qFunc.getValue('qRdy__d_sendkey')



# debug
runMode     = 'debug'



if __name__ == '__main__':
    main_name = 'destroy'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qFunc.init()

    # ログ設定

    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput(main_id + ':init')
    qFunc.logOutput(main_id + ':exsample.py runMode, ')

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

    # 終了サイン

    if (runMode != 'faster'):

        qFunc.txtsWrite(qCtrl_control_kernel    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_speech    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_vision    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_desktop   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_bgm       ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_browser   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_player    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_chatting  ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_knowledge ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        print('Waiting...20s')
        time.sleep(20.00)

    # 終了

    qFunc.kill('adintool-gui')
    qFunc.kill('adintool')
    qFunc.kill('julius')
    qFunc.kill('sox')
    qFunc.kill('ffmpeg')
    qFunc.kill('VLC')
    qFunc.kill('firefox')
    qFunc.kill('ffplay')

    if (runMode != 'faster'):
        print('Waiting...5s')
        time.sleep(5.00)

    qFunc.kill('_v5__main__kernel')
    qFunc.kill('_v5__main_speech')
    qFunc.kill('_v5__main_vision')
    qFunc.kill('_v5__main_desktop')
    qFunc.kill('_v5__sub_bgm')
    qFunc.kill('_v5__sub_browser')
    qFunc.kill('_v5__sub_player')
    qFunc.kill('_v5__sub_chatting')
    qFunc.kill('_v5__sub_knowledge')

    qFunc.kill('_v5_proc_recorder')
    qFunc.kill('_v5_proc_uploader')



    if (runMode != 'faster'):
        print('Waiting...5s')
        time.sleep(5.00)

    qFunc.kill('python')


