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

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont



qFONT_default = {'file':'_fonts/_vision_font_ipaexg.ttf','offset':10}
qFONT_zh = {'file':'C:/Windows/Fonts/msyh.ttc', 'offset':5}
qFONT_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}



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



class proc_txt2img:

    def __init__(self, name='thread', id='0', runMode='debug', drawWidth='0', ):
        self.runMode   = runMode
        self.drawWidth = drawWidth

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_{:01}'.format(int(id))
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qFunc.logOutput(self.proc_id + ':init', display=self.logDisp, )

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

    def __del__(self, ):
        qFunc.logOutput(self.proc_id + ':bye!', display=self.logDisp, )

    def start(self, ):
        #qFunc.logOutput(self.proc_id + ':start')

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ))
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0

        self.proc_main.setDaemon(True)
        self.proc_main.start()

    def stop(self, waitMax=5, ):
        qFunc.logOutput(self.proc_id + ':stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (not self.proc_beat is None) or (int(time.time() - chktime) < waitMax):
            time.sleep(0.10)

    def put(self, data, ):
        self.proc_s.put(data)        
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and (int(time.time() - chktime) < waitMax):
            time.sleep(0.10)
        data = self.get()
        return data

    def get(self, ):
        if (self.proc_r.qsize() == 0):
            return ['', '']        
        data = self.proc_r.get()        
        self.proc_r.task_done()
        return data

    def main_proc(self, cn_r, cn_s, ):
        # ログ
        qFunc.logOutput(self.proc_id + ':start', display=self.logDisp, )
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        fileRdy = qPath_work + self.proc_id + '.rdy'
        fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.remove(fileRdy)
        qFunc.remove(fileBsy)

        # フォント
        font18_default  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
        font18_defaulty =                    qFONT_default['offset']
        if (os.path.exists(qFONT_zh['file'])):
            font18_zh  = ImageFont.truetype(qFONT_zh['file']     , 18, encoding='unic')
            font18_zhy =                    qFONT_zh['offset']
        else:
            font18_zh  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
            font18_zhy =                    qFONT_default['offset']
        if (os.path.exists(qFONT_ko['file'])):
            font18_ko  = ImageFont.truetype(qFONT_ko['file']     , 18, encoding='unic')
            font18_koy =                    qFONT_ko['offset']
        else:
            font18_ko  = ImageFont.truetype(qFONT_default['file'], 18, encoding='unic')
            font18_koy =                    qFONT_default['offset']

        # 待機ループ
        self.proc_step = '5'

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # キュー取得
            if (cn_r.qsize() > 0):
                cn_r_get  = cn_r.get()
                inp_name  = cn_r_get[0]
                inp_value = cn_r_get[1]
                cn_r.task_done()
            else:
                inp_name  = ''
                inp_value = ''

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 20):
                qFunc.logOutput(self.proc_id + ':queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディ設定
            if (not os.path.exists(fileRdy)):
                qFunc.txtsWrite(fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )



            # 処理
            if (inp_name.lower() == '[txts]') \
            or (inp_name.lower() == '[status]'):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ビジー設定
                if (not os.path.exists(fileBsy)):
                    qFunc.txtsWrite(fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )

                # 画像処理
                if (True):

                    texts = inp_value

                    maxlen = 0
                    for i in range(0, len(texts)):
                        if (texts[i][2:3] != ','):
                                lenstr = len(texts[i]) * 2
                                if (maxlen < lenstr):
                                    maxlen = lenstr
                        else:
                            if  (texts[i][:3] == 'ja,') \
                            or  (texts[i][:3] == 'zh,') \
                            or  (texts[i][:3] == 'ko,'):
                                lenstr = len(texts[i]) * 2
                                if (maxlen < lenstr):
                                    maxlen = lenstr
                            else:
                                lenstr = len(texts[i])
                                if (maxlen < lenstr):
                                    maxlen = lenstr

                    draw_width  = int(self.drawWidth)
                    draw_height = int(10 + 30 * len(texts))
                    if (draw_width == 0):
                        if (inp_name.lower() == '[status]'):
                            draw_width = 180
                        else:
                            draw_width = int(50 + 9 * maxlen)

                    text_img  = Image.new('RGB', (draw_width, draw_height), (0xff, 0xff, 0xff))
                    text_draw = ImageDraw.Draw(text_img)

                    if (inp_name.lower() == '[status]'):
                        for i in range(0, len(texts)):
                            if (texts[i].find('busy' )>=0) \
                            or (texts[i].find('slow' )>=0) \
                            or (texts[i].find('disable' )>=0):
                                text_draw.rectangle((0, 30*i+5, draw_width, 30*(i+1)-1), fill=(0x00, 0x00, 0xff))
                            if (texts[i].find('ready' )>=0):
                                text_draw.rectangle((0, 30*i+5, draw_width, 30*(i+1)-1), fill=(0x00, 0xff, 0x00))

                    for i in range(0, len(texts)):
                        if (texts[i][2:3] != ','):
                                text_draw.text((5, 30*i + font18_defaulty), texts[i], font=font18_default, fill=(0x00, 0x00, 0x00))
                        else:
                            if   (texts[i][:3] == 'zh,'):
                                text_draw.text((5, 30*i + font18_zhy), texts[i], font=font18_zh, fill=(0x00, 0x00, 0x00))
                            elif (texts[i][:3] == 'ko,'):
                                text_draw.text((5, 30*i + font18_koy), texts[i], font=font18_ko, fill=(0x00, 0x00, 0x00))
                            else:
                                text_draw.text((5, 30*i + font18_defaulty), texts[i], font=font18_default, fill=(0x00, 0x00, 0x00))

                    # 結果出力
                    if (inp_name.lower() == '[txts]'):
                        out_name  = '[img]'
                        out_value = np.asarray(text_img)
                        cn_s.put([out_name, out_value])
                    if (inp_name.lower() == '[status]'):
                        out_name  = '[status_img]'
                        out_value = np.asarray(text_img)
                        cn_s.put([out_name, out_value])



            # ビジー解除
            if (cn_r.qsize() == 0):
                qFunc.remove(fileBsy)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qFunc.logOutput(self.proc_id + ':end', display=self.logDisp, )
            self.proc_beat = None



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)



    txt2img_thread = proc_txt2img('txt2img', '0', )
    txt2img_thread.start()

    txt2img_thread.put(['[txts]', [u'おはようございます']])
    resdata = txt2img_thread.checkGet()
    if (resdata[0] == '[img]'):
        img = resdata[1].copy()
        cv2.namedWindow('Display',  1)
        cv2.imshow('Display', img )
        cv2.waitKey(1)
        time.sleep(5)

    txt2img_thread.put(['[txts]', [u'こんにちは', u'はじめまして']])
    resdata = txt2img_thread.checkGet()
    if (resdata[0] == '[img]'):
        img = resdata[1].copy()
        cv2.namedWindow('Display',  1)
        cv2.imshow('Display', img )
        cv2.waitKey(1)
        time.sleep(5)

    time.sleep(1)
    txt2img_thread.stop()
    del txt2img_thread



    cv2.destroyAllWindows()


