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



class proc_overlay:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    dspMode='vga', dspStretch='0', dspRotate='0', dspZoom='1.0', ):
        self.runMode    = runMode
        self.dspMode    = dspMode
        self.dspStretch = dspStretch
        self.dspRotate  = dspRotate
        self.dspZoom    = dspZoom
        
        dspWidth, dspHeight = qFunc.getResolution(dspMode)
        self.dspWidth  = dspWidth
        self.dspHeight = dspHeight

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

        # 変数設定
        self.blue_mini  = np.zeros((240,320,3), np.uint8)
        self.black_mini = np.zeros((240,320,3), np.uint8)
        self.white_mini = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.blue_mini ,(0,0),(320,240),(255,  0,  0),-1)
        cv2.rectangle(self.black_mini,(0,0),(320,240),(  0,  0,  0),-1)
        cv2.rectangle(self.white_mini,(0,0),(320,240),(255,255,255),-1)
        self.blue_img = self.blue_mini.copy()
        cv2.putText(self.blue_img, 'No Image !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
        self.blue_img  = cv2.resize(self.blue_img.copy(), (self.dspWidth, self.dspHeight ))
        self.black_img = cv2.resize(self.black_mini     , (self.dspWidth, self.dspHeight ))
        self.white_img = cv2.resize(self.white_mini     , (self.dspWidth, self.dspHeight ))

        self.flag_camzoom    = 'off'
        self.flag_dspzoom    = 'off'
        self.flag_enter      = 'off'
        self.flag_cancel     = 'off'
        self.flag_background = 'on'
        self.flag_blackwhite = 'black'

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

        # 変数設定
        shutter_time    = time.time()
        shutter_img     = None
        cam1_time       = time.time()
        cam1_base       = self.blue_img.copy()
        cam1_mini       = self.blue_mini.copy()
        cam1_fps        = ''
        cam1_reso       = ''
        cam2_time       = time.time()
        cam2_base       = self.blue_img.copy()
        cam2_mini       = self.blue_mini.copy()
        cam2_fps        = ''
        cam2_reso       = ''
        comp_time       = time.time()
        comp_base       = self.blue_img.copy()
        comp_mini       = self.blue_mini.copy()
        comp_fps        = ''
        comp_reso       = ''
        reader_time     = time.time()
        reader_img      = None
        cvdetect1_time  = time.time()
        cvdetect1_base  = self.blue_img.copy()
        detect1_time    = time.time()
        detect1_img     = None
        cvdetect2_time  = time.time()
        cvdetect2_base  = self.blue_img.copy()
        detect2_time    = time.time()
        detect2_img     = None
        status_time     = time.time()
        status_img      = None
        ary_max         = 9
        ary_time        = {}
        ary_img         = {}
        for i in range(1, ary_max+1):
            ary_time[i] = time.time()
            ary_img[i]  = None
        txt_max         = 9
        txt_time        = {}
        txt_img         = {}
        for i in range(1, txt_max+1):
            txt_time[i] = time.time()
            txt_img[i]  = None

        # ＦＰＳ計測
        qFPS_class = _v5__qFunc.qFPS_class()

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

            if (cn_r.qsize() > 10) or (cn_s.qsize() > 20):
                qFunc.logOutput(self.proc_id + ':queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディ設定
            if (not os.path.exists(fileRdy)):
                qFunc.txtsWrite(fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])

            # 表示連携
            elif (inp_name.lower() == 'flag_camzoom'):
                self.flag_camzoom = inp_value
            elif (inp_name.lower() == 'flag_dspzoom'):
                self.flag_dspzoom = inp_value
            elif (inp_name.lower() == 'flag_enter'):
                self.flag_enter = inp_value
            elif (inp_name.lower() == 'flag_cancel'):
                self.flag_cancel = inp_value
            elif (inp_name.lower() == 'flag_background'):
                self.flag_background = inp_value
            elif (inp_name.lower() == 'flag_blackwhite'):
                self.flag_blackwhite = inp_value

            # 連携情報
            elif (inp_name.lower() == 'dspstretch'):
                self.dspStretch = inp_value
            elif (inp_name.lower() == 'dsprotate'):
                self.dspRotate = inp_value
            elif (inp_name.lower() == 'dspzoom'):
                self.dspZoom = inp_value

            # 画像受取
            elif (inp_name.lower() != ''):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # シャッター画像
                if (inp_name.lower() == '[shutter]'):
                    try:
                        image_img = inp_value.copy()
                        shutter_time = time.time()
                        shutter_img  = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))
                    except:
                        print(inp_name.lower() + ' error!')

                # カメラ１（メイン画像）
                if (inp_name.lower() == '[img]') \
                or (inp_name.lower() == '[cam1]'):
                    try:
                        image_img = inp_value.copy()
                        cam1_time = time.time()
                        cam1_base = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))

                        if (cam1_fps != ''):
                            puttext = 'Cam1: ' + cam1_fps + 'fps'
                            cv2.putText(image_img, puttext, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                        if (cam1_reso != ''):
                            puttext = cam1_reso
                            cv2.putText(image_img, puttext, (200,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        cam1_mini   = cv2.resize(image_img, (work_width, work_height))

                    except:
                        print(inp_name.lower() + ' error!')

                if (inp_name.lower() == 'cam1_fps'):
                    cam1_fps  = inp_value
                if (inp_name.lower() == 'cam1_reso'):
                    cam1_reso = inp_value

                # カメラ２（ワイプ画像）
                if (inp_name.lower() == '[cam2]'):
                    try:
                        image_img = inp_value.copy()
                        cam2_time = time.time()
                        cam2_base = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))

                        if (cam2_fps != ''):
                            puttext = 'Cam2: ' + cam2_fps + 'fps'
                            cv2.putText(image_img, puttext, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                        if (cam2_reso != ''):
                            puttext = cam2_reso
                            cv2.putText(image_img, puttext, (200,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        cam2_mini   = cv2.resize(image_img, (work_width, work_height))

                    except:
                        print(inp_name.lower() + ' error!')

                if (inp_name.lower() == 'cam2_fps'):
                    cam2_fps  = inp_value
                if (inp_name.lower() == 'cam2_reso'):
                    cam2_reso = inp_value

                # 演算画像
                if (inp_name.lower() == '[comp]'):
                    try:
                        image_img = inp_value.copy()
                        comp_time = time.time()
                        comp_base = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))

                        puttext = 'comp: '
                        cv2.putText(image_img, puttext, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                        if (comp_fps != ''):
                            puttext = 'comp: ' + comp_fps + 'fps'
                            cv2.putText(image_img, puttext, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                        if (comp_reso != ''):
                            puttext = comp_reso
                            cv2.putText(image_img, puttext, (200,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        comp_mini   = cv2.resize(image_img, (work_width, work_height))

                    except:
                        print(inp_name.lower() + ' error!')

                if (inp_name.lower() == 'comp_fps'):
                    comp_fps  = inp_value
                if (inp_name.lower() == 'comp_reso'):
                    comp_reso = inp_value

                # ステータス画像
                if (inp_name.lower() == '[status_img]'):
                    try:
                        image_img = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]
                        while (image_height > int(self.dspHeight * 0.6)):
                            image_img = cv2.resize(image_img, (int(image_width * 0.8), int(image_height * 0.8)))
                            image_height, image_width = image_img.shape[:2]
                        while (image_width > int(self.dspWidth * 0.25)):
                            image_img = cv2.resize(image_img, (int(image_width * 0.5), image_height))
                            image_height, image_width = image_img.shape[:2]

                        status_time = time.time()
                        status_img  = image_img.copy()

                    except:
                        print(inp_name.lower() + ' error!')

                # リーダー画像
                if (inp_name.lower() == '[reader]'):
                    try:
                        image_img   = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        reader_time = time.time()
                        reader_img  = cv2.resize(image_img, (work_width, work_height))
                    except:
                        print(inp_name.lower() + ' error!')

                # 認識画像
                if (inp_name.lower() == '[cvdetect]') \
                or (inp_name.lower() == '[cvdetect1]'):
                    try:
                        image_img      = inp_value.copy()
                        cvdetect1_time = time.time()
                        cvdetect1_base = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))
                    except:
                        print(inp_name.lower() + ' error!')

                if (inp_name.lower() == '[cvdetect2]'):
                    try:
                        image_img      = inp_value.copy()
                        cvdetect2_time = time.time()
                        cvdetect2_base = cv2.resize(image_img, (self.dspWidth, self.dspHeight ))
                    except:
                        print(inp_name.lower() + ' error!')

                # 認識画像
                if (inp_name.lower() == '[detect]') \
                or (inp_name.lower() == '[detect1]'):
                    try:
                        image_img = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        detect1_time = time.time()
                        detect1_img  = cv2.resize(image_img, (work_width, work_height))
                    except:
                        print(inp_name.lower() + ' error!')

                if (inp_name.lower() == '[detect2]'):
                    try:
                        image_img = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.25)
                        work_height = int(work_width * image_height / image_width)
                        detect2_time = time.time()
                        detect2_img  = cv2.resize(image_img, (work_width, work_height))
                    except:
                        print(inp_name.lower() + ' error!')

                # 配列画像
                if (inp_name.lower() == '[array]'):
                    try:
                        image_img = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]
                        work_width  = int(self.dspWidth * 0.07)
                        work_height = int(work_width * image_height / image_width)

                        for i in range(2, ary_max+1):
                            ary_time[i-1] = ary_time[i]
                            if (not ary_img[i] is None):
                                ary_img[i-1]  = ary_img[i].copy()
                            ary_img[i]    = None
                                
                        ary_time[ary_max] = time.time()
                        ary_img[ary_max]  = cv2.resize(image_img, (work_width, work_height))

                    except:
                        print(inp_name.lower() + ' error!')

                # テキスト画像
                if (inp_name.lower() == '[txts_img]') \
                or (inp_name.lower() == '[message_img]'):
                    try:
                        image_img = inp_value.copy()
                        image_height, image_width = image_img.shape[:2]

                        while (image_height > int(self.dspHeight * 0.6)):
                            image_img = cv2.resize(image_img, (int(image_width * 0.8), int(image_height * 0.8)))
                            image_height, image_width = image_img.shape[:2]

                        while (image_width > int(self.dspWidth * 0.7)):
                            image_img = cv2.resize(image_img, (int(image_width * 0.8), image_height))
                            image_height, image_width = image_img.shape[:2]

                        for i in range(2, txt_max+1):
                            txt_time[i-1] = txt_time[i]
                            if (not txt_img[i] is None):
                                txt_img[i-1]  = txt_img[i].copy()
                            txt_img[i]    = None
                                
                        txt_time[txt_max] = time.time()
                        txt_img[txt_max]  = image_img.copy()

                    except:
                        print(inp_name.lower() + ' error!')

                # メッセージ画像のフィードバック
                if (inp_name.lower() == '[message_img]'):
                    image_img = inp_value.copy()
                    if (not cam1_base is None):
                        cam1_height, cam1_width = cam1_base.shape[:2]
                        image_height, image_width = image_img.shape[:2]

                        work_img = cam1_base.copy()
                        work_height, work_width = work_img.shape[:2]
                        msg_img  = image_img.copy()
                        msg_height, msg_width   = msg_img.shape[:2]

                        if (image_width > (cam1_width-40)):
                            work_width  = int(image_width * 1.5)
                            work_height = int(work_width * cam1_height / cam1_width)
                            work_img  = cv2.resize(cam1_base, (work_width, work_height))
                        else:
                            if (image_width < (cam1_width * 0.7)):
                                msg_width  = int(cam1_width * 0.7)
                                msg_height = int(msg_width * image_height / image_width)
                                if (msg_height > (cam1_height * 0.2)):
                                    msg_width  = int(msg_width / (msg_height / (cam1_height * 0.2)))
                                    msg_height = int(msg_width * image_height / image_width)
                                msg_img  = cv2.resize(image_img, (msg_width, msg_height))

                        over_x = 20
                        over_y = work_height - 40 - msg_height
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + msg_width) < work_width) \
                        and ((over_y + msg_height) < work_height):
                            source_img = work_img[over_y:over_y+msg_height, over_x:over_x+msg_width]
                            if (self.flag_blackwhite == 'white'):
                                alpha_img  = cv2.addWeighted(source_img, 0.4, msg_img, 0.6, 0.0)
                            else:
                                alpha_img  = cv2.addWeighted(source_img, 0.2, msg_img, 0.8, 0.0)
                            work_img[over_y:over_y+msg_height, over_x:over_x+msg_width] = alpha_img

                            # 結果出力
                            out_name  = '[photo_img]'
                            out_value = work_img.copy()
                            cn_s.put([out_name, out_value])

            # 画像処理
            if ((inp_name.lower() == '[img]') \
            or  (inp_name.lower() == '[cam1]')) \
            and (cn_s.qsize() == 0):

                display_mode = 'cam'
                if (self.runMode == 'debug'):
                    display_mode = 'dbg'
                elif (self.runMode == 'hud'):
                    display_mode = 'hud'
                if  (qFunc.busyCheck(qBusy_v_rec , 0) == 'busy'):
                    display_mode = 'rec'

                base_base    = None
                base_time    = time.time()
                base_txt1    = ''
                base_txt2    = ''
                wipe_mini1   = None
                wipe_time1   = time.time()
                wipe_mini2   = None
                wipe_time2   = time.time()
                wipe_mini3   = None
                wipe_time3   = time.time()
                wipe_mini4   = None
                wipe_time4   = time.time()

                if (display_mode == 'dbg'):
                    if (not comp_base is None):
                        base_base  = comp_base.copy()
                        base_time  = comp_time
                        if (comp_fps != ''):
                            base_txt1  = comp_fps + 'fps'
                        if (comp_reso != ''):
                            base_txt2  = comp_reso
                    if (not cam1_mini is None):
                        wipe_mini1 = cam1_mini.copy()
                        wipe_time1 = cam1_time
                    if (not cam2_mini is None):
                        wipe_mini2 = cam2_mini.copy()
                        wipe_time2 = cam2_time

                if (display_mode == 'rec'):
                    if (not cam1_base is None):
                        base_base  = cam1_base.copy()
                        base_time  = cam1_time
                        if (cam1_fps != ''):
                            base_txt1  = cam1_fps + 'fps'
                        if (cam1_reso != ''):
                            base_txt2  = cam1_reso

                if (display_mode == 'cam'):
                    if (not cam1_base is None):
                        base_base  = cam1_base.copy()
                        base_time  = cam1_time
                        if (cam1_fps != ''):
                            base_txt1  = cam1_fps + 'fps'
                        if (cam1_reso != ''):
                            base_txt2  = cam1_reso
                    if (not cam2_mini is None):
                        wipe_mini1 = cam2_mini.copy()
                        wipe_time1 = cam2_time
                    if (not comp_mini is None):
                        wipe_mini2 = comp_mini.copy()
                        wipe_time2 = comp_time

                if (display_mode == 'hud'):
                    if (not comp_base is None):
                        base_base  = self.black_img.copy()
                        base_time  = time.time()
                    if (not cam1_mini is None):
                        wipe_mini3 = cam1_mini.copy()
                        wipe_time3 = cam1_time
                    if (not cam2_mini is None):
                        wipe_mini4 = cam2_mini.copy()
                        wipe_time4 = cam2_time

                if (display_mode != 'rec'):
                    if (self.flag_background == 'off'):
                        if (self.flag_blackwhite != 'white'):
                            base_base  = self.black_img.copy()
                        else:
                            base_base  = self.white_img.copy()
                        wipe_mini1 = None
                        wipe_mini2 = None

                # ベース画像
                if (int(time.time() - base_time) <= 10):
                    display_img = base_base.copy()
                else:
                    display_img = self.blue_img.copy()
                    
                # 左下基準
                if (self.flag_enter != 'on') and (self.flag_cancel != 'on'):
                    over_y = self.dspHeight - 70
                else:
                    over_y = self.dspHeight - 140
                over_x  = 20
                over_y2 = over_y
                over_x2 = over_x

                if (display_mode != 'rec'):

                    # ワイプ画像１ overlay
                    if (int(time.time() - wipe_time1) <= 5) and (not wipe_mini1 is None):
                        over_img = wipe_mini1.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_y -= over_height
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y  -= 10
                            over_x2  = over_x + over_width + 10
                        else:
                            over_y += over_height

                    # ワイプ画像２ overlay
                    if (int(time.time() - wipe_time2) <= 5) and (not wipe_mini2 is None):
                        over_img = wipe_mini2.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_y -= over_height
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_x2  = over_x + over_width + 10
                        else:
                            over_y += over_height

                    over_y = over_y2
                    over_x = over_x2

                    # 配列画像 overlay
                    for i in range(1, ary_max+1):
                        if (int(time.time() - ary_time[i]) <= 10) and (not ary_img[i] is None):
                            over_img = ary_img[i].copy()
                            over_height, over_width = over_img.shape[:2]

                            over_y -= over_height
                            if  (over_x >=0) and (over_y >=0) \
                            and ((over_x + over_width) < self.dspWidth) \
                            and ((over_y + over_height) < self.dspHeight):
                                display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                                cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                                over_x += over_width + 10
                            over_y += over_height

                # 右上基準
                over_y  = 70
                over_x  = self.dspWidth - int(self.dspWidth * 0.10)
                over_y2 = over_y
                over_x2 = over_x

                if (display_mode != 'rec'):

                    # ワイプ画像３ overlay
                    if (int(time.time() - wipe_time3) <= 5) and (not wipe_mini3 is None):
                        over_img = wipe_mini3.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y += over_height + 10
                            over_x2 = over_x - 10
                        over_x += over_width                        

                    # ワイプ画像４ overlay
                    if (int(time.time() - wipe_time4) <= 5) and (not wipe_mini4 is None):
                        over_img = wipe_mini4.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y += over_height + 10
                            over_x2 = over_x - 10
                        over_x += over_width                        

                    # リーダー画像 overlay
                    if (int(time.time() - reader_time) <= 5) and (not reader_img is None):
                        over_img = reader_img.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y += over_height + 10
                            over_x2 = over_x - 10
                        over_x += over_width

                    over_y = over_y2
                    over_x = over_x2

                    # 認識画像(1) overlay
                    if (int(time.time() - detect1_time) <= 5) and (not detect1_img is None):
                        over_img = detect1_img.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y += over_height + 20
                        over_x += over_width

                    # 認識画像(2) overlay
                    if (int(time.time() - detect2_time) <= 5) and (not detect2_img is None):
                        over_img = detect2_img.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                            cv2.rectangle(display_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)
                            over_y += over_height + 20
                        over_x += over_width

                # 左上基準
                over_y = 70
                over_x = int(self.dspWidth * 0.05)

                # テキスト画像 alpha blending
                for i in range(1, txt_max+1):
                    if (int(time.time() - txt_time[i]) <= 10) and (not txt_img[i] is None):
                        over_img = txt_img[i].copy()
                        over_height, over_width = over_img.shape[:2]

                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            source_img = display_img[over_y:over_y+over_height, over_x:over_x+over_width]
                            if (self.flag_blackwhite == 'white'):
                                alpha_img  = cv2.addWeighted(source_img, 0.4, over_img, 0.6, 0.0)
                            else:
                                alpha_img  = cv2.addWeighted(source_img, 0.2, over_img, 0.8, 0.0)
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = alpha_img
                            over_y += over_height + 10

                # 右下基準
                if (self.flag_enter != 'on') and (self.flag_cancel != 'on'):
                    over_y = self.dspHeight - 70
                else:
                    over_y = self.dspHeight - 140
                over_x = self.dspWidth - 10

                # 台形補正
                if (int(self.dspStretch) != 0):
                    x = int((self.dspWidth/2) * abs(int(self.dspStretch))/100)
                    if (int(self.dspStretch) > 0):
                        perspective1 = np.float32([ [x, 0], [self.dspWidth-x, 0], [self.dspWidth, self.dspHeight], [0, self.dspHeight] ])
                    else:
                        perspective1 = np.float32([ [0, 0], [self.dspWidth, 0], [self.dspWidth-x, self.dspHeight], [x, self.dspHeight] ])
                    perspective2 = np.float32([ [0, 0], [self.dspWidth, 0], [self.dspWidth, self.dspHeight], [0, self.dspHeight] ])
                    transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                    display_img = cv2.warpPerspective(display_img, transform_matrix, (self.dspWidth, self.dspHeight))

                # 回転
                if   (int(self.dspRotate) == -180):
                    display_img = cv2.flip(display_img, 0) # 180 Rotation Y
                elif (int(self.dspRotate) == -360):
                    display_img = cv2.flip(display_img, 1) # 180 Rotation X
                elif (abs(int(self.dspRotate)) !=   0):
                    width2      = int((self.dspWidth - self.dspHeight)/2)
                    rect_img    = cv2.resize(display_img[0:self.dspHeight, width2:width2+self.dspHeight], (960, 960))
                    rect_mat    = cv2.getRotationMatrix2D((480, 480), -int(self.dspRotate), 1.0)
                    rect_r      = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                    display_img = cv2.resize(rect_r, (self.dspWidth, self.dspHeight))

                # ズーム
                if (float(self.dspZoom) != 1):
                    zm = float(self.dspZoom)
                    x1 = int((self.dspWidth-(self.dspWidth/zm))/2)
                    x2 = self.dspWidth - x1
                    y1 = int((self.dspHeight-(self.dspHeight/zm))/2)
                    y2 = self.dspHeight - y1
                    zm_img = display_img[y1:y2, x1:x2]
                    display_img = cv2.resize(zm_img, (self.dspWidth, self.dspHeight))

                # 入力 ZOOM 表示
                if (self.flag_background == 'on'):
                    if (self.flag_camzoom == 'on'):
                        cv2.putText(display_img, 'RESET', (35,57), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (  0,255,  0))
                        cv2.rectangle(display_img,(35,40),(115,60), (  0,255,  0),1)
                        cv2.putText(display_img, 'ZOOM', (145,57), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,  0))
                        cv2.rectangle(display_img,(135,40),(215,60),(255,255,  0),1)

                # 出力 ZOOM 表示
                if (self.flag_background == 'on'):
                    if (self.flag_dspzoom == 'on'):
                        cv2.putText(display_img, 'RESET', (self.dspWidth-230,57), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (  0,255,  0))
                        cv2.rectangle(display_img,(self.dspWidth-230,40),(self.dspWidth-150,60),(  0,255,  0),1)
                        cv2.putText(display_img, 'ZOOM', (self.dspWidth-120,57),  cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,  0))
                        cv2.rectangle(display_img,(self.dspWidth-130,40),(self.dspWidth-50,60), (255,255,  0),1)

                # ステータス画像 alpha blending
                if (int(time.time() - status_time) <= 30) and (not status_img is None):
                        over_img = status_img.copy()
                        over_height, over_width = over_img.shape[:2]

                        over_y -= over_height
                        over_x -= over_width
                        if  (over_x >=0) and (over_y >=0) \
                        and ((over_x + over_width) < self.dspWidth) \
                        and ((over_y + over_height) < self.dspHeight):
                            source_img = display_img[over_y:over_y+over_height, over_x:over_x+over_width]
                            if (self.flag_blackwhite == 'white'):
                                alpha_img  = cv2.addWeighted(source_img, 0.4, over_img, 0.6, 0.0)
                            else:
                                alpha_img  = cv2.addWeighted(source_img, 0.2, over_img, 0.8, 0.0)
                            display_img[over_y:over_y+over_height, over_x:over_x+over_width] = alpha_img

                # ENTER 表示
                if (self.flag_background == 'on'):
                    if (self.flag_enter == 'on'):
                        cv2.putText(display_img, 'ENTER', (self.dspWidth-260,self.dspHeight-55), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255))
                        cv2.rectangle(display_img,(self.dspWidth-265,self.dspHeight-105),(self.dspWidth-35,self.dspHeight-50),(255,255,255),2)

                # CANCEL 表示
                if (self.flag_background == 'on'):
                    if (self.flag_cancel == 'on'):
                        cv2.putText(display_img, 'CANCEL', (40,self.dspHeight-55), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255))
                        cv2.rectangle(display_img,(35,self.dspHeight-105),(300,self.dspHeight-50),(0,0,255),2)

                # 入力ＦＰＳ overlay
                puttext = display_mode + ':'
                cv2.putText(display_img, puttext, ( 20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                if (base_txt1 != ''):
                    cv2.putText(display_img, base_txt1, (100,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                if (base_txt2 != ''):
                    cv2.putText(display_img, base_txt2, (200,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                # 出力ＦＰＳ overlay
                fps = qFPS_class.get()
                if (base_txt1 != ''):
                    puttext = 'Dsp: ' + '{:.1f}'.format(fps) + 'fps'
                    if (float(self.dspZoom) == 1):
                        cv2.putText(display_img, puttext, ( self.dspWidth - 300,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                    else:
                        cv2.putText(display_img, puttext, ( self.dspWidth - 430,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
                if (base_txt2 != ''):
                    puttext = str(self.dspWidth) + 'x' + str(self.dspHeight)
                    if (float(self.dspZoom) == 1):
                        cv2.putText(display_img, puttext, (self.dspWidth - 130,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                    else:
                        puttext += ' (Zoom=' + self.dspZoom + ')'
                        cv2.putText(display_img, puttext, (self.dspWidth - 260,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))

                # シャッターイメージ
                if (int(time.time() - shutter_time) <= 5) and (not shutter_img is None):
                    display_img = shutter_img.copy()

                # 結果出力
                self.out_img = display_img.copy()
                out_name  = '[img]'
                out_value = self.out_img
                cn_s.put([out_name, out_value])



            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_dsp, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.10)
            else:
                time.sleep(0.02)



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
    


    def check_mouse_click(self, DisplayEvent, MousePointX, MousePointY, ):
        # R-CLICK
        if (DisplayEvent == cv2.EVENT_RBUTTONDOWN):
            return 'r-click', 'r'
        # L-CLICK
        if (DisplayEvent == cv2.EVENT_LBUTTONUP):
            # ENTER,CANCEL
            if ((not MousePointX is None) and (not MousePointY is None)):
                if   (MousePointY < 80):
                    if   (self.flag_camzoom == 'on') \
                    and  (MousePointX >= 0) and (MousePointX <= 125):
                        return 'l-click', 'camzoom-reset'
                    elif (self.flag_camzoom == 'on') \
                    and  (MousePointX > 125) and (MousePointX <= 250):
                        return 'l-click', 'camzoom-zoom'
                    elif (self.flag_dspzoom == 'on') \
                    and  (MousePointX >= self.dspWidth - 250) and (MousePointX <= self.dspWidth - 125):
                        return 'l-click', 'dspzoom-reset'
                    elif (self.flag_dspzoom == 'on') \
                    and  (MousePointX > self.dspWidth -125):
                        return 'l-click', 'dspzoom-zoom'
                    else:
                        return 'l-click', 'l'
                elif (MousePointY >= 80) \
                and  (MousePointY <= self.dspHeight-150):
                        return 'l-click', 'l'
                elif (MousePointY >  self.dspHeight-150):
                    if   (self.flag_cancel == 'on') \
                    and  (MousePointX >= 0) and (MousePointX <= 350):
                        return 'l-click', 'cancel'
                    elif (self.flag_enter == 'on') \
                    and  (MousePointX >= self.dspWidth - 350) and (MousePointX <= self.dspWidth):
                        return 'l-click', 'enter'
                    else:
                        return 'l-click', 'l'
        # OTHER
        return '', ''



DisplayEvent = None
MousePointX  = None
MousePointY  = None
def DisplayMouseEvent(event, x, y, flags, param):
    global DisplayEvent, MousePointX, MousePointY
    if (event == cv2.EVENT_LBUTTONUP):
        DisplayEvent = cv2.EVENT_LBUTTONUP
        MousePointX  = x
        MousePointY  = y
    elif (event == cv2.EVENT_RBUTTONDOWN):
        DisplayEvent = cv2.EVENT_RBUTTONDOWN
        MousePointX  = x
        MousePointY  = y



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)



    overlay_thread = proc_overlay('overlay', '00', )
    overlay_thread.start()

    cam1   = cv2.imread('_photos/_photo_cv.jpg')
    cam2   = cv2.imread('_photos/_photo_ocr_meter.jpg')
    comp   = cv2.imread('_photos/_photo_face.jpg')
    reader = cv2.imread('_photos/_photo_qrcode.jpg')
    detect = cv2.imread('_photos/_photo_face.jpg')
    txt    = cv2.imread('_photos/_photo_ocr_doc.jpg')

    overlay_thread.put(['flag_camzoom', 'on'      ])
    overlay_thread.put(['flag_dspzoom', 'on'      ])
    overlay_thread.put(['flag_enter',   'on'      ])
    overlay_thread.put(['flag_cancel',  'on'      ])
    overlay_thread.put(['[cam1]',   cam1.copy()   ])
    overlay_thread.put(['[cam2]',   cam2.copy()   ])
    overlay_thread.put(['[comp]',   comp.copy()   ])
    overlay_thread.put(['[reader]', reader.copy() ])
    overlay_thread.put(['[detect]', detect.copy() ])

    overlay_thread.put(['[array]',  cam1.copy()   ])
    overlay_thread.put(['[txt]',    txt.copy()    ])
    time.sleep(0.5)
    overlay_thread.put(['[array]',  cam2.copy()   ])
    overlay_thread.put(['[txt]',    txt.copy()    ])
    time.sleep(0.5)
    overlay_thread.put(['[array]',  reader.copy() ])
    time.sleep(0.5)
    overlay_thread.put(['[array]',  detect.copy() ])

    show_onece = True
    while (True):

        mouse1 = ''
        mouse2 = ''

        res_data  = overlay_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        while (res_name != '') and (mouse1 == ''):
            if (res_name == '[img]'):
                display_img = res_value.copy()

                # 初回表示
                if (show_onece == True):
                    cv2.imshow('Display', display_img )
                    cv2.setMouseCallback('Display', DisplayMouseEvent)
                    show_onece = False

                # キーボード操作検査(1)
                if (cv2.waitKey(1) >= 0):
                    qFunc.logOutput('key accept !', )
                    #break

                # マウス操作検査
                mouse1 = ''
                mouse2 = ''
                if (cv2.getWindowProperty('Display', 0) < 0):
                    # CLOSE
                    mouse1 = 'close'
                    mouse2 = 'close'
                    qFunc.logOutput(mouse1 + ', ' + mouse2 )
                    show_onece = True
                    break

                else:
                    # CLICK
                    mouse1, mouse2 = overlay_thread.check_mouse_click(DisplayEvent, MousePointX, MousePointY, )
                    DisplayEvent = None
                    MousePointX  = None
                    MousePointY  = None
                    if (mouse1 !=''):
                        qFunc.logOutput(mouse1 + ', ' + mouse2 )
                        break

                # 画面出力
                cv2.imshow('Display', display_img )

                # キーボード操作検査(2)
                if (cv2.waitKey(1) >= 0):
                    qFunc.logOutput('key accept !', )
                    #break

        if (mouse2 == 'enter') \
        or (mouse2 == 'cancel') \
        or (mouse2 == 'close'):
            break

        if (overlay_thread.proc_s.qsize() == 0):
            overlay_thread.put(['[cam1]', cam1.copy() ])

        time.sleep(0.01)

    time.sleep(1.00)
    overlay_thread.stop()
    del overlay_thread



    cv2.destroyAllWindows()


