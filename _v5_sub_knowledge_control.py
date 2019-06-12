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



qCtrl_knowledge = 'temp/control_knowledge.txt'



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

# docomo 知識検索
import speech_api_docomo     as docomo_api
import speech_api_docomo_key as docomo_key



def speech(docomoAPI, runMode, inpText, ):
    res, api = docomoAPI.knowledge(inpText=inpText, )
    if (res != '') and (res != '!'):
        if (res[:6] != u'ごめんなさい'):
            qFunc.logOutput(u'★DOCOMO : [' + str(res) + ']')
            qFunc.tts('knowledge.01', 'ja,hoya,' + res, )
            qFunc.tts('knowledge.02', res, )
        else:
            txt = u'ごめんなさい。外部のＡＩに聞いてみます。'
            qFunc.tts('knowledge.00', txt, )

            time.sleep(5.00)

            speechtext = 'ja,hoya,' + inpText
            if (speechtext.find(u'ここ')>=0):
                smart = 'siri'
            else:
                smart = 'auto'
            smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            smtspk.wait()
            smtspk.terminate()
            smtspk = None



main_start = 0
main_last  = None
if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('knowledge_:init')
    qFunc.logOutput('knowledge_:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrl_knowledge
    inpText = ''

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]
    if (len(sys.argv) >= 4):
        inpText  = sys.argv[3]

    qFunc.logOutput('knowledge_:runMode  =' + str(runMode  ))
    qFunc.logOutput('knowledge_:inpFile  =' + str(inpFile  ))
    qFunc.logOutput('knowledge_:inpText  =' + str(inpText  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qFunc.logOutput('knowledge_:start')

    docomoAPI = docomo_api.SpeechAPI()
    res_run = docomoAPI.authenticate('knowledge', docomo_key.getkey('knowledge'), )
    if (res_run):

        if (inpText != '') and (inpText != '!'):
            qFunc.logOutput(u'★KONSAN : [' + str(inpText) + ']')
            speech(docomoAPI, runMode=runMode, inpText=inpText, )



        if (inpFile != ''):
            wrkText = u'DOCOMO知識データベース機能が起動しました。'
            qFunc.tts('knowledge.00', wrkText, )

        main_start = time.time()
        while (inpFile != ''):
            if (main_last is None):
                sec = int(time.time() - main_start)
                if (sec > 60):
                    wrkText = u'何かお調べしましょうか？'
                    qFunc.tts('knowledge.99', wrkText, )
                    main_last = time.time()

            try:
                if (os.path.exists(tmpFile)):
                    os.remove(tmpFile)

                if (os.path.exists(inpFile)):
                    os.rename(inpFile, tmpFile)

                if (os.path.exists(tmpFile)):
                    rt = codecs.open(tmpFile, 'r', 'shift_jis')
                    inpText = ''
                    for t in rt:
                        inpText = (inpText + ' ' + str(t)).strip()
                    rt.close
                    rt = None

                    if (inpText == '_close_'):
                        break

                    if (inpText != '_open_'):
                        if (inpText != '') and (inpText != '!'):
                            main_last = time.time()
                            qFunc.logOutput(u'★KONSAN : [' + str(inpText) + ']')
                            speech(docomoAPI, runMode=runMode, inpText=inpText, )

            except:
                pass

            time.sleep(0.50)

        if (inpFile != ''):
            wrkText = u'DOCOMO知識データベース機能を終了しました。'
            qFunc.tts('knowledge.99', wrkText, )



    qFunc.logOutput('knowledge_:terminate')
    qFunc.logOutput('knowledge_:bye!')



