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

import urllib
import feedparser



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS            = qFunc.getValue('qOS'           )
qHOSTNAME      = qFunc.getValue('qHOSTNAME'     )
qPath_log      = qFunc.getValue('qPath_log'     )
qPath_work     = qFunc.getValue('qPath_work'    )
qPath_rec      = qFunc.getValue('qPath_rec'     )

qPath_s_ctrl   = qFunc.getValue('qPath_s_ctrl'  )
qPath_s_inp    = qFunc.getValue('qPath_s_inp'   )
qPath_s_wav    = qFunc.getValue('qPath_s_wav'   )
qPath_s_jul    = qFunc.getValue('qPath_s_jul'   )
qPath_s_STT    = qFunc.getValue('qPath_s_STT'   )
qPath_s_TTS    = qFunc.getValue('qPath_s_TTS'   )
qPath_s_TRA    = qFunc.getValue('qPath_s_TRA'   )
qPath_s_play   = qFunc.getValue('qPath_s_play'  )
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



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('rss_main__:init')
    qFunc.logOutput('rss_main__:exsample.py runMode, inpText, ')

    runMode = 'debug'
    inpText = u'姫路城'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpText  = sys.argv[2]

    qFunc.logOutput('rss_main__:runMode  =' + str(runMode  ))
    qFunc.logOutput('rss_main__:inpText  =' + str(inpText  ))

    qFunc.logOutput('rss_main__:start')



    if (True):

        try:

            s_quote = urllib.parse.quote(inpText)
            url = 'https://news.google.com/news/rss/search/section/q/' + s_quote + '/' + s_quote + '?ned=jp&hl=ja&gl=JP'

            rss = feedparser.parse(url)

            lang = 'ja,hoya,'
            speechs = []

            i = 0
            for entry in rss['entries']:
                i += 1
                #print("title:", entry.title)
                #print("published: ", entry.published)
                #print("link: ", entry.link)

                txt = entry.title
                txt = txt.replace(u'ニュース', u'ニュース.')

                qFunc.logOutput(' RSS Text  [' + str(txt)  + ']')
                #qFunc.tts('rsssearch.{:02}'.format(i), 'ja,hoya,' + txt, )
                speechs.append({'text':txt, 'wait':0, })

                if (i >= 5):
                    break

            txt = u'以上が、主なニュースです。'

            #qFunc.logOutput(' RSS Text  [' + str(txt)  + ']')
            #qFunc.tts('rsssearch.99', 'ja,hoya,' + txt, )
            speechs.append({'text':txt, 'wait':0, })

            qFunc.speech(speechs, lang, )
            qFunc.speech(speechs, '',   )

        except:
            pass



    qFunc.logOutput('rss_main__:terminate')
    qFunc.logOutput('rss_main__:bye!')



