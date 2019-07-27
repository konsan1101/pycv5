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

# weather 天気予報
import speech_api_weather     as weather_api
import speech_api_weather_key as weather_key



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('weather___:init')
    qFunc.logOutput('weather___:exsample.py runMode, inpText, ')

    runMode = 'debug'
    inpText = u'三木市'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpText  = sys.argv[2]

    qFunc.logOutput('weather___:runMode  =' + str(runMode  ))
    qFunc.logOutput('weather___:inpText  =' + str(inpText  ))

    qFunc.logOutput('weather___:start')



    if (True):

        tenkiAPI = weather_api.WeatherAPI()

        city = inpText
        lang = 'ja,hoya,'

        api = 'openweathermap'
        key = weather_key.getkey(api)
        weather, temp_max, temp_min, humidity = \
            tenkiAPI.getWeather(api, key, city, )

        if (weather != ''):
            speechs = []
            speechs.append({'text':city + u'、今日の天気は、「' + weather + u'」です。', 'wait':0, })
            if (temp_max != ''):
                speechs.append({'text':u'最高気温は、' + temp_max + u'℃。', 'wait':0, })
            if (temp_min != ''):
                speechs.append({'text':u'最低気温は、' + temp_min + u'℃。', 'wait':0, })
            if (humidity != ''):
                speechs.append({'text':u'湿度は、' + humidity + u'%です。', 'wait':0, })
            qFunc.speech(speechs, lang, )
            qFunc.speech(speechs, '',   )

        else:
            txt = u'ごめんなさい。外部のＡＩに聞いてみます。'
            qFunc.tts('weather.00', txt, )

            time.sleep(5.00)

            speechtext = 'ja,hoya,' + city + u'の天気？'
            smart = 'auto'
            smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            smtspk.wait()
            smtspk.terminate()
            smtspk = None



    qFunc.logOutput('weather___:terminate')
    qFunc.logOutput('weather___:bye!')



