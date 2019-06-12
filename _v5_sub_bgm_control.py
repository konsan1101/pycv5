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



qCtrl_bgm   = 'temp/control_bgm_control.txt'



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



def bgm_open(runMode, inpText, ):
    global main_last

    procBgm = ''
    if (inpText == 'playlist 00'  ) or (inpText == 'playlist 0') \
    or (inpText == 'playlist zero') \
    or (inpText == 'bgm') or (inpText == 'garageband'):
        procBgm =  '_00_'

    if (inpText == 'playlist 01' ) or (inpText == 'playlist 1') \
    or (inpText == 'playlist etc') or (inpText == 'playlists etc'):
        procBgm =  '_01_'

    if (inpText == 'playlist 02') or (inpText == 'playlist 2') \
    or (inpText == 'babymetal'):
        procBgm =  '_02_'

    if (inpText == 'playlist 03') or (inpText == 'playlist 3') \
    or (inpText == 'perfume'):
        procBgm =  '_03_'

    if (inpText == 'playlist 04') or (inpText == 'playlist 4') \
    or (inpText == 'kyary pamyu pamyu'):
        procBgm =  '_04_'

    if (inpText == 'playlist 05') or (inpText == 'playlist 5') \
    or (inpText == 'one ok rock') or (inpText == 'one ok'):
        procBgm =  '_05_'

    if (inpText == 'playlist 06') or (inpText == 'playlist 6') \
    or (inpText == 'the end of the world') or (inpText == 'end of the world'):
        procBgm =  '_06_'

    if (inpText == 'playlist') or (inpText == 'playlist list') \
    or (inpText == 'list of playlists') or (inpText == 'bgm list'):
        wrkText = u'プレイリストゼロは、自作ＢＧＭです。'
        qFunc.tts('bgmcontrol.00', wrkText, )
        wrkText = u'プレイリスト１は、お気に入り音楽です。'
        qFunc.tts('bgmcontrol.01', wrkText, )
        wrkText = u'プレイリスト２は、「BABYMETAL」です。'
        qFunc.tts('bgmcontrol.02', wrkText, )
        wrkText = u'プレイリスト３は、「perfume」です。'
        qFunc.tts('bgmcontrol.03', wrkText, )
        wrkText = u'プレイリスト４は、「きゃりーぱみゅぱみゅ」です。'
        qFunc.tts('bgmcontrol.04', wrkText, )
        wrkText = u'プレイリスト５は、「ONE OK ROCK」です。'
        qFunc.tts('bgmcontrol.05', wrkText, )
        wrkText = u'プレイリスト６は、「SEKAI NO OWARI」です。'
        qFunc.tts('bgmcontrol.06', wrkText, )
        wrkText = u'プレイリストを再生しますか？'
        qFunc.tts('bgmcontrol.07', wrkText, )

    if (procBgm != ''):
        qFunc.kill('VLC', )

    if (procBgm != '_close_'):
        plist = ''
        pparm = ''
        if (os.name == 'nt'):
            if (procBgm == '_00_'):
                plist = u'C:\\Users\\Public\\_VLC_GB_プレイリスト.xspf'
                pparm = '--qt-start-minimized'
            if (procBgm == '_01_'):
                plist = u'C:\\Users\\Public\\_VLC_etc_プレイリスト.xspf'
            if (procBgm == '_02_'):
                plist = u'C:\\Users\\Public\\_VLC_BABYMETAL_プレイリスト.xspf'
            if (procBgm == '_03_'):
                plist = u'C:\\Users\\Public\\_VLC_Perfume_プレイリスト.xspf'
            if (procBgm == '_04_'):
                plist = u'C:\\Users\\Public\\_VLC_きゃりーぱみゅぱみゅ_プレイリスト.xspf'
            if (procBgm == '_05_'):
                plist = u'C:\\Users\\Public\\_VLC_ワンオク_プレイリスト.xspf'
            if (procBgm == '_06_'):
                plist = u'C:\\Users\\Public\\_VLC_セカオワ_プレイリスト.xspf'
            if (plist != ''):
                main_last = time.time()
                try:
                    if (pparm != ''):
                        bgm = subprocess.Popen(['VLC', pparm, plist, ], \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    else:
                        bgm = subprocess.Popen(['VLC', plist, ], \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #bgm.wait()
                    #bgm.terminate()
                    #bgm = None
                except:
                    pass
        else:
            if (procBgm == '_00_'):
                plist = u'/users/kondou/Documents/_VLC_GB_プレイリスト.xspf'
                pparm = '--qt-start-minimized'
            if (procBgm == '_01_'):
                plist = u'/users/kondou/Documents/_VLC_etc_プレイリスト.xspf'
            if (procBgm == '_02_'):
                plist = u'/users/kondou/Documents/_VLC_BABYMETAL_プレイリスト.xspf'
            if (procBgm == '_03_'):
                plist = u'/users/kondou/Documents/_VLC_Perfume_プレイリスト.xspf'
            if (procBgm == '_04_'):
                plist = u'/users/kondou/Documents/_VLC_きゃりーぱみゅぱみゅ_プレイリスト.xspf'
            if (procBgm == '_05_'):
                plist = u'/users/kondou/Documents/_VLC_ワンオク_プレイリスト.xspf'
            if (procBgm == '_06_'):
                plist = u'/users/kondou/Documents/_VLC_セカオワ_プレイリスト.xspf'
            if (plist != ''):
                main_last = time.time()
                try:
                    if (pparm != ''):
                        #bgm = subprocess.Popen(['open', '-a', 'VLC', plist, pparm, ], \
                        bgm = subprocess.Popen(['open', '-a', 'VLC', plist, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    else:
                        bgm = subprocess.Popen(['open', '-a', 'VLC', plist, ], \
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #bgm.wait()
                    #bgm.terminate()
                    #bgm = None
                except:
                    pass



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
    qFunc.logOutput('bgm_main__:init')
    qFunc.logOutput('bgm_main__:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrl_bgm

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]

    qFunc.logOutput('bgm_main__:runMode  =' + str(runMode  ))
    qFunc.logOutput('bgm_main__:inpFile  =' + str(inpFile  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qFunc.logOutput('bgm_main__:start')



    wrkText = u'ＢＧＭ制御機能が起動しました。'
    qFunc.tts('bgmcontrol.00', wrkText, )

    main_start = time.time()
    while (True):
            if (main_last is None):
                sec = int(time.time() - main_start)
                if (sec > 60):
                    wrkText = u'ＢＧＭを開始しましょうか？'
                    qFunc.tts('bgmcontrol.99', wrkText, )
                    main_last = time.time()

            #try:
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
                        #qFunc.logOutput(u'★KONSAN : [' + str(inpText) + ']')
                        bgm_open(runMode=runMode, inpText=inpText, )

            #except:
            #pass

            time.sleep(0.50)



    qFunc.logOutput('bgm_main__:terminate')

    qFunc.kill('VLC', )

    wrkText = u'ＢＧＭ制御機能を終了しました。'
    qFunc.tts('bgmcontrol.99', wrkText, )

    qFunc.logOutput('bgm_main__:bye!')



