#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2019 Mitsuo KONDOU.
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

# 音声処理 api
import       _v5_api_speech
api_speech = _v5_api_speech.api_speech_class()



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('self_check:init')
    qFunc.logOutput('self_check:exsample.py runMode,')

    runMode = 'debug'
    check   = 'all'

    if (len(sys.argv) >= 2):
        runMode  = sys.argv[1]
    if (len(sys.argv) >= 3):
        check    = sys.argv[2]

    #check   = 'demo'

    qFunc.logOutput('self_check:runMode  =' + str(runMode  ))
    qFunc.logOutput('self_check:check    =' + str(check    ))

    qFunc.logOutput('')
    qFunc.logOutput('self_check:start')

    lang = 'ja,hoya,'



    if (check == 'all') or (check == 'demo'):
        text = u'BGM'
        api_speech.loopback(text, 'ja,free,', )

        text = u'画像処理の開始'
        api_speech.loopback(text, 'ja,free,', )

        text = u'プレイリスト 0'
        api_speech.loopback(text, 'ja,free,', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        speechs = []
        speechs.append({'text':u'こんにちは。私はハンズフリーコントロール翻訳システムです。', 'wait':0, })
        speechs.append({'text':u'私は、近藤家の自家用車ＭＰＶで動作するように設計されました。', 'wait':0, })
        speechs.append({'text':u'これから自己診断を兼ねて、私自身の機能紹介を行います。', 'wait':0, })
        speechs.append({'text':u'このナレーションは、主にＨＯＹＡの音声合成ＡＩが担当します。', 'wait':0, })
        speechs.append({'text':u'よろしくお願いします。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        speechs = []
        speechs.append({'text':u'こんにちは。私はハンズフリーコントロール翻訳システムです。', 'wait':0, })
        speechs.append({'text':u'これから自己診断を兼ねて、私自身の機能紹介を行います。', 'wait':0, })
        speechs.append({'text':u'よろしくお願いします。', 'wait':0, })
        qFunc.speech(speechs, '', )



    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        speechs = []
        speechs.append({'text':u'翻訳機能', 'wait':0, })
        speechs.append({'text':u'音声認識、機械翻訳、音声合成機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、翻訳機能の自己テストを開始します。', 'wait':0, })
        qFunc.speech(speechs, lang, )

        text = u'A.P.I.一覧。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        text = u'スペシャル。'
        api_speech.loopback(text, 'ja,free,', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

        text = u'コンテスト。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

    if (check == 'all') or (check == u'翻訳'):
        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'n.i.c.t.'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

        text = u'アイビーエム。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

        text = u'マイクロソフト。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

        text = u'グーグル。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )

        text = u'デフォルト。'
        api_speech.loopback(text, 'ja,free,', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        if (check == 'all'):
            now2=datetime.datetime.now()
            text  = u'現在の日時は、'
            text += now2.strftime('%m') + u'月'
            text += now2.strftime('%d') + u'日、'
            text += now2.strftime('%H') + u'時'
            text += now2.strftime('%M') + u'分'
            text += now2.strftime('%S') + u'秒です'
            api_speech.loopback(text, lang, )



    if (check == 'all') or (check == u'翻訳') or (check == 'demo'):

        text = u'言語は何ですか？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'フランス語。'
        api_speech.loopback(text, lang, )

        text = u'2020年。日本で逢いましょう。'
        api_speech.loopback(text, lang, )

        text = u'英語。'
        api_speech.loopback(text, 'ja,free,', )

        speechs = []
        speechs.append({'text':u'翻訳機能の紹介を終わります。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        qFunc.speech(speechs, '',   )



    if (check == 'all') or (check == u'ハンズフリー') or (check == 'demo'):
        qFunc.busyWait(idolSec=5, maxWait=30, )

        speechs = []
        speechs.append({'text':u'ハンズフリー制御', 'wait':0, })
        speechs.append({'text':u'ハンズフリー制御機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'この翻訳システムで対処できない場合、外部のデバイスと連携します。', 'wait':0, })
        if (check == 'demo'):
            speechs.append({'text':u'デモンストレーションでは、ＢＧＭの制御機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、ハンズフリー機能の自己テストを開始します。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        speechs = []
        speechs.append({'text':u'ハンズフリー機能', 'wait':0, })
        speechs.append({'text':u'ハンズフリー機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、ハンズフリー機能の自己テストを開始します。', 'wait':0, })
        qFunc.speech(speechs, '', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'プレイリスト。一覧。'
        #api_speech.loopback(text, lang, )
        api_speech.loopback(text, 'ja,free,', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'bgm'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'bgm。ストップ。'
        api_speech.loopback(text, lang, )

        text = u'三木市の天気。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

    if (check == 'all') or (check == u'ハンズフリー'):

        text = u'姫路市のニュース。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'岡山大学の住所を調べて？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'ブラウザー。'
        api_speech.loopback(text, lang, )

        text = u'岡山大学。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'ブラウザー。ストップ。'
        api_speech.loopback(text, lang, )

        text = u'知識データベース開始。'
        api_speech.loopback(text, lang, )

        text = u'富士山の高さは？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'知識データベース終了。'
        api_speech.loopback(text, lang, )

        text = u'雑談開始。'
        api_speech.loopback(text, lang, )

        text = u'富士山の高さ知ってる？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'雑談終了。'
        api_speech.loopback(text, lang, )

        text = u'ここの住所調べて？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'ここから姫路城の経路調べて？'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        text = u'アミに電話して。'
        api_speech.loopback(text, lang, )

        qFunc.busyWait(idolSec=5, maxWait=30, )

    if (check == 'all') or (check == u'ハンズフリー') or (check == 'demo'):

        speechs = []
        speechs.append({'text':u'ハンズフリー制御機能の紹介を終わります。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        qFunc.speech(speechs, '',   )



    if (check == 'all') or (check == u'連携') or (check == 'demo'):
        qFunc.busyWait(idolSec=5, maxWait=30, )

        speechs = []
        speechs.append({'text':u'外部ＡＩ連携機能', 'wait':0, })
        speechs.append({'text':u'スマートスピーカー等の外部機器との連携機能を紹介します。', 'wait':0, })
        if (check == 'demo'):
            speechs.append({'text':u'デモンストレーションでは、アイフォーンのSiriに連携します。', 'wait':0, })
        speechs.append({'text':u'それでは、外部ＡＩ連携機能の自己テストを開始します。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        speechs = []
        speechs.append({'text':u'外部ＡＩ連携機能', 'wait':0, })
        speechs.append({'text':u'スマートスピーカー等の外部機器との連携機能を紹介します。', 'wait':0, })
        speechs.append({'text':u'それでは、外部ＡＩ連携機能の自己テストを開始します。', 'wait':0, })
        qFunc.speech(speechs, '', )

        qFunc.busyWait(idolSec=5, maxWait=30, )

        speechtext  = u'ja,hoya,調子はどうですか？'

        smart = 'siri'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        qFunc.busyWait(idolSec=5, maxWait=30, )

    if (check == 'all') or (check == u'連携'):

        speechtext  = u'ja,hoya,調子はどうですか？'

        smart = 'clova'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        qFunc.busyWait(idolSec=5, maxWait=30, )

        smart = 'google'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        qFunc.busyWait(idolSec=5, maxWait=30, )

        smart = 'alexa'
        smtspk= subprocess.Popen(['python', '_handsfree_smart_speaker.py', runMode, speechtext, smart, ], )
                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        smtspk.wait()
        smtspk.terminate()
        smtspk = None

        qFunc.busyWait(idolSec=5, maxWait=30, )

    if (check == 'all') or (check == u'連携') or (check == 'demo'):
        speechs = []
        speechs.append({'text':u'連携機能の紹介を終わります。', 'wait':0, })
        qFunc.speech(speechs, lang, )
        qFunc.speech(speechs, '',   )



    if (check == 'all') or (check == 'demo'):
        qFunc.busyWait(idolSec=5, maxWait=30, )

        speechs = []
        speechs.append({'text':u'自己診断と機能紹介が終わりました。', 'wait':0, })
        speechs.append({'text':u'いかがでしたでしょうか。ありがとうございました', 'wait':0, })
        qFunc.speech(speechs, lang, )
        qFunc.speech(speechs, '',   )



    qFunc.logOutput('')
    qFunc.logOutput('self_check:terminate')

    qFunc.logOutput('self_check:bye!')



