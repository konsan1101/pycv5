#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs
import glob

import requests as web
import bs4
import urllib.parse



qCtrl_web   = 'temp/control_web_control.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS            = qFunc.getValue('qOS'           )
qHOSTNAME      = qFunc.getValue('qHOSTNAME'     )
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
qPath_v_msg    = qFunc.getValue('qPath_v_msg'   )
qPath_v_movie  = qFunc.getValue('qPath_v_movie' )
qPath_v_screen = qFunc.getValue('qPath_v_screen')

qBusy_dev_cpu  = qFunc.getValue('qBusy_dev_cpu' )
qBusy_dev_com  = qFunc.getValue('qBusy_dev_com' )
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
qBusy_v_rec    = qFunc.getValue('qBusy_v_rec'   )



def web_open(runMode, inpText, url='', ):
    #url   = ''
    title = ''
    text  = ''

    if (url == ''):
        try:
            # キーワードを使って検索する
            list_keywd = [inpText]
            resp = web.get('https://www.google.co.jp/search?num=10&q=' + '　'.join(list_keywd))
            resp.raise_for_status()

            # 取得したHTMLをパースする
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            link_elem01 = soup.select('.r > a')
            link_elem02 = soup.select('.s > .st')

            title = link_elem01[0].get_text()
            title = urllib.parse.unquote(title)

            text  = link_elem01[0].get_text()
            text  = urllib.parse.unquote(text)
            text  = text.replace('\n', '')

            url   = link_elem01[0].get('href')
            url   = url.replace('/url?q=', '')
            if (url.find('&sa=') >= 0):
                url = url[:url.find('&sa=')]
            url   = urllib.parse.unquote(url)
            url   = urllib.parse.unquote(url)

        except:
            pass

    if (url != ''):
        if (title != ''):
            qFunc.logOutput(' Web Title [' + str(title) + ']')

        if (text != ''):
            qFunc.logOutput(' Web Text  [' + str(text)  + ']')

            if (runMode=='debug' or runMode=='translator' or runMode=='learning'):
                wrkText = text + u'のホームページを表示します。'
                qFunc.tts(runMode, 'webcontrol.01', wrkText, )

        if (url[:4] != 'http'):
            url = 'https://google.co.jp' + url
        qFunc.logOutput(' Web URL   [' + str(url)   + ']')

        if (os.name == 'nt'):
            #qFunc.kill('iexplore', )
            qFunc.kill('chrome', )
            #qFunc.kill('Safari', )
            #qFunc.kill('firefox', )
            #qFunc.kill('microsoftedge', )
        else:
            qFunc.kill('Goocle Chrome', )

        if (os.name == 'nt'):
            #browser = 'C:\\Program Files\\Internet Explorer\\iexplore.exe'
            browser = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            #browser = 'C:\\Program Files (x86)\\Safari\\Safari.exe'
            #browser = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
            #browser = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            #browser = 'microsoft-edge:'
            bat = subprocess.Popen([browser, url, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #bat.wait()
            #bat.terminate()
            #bat = None
        else:
            bat = subprocess.Popen(['open', '-a', 'Goocle Chrome', url, ], \
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            #bat.wait()
            #bat.terminate()
            #bat = None



main_start = 0
main_last  = None
if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('web_main__:init')
    qFunc.logOutput('web_main__:exsample.py runMode, inpFile, ')

    runMode = 'debug'
    inpFile = qCtrl_web

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpFile  = sys.argv[2]

    qFunc.logOutput('web_main__:runMode  =' + str(runMode  ))
    qFunc.logOutput('web_main__:inpFile  =' + str(inpFile  ))

    tmpFile = inpFile[:-4] + '.tmp'

    qFunc.logOutput('web_main__:start')



    wrkText = u'ブラウザー制御機能が起動しました。'
    qFunc.tts('webcontrol.00', wrkText, )

    #url='https://google.co.jp'
    url='https://www.pscp.tv/search?q=konsan1101'
    web_open(runMode=runMode, inpText='', url=url, )
    time.sleep(3.00)

    main_start = time.time()
    while (True):
        if (main_last is None):
            sec = (time.time() - main_start)
            if (sec > 60):
                wrkText = u'何かＷｅｂ検索しませんか？'
                qFunc.tts('webcontrol.99', wrkText, )
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
                        #qFunc.logOutput(u'★KONSAN : [' + str(inpText) + ']')
                        web_open(runMode=runMode, inpText=inpText, url='', )

        except:
            pass

        time.sleep(0.50)



    qFunc.logOutput('web_main__:terminate')

    if (os.name == 'nt'):
        #qFunc.kill('iexplore', )
        qFunc.kill('chrome', )
        #qFunc.kill('Safari', )
        #qFunc.kill('firefox', )
        #qFunc.kill('microsoftedge', )
    else:
        qFunc.kill('Goocle Chrome', )

    wrkText = u'ブラウザー制御機能を終了しました。'
    qFunc.tts('webcontrol.99', wrkText, )

    qFunc.logOutput('web_main__:bye!')



