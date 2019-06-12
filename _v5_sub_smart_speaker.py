#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
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

qOS            = qFunc.getValue('qOS'           )
qPath_log      = qFunc.getValue('qPath_log'     )
qPath_work     = qFunc.getValue('qPath_work'    )
qPath_rec      = qFunc.getValue('qPath_rec'     )

qPath_a_ctrl   = qFunc.getValue('qPath_a_ctrl'  )
qPath_a_inp    = qFunc.getValue('qPath_a_inp'   )
qPath_a_wav    = qFunc.getValue('qPath_a_wav'   )
qPath_a_jul    = qFunc.getValue('qPath_a_jul'   )
qPath_a_STT    = qFunc.getValue('qPath_a_STT'   )
qPath_a_TTS    = qFunc.getValue('qPath_a_TTS'   )
qPath_a_TRA    = qFunc.getValue('qPath_a_TRA'   )
qPath_a_play   = qFunc.getValue('qPath_a_play'  )
qPath_v_ctrl   = qFunc.getValue('qPath_v_ctrl'  )
qPath_v_inp    = qFunc.getValue('qPath_v_inp'   )
qPath_v_jpg    = qFunc.getValue('qPath_v_jpg'   )
qPath_v_detect = qFunc.getValue('qPath_v_detect')
qPath_v_cv     = qFunc.getValue('qPath_v_cv'    )
qPath_v_photo  = qFunc.getValue('qPath_v_photo' )

qBusy_dev_cpu  = qFunc.getValue('qBusy_dev_cpu' )
qBusy_dev_mic  = qFunc.getValue('qBusy_dev_mic' )
qBusy_dev_spk  = qFunc.getValue('qBusy_dev_spk' )
qBusy_dev_cam  = qFunc.getValue('qBusy_dev_cam' )
qBusy_dev_dsp  = qFunc.getValue('qBusy_dev_dsp' )
qBusy_a_ctrl   = qFunc.getValue('qBusy_a_ctrl'  )
qBusy_a_inp    = qFunc.getValue('qBusy_a_inp'   )
qBusy_a_wav    = qFunc.getValue('qBusy_a_wav'   )
qBusy_a_STT    = qFunc.getValue('qBusy_a_STT'   )
qBusy_a_TTS    = qFunc.getValue('qBusy_a_TTS'   )
qBusy_a_TRA    = qFunc.getValue('qBusy_a_TRA'   )
qBusy_a_play   = qFunc.getValue('qBusy_a_play'  )
qBusy_v_ctrl   = qFunc.getValue('qBusy_v_ctrl'  )
qBusy_v_inp    = qFunc.getValue('qBusy_v_inp'   )
qBusy_v_jpg    = qFunc.getValue('qBusy_v_jpg'   )
qBusy_v_CV     = qFunc.getValue('qBusy_v_CV'    )



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
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
        stamp=now.strftime('%Y%m%d-%H%M%S')

        if (smart == 'siri'):
            #txt = 'en,Hey, Siri'
            #qFunc.tts(id, txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ヘイSiri.mp3'
            print(mp3)
            wrkFile = qPath_a_play + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            time.sleep(2.00)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'google'):
            #txt = 'ja,ねぇグーグル'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ねぇグーグル.mp3'
            print(mp3)
            wrkFile = qPath_a_play + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'alexa'):
            #txt = 'ja,アレクサ'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_アレクサ.mp3'
            print(mp3)
            wrkFile = qPath_a_play + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )

        if (smart == 'clova'):
            #txt = 'ja,ねぇクローバ'
            #qFunc.tts('smartspeaker.01', txt, )

            id  = 'smartspeaker.01'
            mp3 = u'_sound_handsfree_ねぇクローバ.mp3'
            print(mp3)
            wrkFile = qPath_a_play + stamp + '.' + id + '.mp3'
            shutil.copy2(mp3, wrkFile)

            id  = 'smartspeaker.02'
            qFunc.tts(id, outText, idolSec=1, maxWait=0, )



    qFunc.logOutput('smart_spk_:terminate')
    qFunc.logOutput('smart_spk_:bye!')



