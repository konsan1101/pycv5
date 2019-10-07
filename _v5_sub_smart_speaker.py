#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
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

import random



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS             = qFunc.getValue('qOS'            )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
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



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('smart_spk_:init')
    qFunc.logOutput('smart_spk_:exsample.py runMode, outText, outSmart,')

    runMode = 'debug'
    outText = u'今なんじ'
    outSmart= 'auto'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        outText  = sys.argv[2]
    if (len(sys.argv) >= 4):
        outSmart = sys.argv[3]

    qFunc.logOutput('smart_spk_:runMode  =' + str(runMode  ))
    qFunc.logOutput('smart_spk_:outText  =' + str(outText  ))
    qFunc.logOutput('smart_spk_:outSmart =' + str(outSmart ))

    qFunc.logOutput('smart_spk_:start')

    if (True):

        smart = outSmart

        #smart = 'siri'
        #print('#############SIRI##############')

        if (smart == 'auto'):
            if (outText.find(u'現在地')>=0) \
            or (outText.find(u'ここ' )>=0) \
            or (outText.find(u'此処' )>=0):
                smart = 'siri'

        if (smart == 'auto'):
            i=random.randrange(1,4)
            if (i == 1):
                smart = 'siri'
            if (i == 2):
                smart = 'google'
            if (i == 3):
                smart = 'alexa'
            if (i == 4):
                smart = 'clova'

        qFunc.busyWait(idolSec=2, maxWait=15, )

        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d.%H%M%S')

        if (smart == 'siri'):
            #txt = 'en,Hey, Siri'
            #qFunc.tts(id, txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sounds/_sound_handsfree_ヘイSiri.mp3'
            print(mp3)
            wrkFile = qPath_s_play + stamp + '.' + id + '.mp3'
            qFunc.copy(mp3, wrkFile)

            time.sleep(2.00)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'google'):
            #txt = 'ja,ねぇグーグル'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sounds/_sound_handsfree_ねぇグーグル.mp3'
            print(mp3)
            wrkFile = qPath_s_play + stamp + '.' + id + '.mp3'
            qFunc.copy(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'alexa'):
            #txt = 'ja,アレクサ'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sounds/_sound_handsfree_アレクサ.mp3'
            print(mp3)
            wrkFile = qPath_s_play + stamp + '.' + id + '.mp3'
            qFunc.copy(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'clova'):
            #txt = 'ja,ねぇクローバ'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sounds/_sound_handsfree_ねぇクローバ.mp3'
            print(mp3)
            wrkFile = qPath_s_play + stamp + '.' + id + '.mp3'
            qFunc.copy(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )



    qFunc.logOutput('smart_spk_:terminate')
    qFunc.logOutput('smart_spk_:bye!')



