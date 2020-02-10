#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import datetime
import codecs
import glob



# qLog,qFunc 共通ルーチン
import  _v5__qLog
qLog  = _v5__qLog.qLog_class()
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qPath_log       = qFunc.getValue('qPath_log'      )



if __name__ == '__main__':

    # 共通クラス
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # パラメータ
    imgPath = '_icons/'
    imgFile = 'detect_speech.png'
    inpText = ''

    if (len(sys.argv) >= 2):
        wavPath = str(sys.argv[1])
        if (wavPath[:-1] != '/'):
            wavPath += '/'
    if (len(sys.argv) >= 3):
        wavFile  = str(sys.argv[2])
    if (len(sys.argv) >= 4):
        inpText  = str(sys.argv[3])

    # 画像表示
    imgFile = imgPath + imgFile
    qFunc.guideDisplay(display=True, panel='detect_speech', filename=imgFile, txt='', )

    # メッセージ
    time.sleep(1.00)
    if (inpText == ''):
        inpText = '!'
    qFunc.guideDisplay(display=True, txt=inpText, )
    time.sleep(3.00)

    # 画像消去
    qFunc.guideDisplay(display=False, )


