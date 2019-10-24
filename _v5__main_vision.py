#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
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

import numpy as np
import cv2

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)


# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_vision

qCtrl_recognize          = 'temp/result_recognize.txt'
qCtrl_translate          = 'temp/result_translate.txt'

# 出力インターフェース
qCtrl_result_photo       = 'temp/result_photo.jpg'
qCtrl_result_screen      = 'temp/result_screen.jpg'
qCtrl_result_vision      = 'temp/result_vision.txt'
qCtrl_result_cv          = 'temp/result_cv.txt'
qCtrl_result_cv_sjis     = 'temp/result_cv_sjis.txt'
qCtrl_result_ocr         = 'temp/result_ocr.txt'
qCtrl_result_ocr_sjis    = 'temp/result_ocr_sjis.txt'
qCtrl_result_ocrTrn      = 'temp/result_ocr_translate.txt'
qCtrl_result_ocrTrn_sjis = 'temp/result_ocr_translate_sjis.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS             = qFunc.getValue('qOS'            )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
qPath_cache     = qFunc.getValue('qPath_cache'    )
qPath_sounds    = qFunc.getValue('qPath_sounds'   )
qPath_fonts     = qFunc.getValue('qPath_fonts'    )
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
qBusy_dev_scn   = qFunc.getValue('qBusy_dev_scn'  )
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
qBusy_d_upload  = qFunc.getValue('qBusy_d_upload' )
qRdy__s_force   = qFunc.getValue('qRdy__s_force'  )
qRdy__s_fproc   = qFunc.getValue('qRdy__s_fproc'  )
qRdy__s_sendkey = qFunc.getValue('qRdy__s_sendkey')
qRdy__v_reader  = qFunc.getValue('qRdy__v_reader' )
qRdy__v_sendkey = qFunc.getValue('qRdy__v_sendkey')
qRdy__d_reader  = qFunc.getValue('qRdy__d_reader' )
qRdy__d_sendkey = qFunc.getValue('qRdy__d_sendkey')

# thread ルーチン群
import _v5_proc_controlv
import _v5_proc_overlay
import _v5_proc_camera
import _v5_proc_txt2img
import _v5_proc_cvreader
import _v5_proc_cvdetect
import _v5_proc_cv2dnn_yolo
import _v5_proc_cv2dnn_ssd
import _v5_proc_vin2jpg
import _v5_proc_coreCV



if getattr(sys, 'frozen', False):
    #print('exe')
    google = False
else:
    #print('python')
    google = True

runMode    = 'hud'

if (google == True):
    qApiCV     = 'google'
    qApiOCR    = qApiCV
    qApiTrn    = 'free'
else:
    qApiCV     = 'azure'
    qApiOCR    = qApiCV
    qApiTrn    = 'azure'
qLangCV    = 'ja'
qLangOCR   = qLangCV
qLangTrn   = 'en'



class main_vision:

    def __init__(self, name='thread', id='0', 
                                runMode='debug',
                                cam1Dev='0', cam1Mode='vga', cam1Stretch='0', cam1Rotate='0', cam1Zoom='1.0',
                                cam2Dev='none', cam2Mode='vga', cam2Stretch='0', cam2Rotate='0', cam2Zoom='1.0',
                                dspMode='vga', dspStretch='0', dspRotate='0', dspZoom='1.0',
                                codeRead='qr', casName1='face', casName2='car',
                                qApiCV='google', qApiOCR='google', qApiTrn='free',
                                qLangCV='ja', qLangOCR='ja', qLangTrn='en',
                                ):
        self.runMode     = runMode
        self.cam1Dev     = cam1Dev
        self.cam1Dev_org = cam1Dev
        self.cam1Mode    = cam1Mode
        self.cam1Stretch = cam1Stretch
        self.cam1Rotate  = cam1Rotate
        self.cam1Zoom    = cam1Zoom
        self.cam2Dev     = cam2Dev
        self.cam2Dev_org = cam2Dev
        self.cam2Mode    = cam2Mode
        self.cam2Stretch = cam2Stretch
        self.cam2Rotate  = cam2Rotate
        self.cam2Zoom    = cam2Zoom
        self.dspMode     = dspMode
        self.dspStretch  = dspStretch
        self.dspRotate   = dspRotate
        self.dspZoom     = dspZoom

        self.codeRead    = codeRead
        self.casName1    = casName1
        self.casName2    = casName2
        self.qApiCV      = qApiCV
        self.qApiOCR     = qApiOCR
        self.qApiTrn     = qApiTrn
        self.qLangCV     = qLangCV
        self.qLangOCR    = qLangOCR
        self.qLangTrn    = qLangTrn

        dspWidth, dspHeight = qFunc.getResolution(dspMode)
        self.dspWidth  = dspWidth
        self.dspHeight = dspHeight

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_' + str(id)
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
        self.flag_camzoom    = 'off'
        self.flag_dspzoom    = 'off'
        self.flag_enter      = 'off'
        self.flag_cancel     = 'off'
        self.flag_background = 'on'
        self.flag_blackwhite = 'black'

        if   (self.runMode == 'debug'):
            self.flag_camzoom    = 'on'
            self.flag_dspzoom    = 'on'
            self.flag_enter      = 'on'
            self.flag_cancel     = 'on'
        elif (self.runMode == 'hud'):
            self.flag_blackwhite = 'white'
        elif (self.runMode == 'handsfree'):
            self.flag_camzoom    = 'on'
            self.flag_dspzoom    = 'on'
        elif (self.runMode == 'camera'):
            self.flag_camzoom    = 'on'
            self.flag_enter      = 'on'
            self.flag_cancel     = 'on'
        elif (self.runMode == 'background'):
            self.flag_camzoom    = 'on'
            self.flag_enter      = 'on'
            self.flag_cancel     = 'on'

    def __del__(self, ):
        qFunc.logOutput(self.proc_id + ':bye!', display=self.logDisp, )

    def begin(self, ):
        #qFunc.logOutput(self.proc_id + ':start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.statusSet(self.fileRun, False)
        qFunc.statusSet(self.fileRdy, False)
        qFunc.statusSet(self.fileBsy, False)

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ))
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0

        self.proc_main.setDaemon(True)
        self.proc_main.start()

    def abort(self, waitMax=20, ):
        qFunc.logOutput(self.proc_id + ':stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (not self.proc_beat is None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)
        chktime = time.time()
        while (os.path.exists(self.fileRun)) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)

    def put(self, data, ):
        self.proc_s.put(data)
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and ((time.time() - chktime) < waitMax):
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
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        # 起動条件
        controlv_thread    = None
        controlv_switch    = 'on'
        overlay_thread     = None
        overlay_switch     = 'on'
        camera_thread1     = None
        camera_switch1     = 'on'
        camera_thread2     = None
        camera_switch2     = 'on'
        txt2img_thread     = None
        txt2img_switch     = 'on'
        cvreader_thread    = None
        cvreader_switch    = 'on'
        cvdetect_thread1   = None
        cvdetect_switch1   = 'on'
        cvdetect_thread2   = None
        cvdetect_switch2   = 'on'
        cv2dnn_yolo_thread = None
        cv2dnn_yolo_switch = 'on'
        cv2dnn_ssd_max     = 2
        cv2dnn_ssd_seq     = 0
        cv2dnn_ssd_thread  = {}
        cv2dnn_ssd_switch  = 'on'
        for i in range(cv2dnn_ssd_max):
            cv2dnn_ssd_thread[i] = None
        vin2jpg_thread     = None
        vin2jpg_switch     = 'on'
        coreCV_thread      = None
        coreCV_switch      = 'on'

        if (self.runMode == 'debug'):
            camera_switch2     = 'on'
            txt2img_switch     = 'on'
            cvreader_switch    = 'on'
            cvdetect_switch1   = 'on'
            cvdetect_switch2   = 'on'
            cv2dnn_yolo_switch = 'on'
            cv2dnn_ssd_switch  = 'on'
            vin2jpg_switch     = 'on'
            coreCV_switch      = 'on'
        elif (self.runMode == 'hud'):
            camera_switch2     = 'off'
            txt2img_switch     = 'on'
            cvreader_switch    = 'on'
            cvdetect_switch1   = 'off'
            cvdetect_switch2   = 'off'
            cv2dnn_yolo_switch = 'off'
            cv2dnn_ssd_switch  = 'off'
            vin2jpg_switch     = 'off'
            coreCV_switch      = 'off'
        elif (self.runMode == 'handsfree'):
            camera_switch2     = 'on'
            txt2img_switch     = 'on'
            cvreader_switch    = 'on'
            cvdetect_switch1   = 'off'
            cvdetect_switch2   = 'off'
            cv2dnn_yolo_switch = 'on'
            cv2dnn_ssd_switch  = 'off'
            if (qHOSTNAME == 'kondou-s10'):
                cv2dnn_yolo_switch  = 'off'
                cv2dnn_ssd_switch   = 'on'
            vin2jpg_switch     = 'on'
            coreCV_switch      = 'on'
        elif (self.runMode == 'camera'):
            camera_switch2     = 'off'
            txt2img_switch     = 'on'
            cvreader_switch    = 'on'
            cvdetect_switch1   = 'off'
            cvdetect_switch2   = 'off'
            cv2dnn_yolo_switch = 'off'
            cv2dnn_ssd_switch  = 'off'
            vin2jpg_switch     = 'off'
            coreCV_switch      = 'off'
        elif (self.runMode == 'background'):
            camera_switch2     = 'off'
            txt2img_switch     = 'on'
            cvreader_switch    = 'on'
            cvdetect_switch1   = 'off'
            cvdetect_switch2   = 'off'
            cv2dnn_yolo_switch = 'off'
            cv2dnn_ssd_switch  = 'off'
            vin2jpg_switch     = 'off'
            coreCV_switch      = 'off'

        if (self.cam2Dev == 'none'):
            camera_switch2     = 'off'

        busy_status_txts = _v5__qFunc.qBusy_status_txts_class()

        # 待機ループ
        self.proc_step = '5'

        cvreader_last_put  = time.time()
        cvdetect1_last_put = time.time()
        cvdetect2_last_put = time.time()
        cv2dnn_last_put    = time.time()

        main_img        = None
        display_img     = None
        message_txts    = None
        message_time    = time.time()
        photo_img       = None
        photo_time      = time.time()

        cam1Stretch     = self.cam1Stretch
        cam1Rotate      = self.cam1Rotate
        cam1Zoom        = self.cam1Zoom
        cam2Stretch     = self.cam2Stretch
        cam2Rotate      = self.cam2Rotate
        cam2Zoom        = self.cam2Zoom
        dspStretch      = self.dspStretch
        dspRotate       = self.dspRotate
        dspZoom         = self.dspZoom

        flag_camzoom    = self.flag_camzoom
        flag_dspzoom    = self.flag_dspzoom
        flag_enter      = self.flag_enter
        flag_cancel     = self.flag_cancel
        flag_background = self.flag_background
        flag_blackwhite = self.flag_blackwhite

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_'):
                    break

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qFunc.logOutput(self.proc_id + ':alive', display=True, )
                last_alive = time.time()

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

            # スレッド設定

            speechs = []

            if (controlv_thread is None) and (controlv_switch == 'on'):
                controlv_thread = _v5_proc_controlv.proc_controlv(
                                    name='controlv', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                controlv_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ制御」の機能が有効になりました。', 'wait':0, })

            if (not controlv_thread is None) and (controlv_switch != 'on'):
                controlv_thread.abort()
                del controlv_thread
                controlv_thread = None

            if (overlay_thread is None) and (overlay_switch == 'on'):
                overlay_thread = _v5_proc_overlay.proc_overlay(
                                    name='overlay', id='0',
                                    runMode=self.runMode,
                                    dspMode=self.dspMode, dspStretch=self.dspStretch, dspRotate=self.dspRotate, dspZoom=self.dspZoom,
                                    )
                overlay_thread.begin()

                overlay_thread.put(['_flag_camzoom_'   , flag_camzoom    ])
                overlay_thread.put(['_flag_dspzoom_'   , flag_dspzoom    ])
                overlay_thread.put(['_flag_enter_'     , flag_enter      ])
                overlay_thread.put(['_flag_cancel_'    , flag_cancel     ])
                overlay_thread.put(['_flag_background_', flag_background ])
                overlay_thread.put(['_flag_blackwhite_', flag_blackwhite ])

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「画面表示」の機能が有効になりました。', 'wait':0, })

            if (not overlay_thread is None) and (overlay_switch != 'on'):
                overlay_thread.abort()
                del overlay_thread
                overlay_thread = None

            if (camera_thread1 is None) and (camera_switch1 == 'on'):
                camera_thread1 = _v5_proc_camera.proc_camera(
                                    name='camera', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev, camMode=self.cam1Mode, camStretch=self.cam1Stretch, camRotate=self.cam1Rotate, camZoom=self.cam1Zoom, camFps='5',
                                    )
                camera_thread1.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ１入力」の機能が有効になりました。', 'wait':0, })

            if (not camera_thread1 is None) and (camera_switch1 != 'on'):
                camera_thread1.abort()
                del camera_thread1
                camera_thread1 = None

            if (camera_thread2 is None) and (camera_switch2 == 'on'):
                camera_thread2 = _v5_proc_camera.proc_camera(
                                    name='camera', id='1',
                                    runMode=self.runMode,
                                    camDev=self.cam2Dev, camMode=self.cam2Mode, camStretch=self.cam2Stretch, camRotate=self.cam2Rotate, camZoom=self.cam2Zoom, camFps='2',
                                    )
                camera_thread2.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ２入力」の機能が有効になりました。', 'wait':0, })

            if (not camera_thread2 is None) and (camera_switch2 != 'on'):
                camera_thread2.abort()
                del camera_thread2
                camera_thread2 = None

            if (txt2img_thread is None) and (txt2img_switch == 'on'):
                txt2img_thread = _v5_proc_txt2img.proc_txt2img(
                                    name='txt2img', id='0',
                                    runMode=self.runMode,
                                    )
                txt2img_thread.begin()

                txt2img_thread.put(['_flag_background_', flag_background ])
                txt2img_thread.put(['_flag_blackwhite_', flag_blackwhite ])

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「認識文字の表示」の機能が有効になりました。', 'wait':0, })

            if (not txt2img_thread is None) and (txt2img_switch != 'on'):
                txt2img_thread.abort()
                del txt2img_thread
                txt2img_thread = None

            if (cvreader_thread is None) and (cvreader_switch == 'on'):
                cvreader_thread = _v5_proc_cvreader.proc_cvreader(
                                    name='reader', id='v',
                                    runMode=self.runMode, 
                                    reader=self.codeRead,
                                    )
                cvreader_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＱＲコード認識」の機能が有効になりました。', 'wait':0, })

            if (not cvreader_thread is None) and (cvreader_switch != 'on'):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (cvdetect_thread1 is None) and (cvdetect_switch1 == 'on'):
                cvdetect_thread1 = _v5_proc_cvdetect.proc_cvdetect(
                                    name='detect', id='0',
                                    runMode=self.runMode, 
                                    casName=self.casName1, procMode='640x480',
                                    )
                cvdetect_thread1.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「オープンＣＶ画像認識」の機能が有効になりました。', 'wait':0, })

            if (not cvdetect_thread1 is None) and (cvdetect_switch1 != 'on'):
                cvdetect_thread1.abort()
                del cvdetect_thread1
                cvdetect_thread1 = None

            if (cvdetect_thread2 is None) and (cvdetect_switch2 == 'on'):
                cvdetect_thread2 = _v5_proc_cvdetect.proc_cvdetect(
                                    name='detect', id='1',
                                    runMode=self.runMode, 
                                    casName=self.casName2, procMode='640x480',
                                    )
                cvdetect_thread2.begin()

            if (not cvdetect_thread2 is None) and (cvdetect_switch2 != 'on'):
                cvdetect_thread2.abort()
                del cvdetect_thread2
                cvdetect_thread2 = None

            if (cv2dnn_yolo_thread is None) and (cv2dnn_yolo_switch == 'on'):
                cv2dnn_yolo_thread = _v5_proc_cv2dnn_yolo.proc_cv2dnn_yolo(
                                    name='cv2_yolo', id='0',
                                    runMode=self.runMode, 
                                    procMode='320x240',
                                    )
                cv2dnn_yolo_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「画像認識（ｙｏｌｏ）」の機能が有効になりました。', 'wait':0, })

            if (not cv2dnn_yolo_thread is None) and (cv2dnn_yolo_switch != 'on'):
                cv2dnn_yolo_thread.abort()
                del cv2dnn_yolo_thread
                cv2dnn_yolo_thread = None

            for i in range(cv2dnn_ssd_max):
                if (cv2dnn_ssd_thread[i] is None) and (cv2dnn_ssd_switch == 'on'):
                    cv2dnn_ssd_thread[i] = _v5_proc_cv2dnn_ssd.proc_cv2dnn_ssd(
                                        name='cv2_ssd', id=str(i),
                                        runMode=self.runMode, 
                                        procMode='320x240',
                                        )
                    cv2dnn_ssd_thread[i].begin()

                    if (i == 0):
                        if (self.runMode == 'debug') \
                        or (self.runMode == 'handsfree'):
                            speechs.append({ 'text':u'「画像認識（ｓｓｄ）」の機能が有効になりました。', 'wait':0, })

            for i in range(cv2dnn_ssd_max):
                if (not cv2dnn_ssd_thread[i] is None) and (cv2dnn_ssd_switch != 'on'):
                    cv2dnn_ssd_thread[i].abort()
                    del cv2dnn_ssd_thread[i]
                    cv2dnn_ssd_thread[i] = None

            if (vin2jpg_thread is None) and (vin2jpg_switch == 'on'):
                vin2jpg_thread = _v5_proc_vin2jpg.proc_vin2jpg(
                                    name='vin2jpg', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                vin2jpg_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「写真認識」の機能が有効になりました。', 'wait':0, })

            if (not vin2jpg_thread is None) and (vin2jpg_switch != 'on'):
                vin2jpg_thread.abort()
                del vin2jpg_thread
                vin2jpg_thread = None

            if (coreCV_thread is None) and (coreCV_switch == 'on'):
                coreCV_thread = _v5_proc_coreCV.proc_coreCV(
                                    name='coreCV', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                coreCV_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＡＩ画像認識」の機能が有効になりました。', 'wait':0, })

            if (not coreCV_thread is None) and (coreCV_switch != 'on'):
                coreCV_thread.abort()
                del coreCV_thread
                coreCV_thread = None

            if (len(speechs) != 0):
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree') \
                or (self.runMode == 'hud') \
                or (self.runMode == 'camera'):
                    speechs = []
                    speechs.append({ 'text':u'「カメラ機能」の準備が完了しました。', 'wait':0, })
                    qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            # レディ設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 動画ファイル処理（バッチ）時の自動終了
            if (not self.cam1Dev.isdigit()):
                if  ((time.time() - camera_thread1.proc_last) > 60):
                    break

            # 制御処理
            control = ''

            if (inp_name.lower() == 'control'):
                control = inp_value.lower()

            else:

                if (not controlv_thread is None):
                    while (controlv_thread.proc_r.qsize() != 0):
                        res_data  = controlv_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == 'control'):
                            control = res_value
                            # 結果出力
                            if (cn_s.qsize() < 99):
                                out_name  = res_name
                                out_value = res_value
                                cn_s.put([out_name, out_value])
                            break

                        if (res_name == '[txts]'):
                            if (not txt2img_thread is None):
                                # 結果出力
                                if (txt2img_thread.proc_s.qsize() < 99):
                                    txt2img_thread.put([res_name, res_value])

                        if (res_name == '[message_txts]'):
                            if (not txt2img_thread is None):
                                message_txts = res_value
                                message_time = time.time()
                                message_img  = None
                                # 結果出力
                                if (txt2img_thread.proc_s.qsize() < 99):
                                    txt2img_thread.put(['[message_txts]', message_txts])

            # カメラ変更１
            if (control == '_camchange_off_'):
                camera_switch1_org = camera_switch1
                camera_switch2_org = camera_switch2
                camera_switch1 = 'off'
                camera_switch2 = 'off'
                if (self.cam1Dev != self.cam1Dev_org) \
                or (self.cam2Dev != self.cam2Dev_org):
                    self.cam1Dev = self.cam1Dev_org
                    self.cam2Dev = self.cam2Dev_org
                else:
                    # カメラ1,0の場合
                    if ((self.cam1Dev_org == '1') and (self.cam2Dev_org == '0')) \
                    or ((self.cam1Dev_org == '0') and (self.cam2Dev_org == '1')):
                        self.cam1Dev = self.cam2Dev_org
                        self.cam2Dev = self.cam1Dev_org
                    # kondou-s10 カメラ2,1の場合
                    elif (qHOSTNAME == 'kondou-s10') \
                    and ((self.cam1Dev == '2') and (self.cam2Dev == '1')):
                        self.cam1Dev = '0'
                    # surface-go カメラ1,2の場合
                    elif (qHOSTNAME == 'surface-go') \
                    and ((self.cam1Dev == '0') and (self.cam2Dev == '2')):
                        self.cam1Dev = '2'
                        self.cam2Dev = '0'
                    # カメラn,0の場合
                    elif (self.cam1Dev.isdigit()) and (self.cam2Dev == '0'):
                        self.cam1Dev = str(int(self.cam1Dev) - 1)
                    # カメラ0,nの場合
                    elif (self.cam1Dev == '0') and (self.cam2Dev.isdigit()):
                        self.cam1Dev = str(int(self.cam2Dev) - 1)

            # カメラ変更２
            if (control == '_camchange_on_'):
                camera_switch1 = camera_switch1_org
                camera_switch2 = camera_switch2_org

            # リセット
            if (control == '_reset_') \
            or (control == '_camchange_on_'):
                cam1Stretch     = self.cam1Stretch
                cam1Rotate      = self.cam1Rotate
                cam1Zoom        = self.cam1Zoom
                cam2Stretch     = self.cam2Stretch
                cam2Rotate      = self.cam2Rotate
                cam2Zoom        = self.cam2Zoom
                dspStretch      = self.dspStretch
                dspRotate       = self.dspRotate
                dspZoom         = self.dspZoom

                flag_camzoom    = self.flag_camzoom
                flag_dspzoom    = self.flag_dspzoom
                flag_enter      = self.flag_enter
                flag_cancel     = self.flag_cancel
                flag_background = self.flag_background
                flag_blackwhite = self.flag_blackwhite

                if (not camera_thread1 is None):
                    camera_thread1.put(['_camstretch_'     , cam1Stretch     ])
                    camera_thread1.put(['_camrotate_'      , cam1Rotate      ])
                    camera_thread1.put(['_camzoom_'        , cam1Zoom        ])
                if (not camera_thread2 is None):
                    camera_thread2.put(['_camstretch_'     , cam2Stretch     ])
                    camera_thread2.put(['_camrotate_'      , cam2Rotate      ])
                    camera_thread2.put(['_camzoom_'        , cam2Zoom        ])
                if (not overlay_thread is None):
                    overlay_thread.put(['_dspstretch_'     , dspStretch      ])
                    overlay_thread.put(['_dsprotate_'      , dspRotate       ])
                    overlay_thread.put(['_dspzoom_'        , dspZoom         ])
                    overlay_thread.put(['_flag_camzoom_'   , flag_camzoom    ])
                    overlay_thread.put(['_flag_dspzoom_'   , flag_dspzoom    ])
                    overlay_thread.put(['_flag_background_', flag_background ])
                    overlay_thread.put(['_flag_blackwhite_', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['_flag_background_', flag_background ])
                    txt2img_thread.put(['_flag_blackwhite_', flag_blackwhite ])

            # カメラ操作
            if (control == '_zoomout_') or (control == '_camzoom_reset_'):
                cam1Zoom    = '1.0'
                if (not camera_thread1 is None):
                    camera_thread1.put(['_camzoom_', cam1Zoom ])
            if (control == '_zoomin_') or (control == '_camzoom_zoom_'):
                cam1Zoom    = '{:.1f}'.format(float(cam1Zoom) + 0.5)
                if (not camera_thread1 is None):
                    camera_thread1.put(['_camzoom_', cam1Zoom ])
            if (control == '_stretch_'):
                cam1Stretch = str(int(cam1Stretch) + 10)
                if (not camera_thread1 is None):
                    camera_thread1.put(['_camstretch_',  cam1Stretch ])
            if (control == '_rotate_'):
                cam1Rotate  = str(int(cam1Rotate)  + 45)
                if (not camera_thread1 is None):
                    camera_thread1.put(['_camrotate_',   cam1Rotate  ])

            # 表示操作
            if (control == '_dspzoom_reset_'):
                dspZoom    = '1.0'
                if (not overlay_thread is None):
                    overlay_thread.put(['_dspzoom_', dspZoom ])
            if (control == '_dspzoom_zoom_'):
                dspZoom    = '{:.1f}'.format(float(dspZoom) + 0.5)
                if (not overlay_thread is None):
                    overlay_thread.put(['_dspzoom_', dspZoom ])

            # 背景操作
            if (control == '_background_'):
                if   (flag_background == 'on'):
                    flag_background = 'off'
                elif (flag_background == 'off'):
                    flag_background = 'on'
                if (not overlay_thread is None):
                    overlay_thread.put(['_flag_background_', flag_background ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['_flag_background_', flag_background ])
            if (control == '_black_'):
                flag_blackwhite = 'black'
                if (not overlay_thread is None):
                    overlay_thread.put(['_flag_blackwhite_', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['_flag_blackwhite_', flag_blackwhite ])
            if (control == '_white_'):
                flag_blackwhite = 'white'
                if (not overlay_thread is None):
                    overlay_thread.put(['_flag_blackwhite_', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['_flag_blackwhite_', flag_blackwhite ])

            # シャッター
            if (control == '_shutter_'):
                if (qFunc.statusCheck(qBusy_dev_cam) == False):
                    if (not main_img is None):

                        # 撮影ログ
                        logset = False
                        if ((time.time() - photo_time) < 5.00):
                            overlay_thread.put(['[shutter]', photo_img ])
                            overlay_thread.put(['[array]',   photo_img ])
                            logset = True
                        if (logset == False):
                            overlay_thread.put(['[shutter]', main_img ])
                            overlay_thread.put(['[array]',   main_img ])

                        # ＡＩ画像認識処理へ
                        nowTime = datetime.datetime.now()
                        stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                        filename0 = qPath_v_inp + stamp + '.photo.jpg'
                        cv2.imwrite(filename0, main_img)

                        # 写真保存
                        self.save_photo(stamp, main_img, display_img, message_txts, message_time, photo_img, photo_time, )

            if  (cn_s.qsize() == 0) \
            and (overlay_thread.proc_s.qsize() == 0):

                # 画像入力（メインカメラ）
                if (not camera_thread1 is None):
                    while (camera_thread1.proc_r.qsize() != 0):
                        res_data  = camera_thread1.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '_fps_'):
                            overlay_thread.put(['_cam1_fps_', res_value ])
                        if (res_name == '_reso_'):
                            overlay_thread.put(['_cam1_reso_', res_value ])
                        if (res_name == '[img]'):
                            main_img = res_value.copy()

                            if ((qFunc.statusCheck(qBusy_dev_cam) == False) \
                            or  (qFunc.statusCheck(qRdy__v_sendkey) == True)):

                                # 画像識別（ＱＲ）
                                if (not cvreader_thread is None):
                                    if ((time.time() - cvreader_last_put) >= 1):
                                        if (cvreader_thread.proc_s.qsize() == 0):
                                            cvreader_thread.put(['[img]', main_img ])
                                            cvreader_last_put = time.time()

                                # 画像識別（顔等）
                                if (not cvdetect_thread1 is None):
                                    if  ((time.time() - cvdetect1_last_put) >= 1):
                                        if (cvdetect_thread1.proc_s.qsize() == 0):
                                            cvdetect_thread1.put(['[img]', main_img ])
                                            cvdetect1_last_put = time.time()
                                
                                # 画像識別（自動車等）
                                if (not cvdetect_thread2 is None):
                                    if  ((time.time() - cvdetect2_last_put) >= 1):
                                        if (cvdetect_thread2.proc_s.qsize() == 0):
                                            cvdetect_thread2.put(['[img]', main_img ])
                                            cvdetect2_last_put = time.time()

                                # 画像識別（cv2dnn）yolo
                                if (not cv2dnn_yolo_thread is None):
                                    if (cv2dnn_yolo_thread.proc_s.qsize() == 0):
                                        cv2dnn_yolo_thread.put(['[img]', main_img ])
                                        cv2dnn_last_put = time.time()

                                # 画像識別（cv2dnn）ssd
                                i = cv2dnn_ssd_seq
                                if (not cv2dnn_ssd_thread[i] is None):
                                    if ((time.time() - cv2dnn_last_put) >= (0.5/cv2dnn_ssd_max)):
                                        if (cv2dnn_ssd_thread[i].proc_s.qsize() == 0):
                                            cv2dnn_ssd_thread[i].put(['[img]', main_img ])
                                            cv2dnn_last_put = time.time()
                                            cv2dnn_ssd_seq += 1
                                            cv2dnn_ssd_seq = cv2dnn_ssd_seq % cv2dnn_ssd_max
                                            break

                            # 画像合成（メイン画像）
                            overlay_thread.put(['[cam1]', main_img ])

                            break

                # 画像入力（ワイプカメラ）
                if (not camera_thread2 is None):
                    while (camera_thread2.proc_r.qsize() != 0):
                        res_data  = camera_thread2.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '_fps_'):
                            overlay_thread.put(['_cam2_fps_', res_value ])
                        if (res_name == '_reso_'):
                            overlay_thread.put(['_cam2_reso_', res_value ])
                        if (res_name == '[img]'):
                            wipe_img = res_value.copy()

                            # 画像合成（ワイプ画像）
                            overlay_thread.put(['[cam2]', wipe_img ])
                            break

                # 画像合成（ＱＲ　識別結果）
                if (not cvreader_thread is None):
                    while (cvreader_thread.proc_r.qsize() != 0):
                        res_data  = cvreader_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[img]'):
                            reader_img = res_value.copy()
                            overlay_thread.put(['[reader]', reader_img ])
                        if (res_name == '[txts]'):
                            for txt in res_value:
                                qFunc.notePad(txt)
                                if (qFunc.statusCheck(qRdy__v_sendkey) == True):
                                    qFunc.sendKey(txt)

                # 画像合成（顔等　識別結果）
                if (not cvdetect_thread1 is None):
                    while (cvdetect_thread1.proc_r.qsize() != 0):
                        res_data  = cvdetect_thread1.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[img]'):
                            cvdetect_img1 = res_value.copy()
                            overlay_thread.put(['[cvdetect1]', cvdetect_img1 ])
                        if (res_name == '[detect]'):
                            detect_img1 = res_value.copy()
                            overlay_thread.put(['[detect1]', detect_img1 ])
                        if (res_name == '[array]'):
                            ary_img1 = res_value.copy()
                            overlay_thread.put(['[array]', ary_img1 ])

                # 画像合成（自動車等　識別結果）
                if (not cvdetect_thread2 is None):
                    while (cvdetect_thread2.proc_r.qsize() != 0):
                        res_data  = cvdetect_thread2.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[img]'):
                            cvdetect_img2 = res_value.copy()
                            overlay_thread.put(['[cvdetect2]', cvdetect_img2 ])
                        if (res_name == '[detect]'):
                            detect_img2 = res_value.copy()
                            overlay_thread.put(['[detect2]', detect_img2 ])

                # 画像合成（cv2dnn識別結果）yolo
                if (not cv2dnn_yolo_thread is None):
                    while (cv2dnn_yolo_thread.proc_r.qsize() != 0):
                        res_data  = cv2dnn_yolo_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '_fps_'):
                            overlay_thread.put(['_comp_fps_', res_value ])
                        if (res_name == '_reso_'):
                            overlay_thread.put(['_comp_reso_', res_value ])
                        #if (res_name == '[img]'):
                        #    cv2dnn_img = res_value.copy()
                        #    overlay_thread.put(['[comp]', cv2dnn_img ])
                        if (res_name == '[array]'):
                            ary_imgy = res_value.copy()
                            overlay_thread.put(['[array]', ary_imgy ])
                            if (cvdetect_thread1 is None):
                                overlay_thread.put(['[detect1]', ary_imgy ])

                # 画像合成（cv2dnn識別結果）ssd
                for i in range(cv2dnn_ssd_max):
                    if (not cv2dnn_ssd_thread[i] is None):
                        while (cv2dnn_ssd_thread[i].proc_r.qsize() != 0):
                            res_data  = cv2dnn_ssd_thread[i].get()
                            res_name  = res_data[0]
                            res_value = res_data[1]
                            if (res_name == '_fps_'):
                                overlay_thread.put(['_comp_fps_', '{:.2f}'.format(float(res_value) * cv2dnn_ssd_max) ])
                            if (res_name == '_reso_'):
                                overlay_thread.put(['_comp_reso_', res_value ])
                            if (res_name == '[img]'):
                                cv2dnn_img = res_value.copy()
                                overlay_thread.put(['[comp]', cv2dnn_img ])
                            if (res_name == '[array]'):
                                ary_imgy = res_value.copy()
                                overlay_thread.put(['[array]', ary_imgy ])
                                if (cvdetect_thread1 is None):
                                    overlay_thread.put(['[detect1]', ary_imgy ])

                # 画像処理（前処理）
                if (not vin2jpg_thread is None):
                    res_data  = vin2jpg_thread.get()

                # ＡＩ画像認識（クラウド処理）
                if (not coreCV_thread is None):
                    res_data  = coreCV_thread.get()

                # 文字→画像変換
                if (not txt2img_thread is None):

                    # ステータス状況
                    if  (qFunc.statusCheck(qBusy_d_rec) == False) \
                    and ((self.runMode == 'debug') \
                     or  (self.runMode == 'handsfree') \
                     or  (self.runMode == 'hud')):
                        res_txts = busy_status_txts.getAll()
                        if (res_txts != False):
                            txt2img_thread.put(['[status]', res_txts ])
                    else:
                        res_txts = busy_status_txts.getRecorder()
                        if (res_txts != False):
                            txt2img_thread.put(['[status]', res_txts ])

                    # ＡＩ画像認識結果
                    res_txts, txt = qFunc.txtsRead(qCtrl_result_cv, encoding='utf-8', exclusive=True, )
                    if (res_txts != False):
                        txt2img_thread.put(['[txts]', res_txts ])
                    # ＡＩ画像認識結果　※ＯＣＲ
                    res_txts, txt = qFunc.txtsRead(qCtrl_result_ocr, encoding='utf-8', exclusive=True, )
                    if (res_txts != False):
                        txt2img_thread.put(['[txts]', res_txts ])
                    # ＡＩ画像認識結果　※翻訳結果
                    res_txts, txt = qFunc.txtsRead(qCtrl_result_ocrTrn, encoding='utf-8', exclusive=True, )
                    if (res_txts != False):
                        txt2img_thread.put(['[txts]', res_txts ])
                    # ＡＩ音声認識結果Ｉ／Ｆ
                    if (self.runMode == 'debug') \
                    or (self.runMode == 'handsfree') \
                    or (self.runMode == 'hud'):
                        res_txts, txt = qFunc.txtsRead(qCtrl_recognize, encoding='utf-8', exclusive=True, )
                        if (res_txts != False):
                            txt2img_thread.put(['[txts]', res_txts ])
                    # ＡＩ機械翻訳結果Ｉ／Ｆ
                    if (self.runMode == 'debug') \
                    or (self.runMode == 'handsfree') \
                    or (self.runMode == 'hud'):
                        res_txts, txt = qFunc.txtsRead(qCtrl_translate, encoding='utf-8', exclusive=True, )
                        if (res_txts != False):
                            txt2img_thread.put(['[txts]', res_txts ])

                # 画像合成（文字→画像変換結果）
                if (not txt2img_thread is None):
                    res_data  = txt2img_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '[txts_img]'):
                        txt_img = res_value.copy()
                        overlay_thread.put(['[txts_img]', txt_img ])
                    if (res_name == '[message_img]'):
                        message_img = res_value.copy()
                        overlay_thread.put(['[message_img]', message_img ])
                    if (res_name == '[status_img]'):
                        txt_img = res_value.copy()
                        overlay_thread.put(['[status_img]', txt_img ])

                # 画像出力
                if (not overlay_thread is None):
                    while (overlay_thread.proc_r.qsize() != 0):
                        res_data  = overlay_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[photo_img]'):
                            photo_img  = res_value.copy()
                            photo_time = time.time()
                        if (res_name == '[img]'):
                            display_img = res_value.copy()

                            # 結果出力
                            if (cn_s.qsize() < 99):
                                out_name  = '[display_img]'
                                out_value = display_img
                                cn_s.put([out_name, out_value])

            # アイドリング
            slow = False
            if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif ((qFunc.statusCheck(qBusy_dev_cam) == True) \
               or (qFunc.statusCheck(qBusy_dev_dsp) == True)) \
            and   (qFunc.statusCheck(qRdy__v_reader)  == False) \
            and   (qFunc.statusCheck(qRdy__v_sendkey) == False):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                time.sleep(0.05)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # スレッド停止
            if (not controlv_thread is None):
                controlv_thread.abort()
                del controlv_thread
                controlv_thread = None

            if (not overlay_thread is None):
                overlay_thread.abort()
                del overlay_thread
                overlay_thread = None

            if (not camera_thread1 is None):
                camera_thread1.abort()
                del camera_thread1
                camera_thread1 = None

            if (not camera_thread2 is None):
                camera_thread2.abort()
                del camera_thread2
                camera_thread2 = None

            if (not txt2img_thread is None):
                txt2img_thread.abort()
                del txt2img_thread
                txt2img_thread = None

            if (not cvreader_thread is None):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (not cvdetect_thread1 is None):
                cvdetect_thread1.abort()
                del cvdetect_thread1
                cvdetect_thread1 = None

            if (not cvdetect_thread2 is None):
                cvdetect_thread2.abort()
                del cvdetect_thread2
                cvdetect_thread2 = None

            if (not cv2dnn_yolo_thread is None):
                cv2dnn_yolo_thread.abort()
                del cv2dnn_yolo_thread
                cv2dnn_yolo_thread = None

            for i in range(cv2dnn_ssd_max):
                if (not cv2dnn_ssd_thread[i] is None):
                    cv2dnn_ssd_thread[i].abort()
                    del cv2dnn_ssd_thread[i]
                    cv2dnn_ssd_thread[i] = None

            if (not vin2jpg_thread is None):
                vin2jpg_thread.abort()
                del vin2jpg_thread
                vin2jpg_thread = None

            if (not coreCV_thread is None):
                coreCV_thread.abort()
                del coreCV_thread
                coreCV_thread = None

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qFunc.logOutput(self.proc_id + ':end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



    def save_photo(self, stamp, main_img, display_img, message_txts, message_time, photo_img, photo_time, ):

        # 写真保存
        main_file = ''
        try:
            if (not main_img is None):
                main_file = qPath_rec + stamp + '.photo.jpg'
                cv2.imwrite(main_file, main_img)
        except:
            main_file = ''

        screen_file = ''
        try:
            if (not display_img is None):
                screen_file = qPath_rec + stamp + '.screen.jpg'
                cv2.imwrite(screen_file, display_img)
        except:
            screen_file = ''

        photo_file = ''
        photo_txt  = ''
        try:
            if (not message_txts is None):
                if ((time.time() - message_time) < 5.00):
                    if (not photo_img is None):
                        if ((time.time() - photo_time) < 5.00):
                            photo_txt = '.' + qFunc.txt2filetxt(message_txts[0])
                            photo_file = qPath_work + stamp + '.jpg'
                            cv2.imwrite(photo_file, photo_img)
                            photo_img = None
        except:
            photo_file = ''
            photo_txt  = ''
        #if (photo_file == ''):
        #    main_file = ''

        # 写真コピー保存
        filename_p1 = qPath_v_photo  + stamp + '.photo.jpg'
        filename_p2 = qPath_d_upload + stamp + '.photo.jpg'
        filename_p3 = qCtrl_result_photo
        filename_p4 = qPath_pictures + stamp + '.photo.jpg'
        filename_s1 = qPath_d_prtscn + stamp + '.screen.jpg'
        filename_s2 = qCtrl_result_screen
        filename_m1 = qPath_rec      + stamp + photo_txt + '.jpg'
        filename_m2 = qPath_d_upload + stamp + photo_txt + '.jpg'
        filename_m3 = qPath_v_msg    + stamp + photo_txt + '.jpg'
        filename_m4 = qPath_pictures + stamp + photo_txt + '.jpg'
        if (main_file != ''):
            qFunc.copy(main_file,   filename_p1)
            qFunc.copy(main_file,   filename_p2)
            qFunc.copy(main_file,   filename_p3)
            if (qPath_pictures != ''):
                qFunc.copy(main_file,   filename_p4)
        if (screen_file != ''):
            qFunc.copy(screen_file, filename_s1)
            qFunc.copy(screen_file, filename_s2)
        if (photo_file != ''):
            qFunc.copy(photo_file,  filename_m1)
            qFunc.copy(photo_file,  filename_m2)
            qFunc.copy(photo_file,  filename_m3)
            if (qPath_pictures != ''):
                qFunc.copy(photo_file,  filename_m4)



    def check_mouse_click(self, DisplayEvent, MousePointX, MousePointY, ):
        # R-CLICK
        if (DisplayEvent == cv2.EVENT_RBUTTONDOWN):
            return 'click_r', 'r'
        # L-CLICK
        if (DisplayEvent == cv2.EVENT_LBUTTONUP):
            # ENTER,CANCEL
            if ((not MousePointX is None) and (not MousePointY is None)):
                if   (MousePointY < 80):
                    if   (self.flag_camzoom == 'on') \
                    and  (MousePointX >= 0) and (MousePointX <= 125):
                        return 'click_l', 'camzoom_reset'
                    elif (self.flag_camzoom == 'on') \
                    and  (MousePointX > 125) and (MousePointX <= 250):
                        return 'click_l', 'camzoom_zoom'
                    elif (self.flag_dspzoom == 'on') \
                    and  (MousePointX >= self.dspWidth - 250) and (MousePointX <= self.dspWidth - 125):
                        return 'click_l', 'dspzoom_reset'
                    elif (self.flag_dspzoom == 'on') \
                    and  (MousePointX > self.dspWidth -125):
                        return 'click_l', 'dspzoom_zoom'
                    else:
                        return 'click_l', 'l'
                elif (MousePointY >= 80) \
                and  (MousePointY <= self.dspHeight-150):
                        return 'click_l', 'l'
                elif (MousePointY >  self.dspHeight-150):
                    if   (self.flag_cancel == 'on') \
                    and  (MousePointX >= 0) and (MousePointX <= 350):
                        return 'click_l', 'cancel'
                    elif (self.flag_enter == 'on') \
                    and  (MousePointX >= self.dspWidth - 350) and (MousePointX <= self.dspWidth):
                        return 'click_l', 'enter'
                    else:
                        return 'click_l', 'l'
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



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'vision'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qFunc.init()

    # ログ設定

    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput(main_id + ':init')
    qFunc.logOutput(main_id + ':exsample.py runMode, cam... ')

    #runMode  debug, handsfree, hud, camera,
    #cam1Dev  num or file

    # 最終カメラ番号
    camDev_max = '9'
    chk = False
    while (chk == False) and (camDev_max >= '0'):
        try:
            dev = cv2.VideoCapture(int(camDev_max))
            ret, frame = dev.read()
            if ret == True:
                dev.release()
                chk = True
            else:
                camDev_max = str(int(camDev_max)-1)
        except:
            camDev_max = str(int(camDev_max)-1)
    if (chk == False):
        camDev_max = 'none'

    print('camDev_max', camDev_max)

    # パラメータ

    if (True):

        cam1Dev     = 'auto'
        cam1Mode    = 'full'
        cam1Stretch = '0'
        cam1Rotate  = '0'
        cam1Zoom    = '1.0'

        cam2Dev     = 'auto'
        cam2Mode    = 'vga'
        cam2Stretch = '0'
        cam2Rotate  = '0'
        cam2Zoom    = '1.0'

        dspMode     = 'full'
        dspStretch  = '0'
        dspRotate   = '0'
        dspZoom     = '1.0'

        #if (os.name == 'nt'):
        #    dspMode     = 'full+'

        if (cam1Dev == 'auto'):
            if (camDev_max == 'none'):
                cam1Dev = 'none'
            else:
                cam1Dev = camDev_max
        if (cam2Dev == 'auto'):
            if (cam1Dev == 'none') \
            or (cam1Dev == '0'):
                cam2Dev = 'none'
            else:
                cam2Dev = '0'

        if (qHOSTNAME == 'kondou-s10'):
            if (cam1Dev == '1') and (cam2Dev == '0'):
                cam1Dev  = '0'
                cam2Dev  = '1'
            if (cam1Dev == '2') and (cam2Dev == '0'):
                cam1Dev  = '2'
                cam2Dev  = '1'
        if (qHOSTNAME == 'surface-go'):
            if (cam1Dev == '2') and (cam2Dev == '0'):
                cam1Dev  = '0'
                cam2Dev  = '1'

        if (cam1Dev == cam2Dev):
            print('cam1Dev == cam2Dev')
            cam2Dev = 'none'

        codeRead    = 'qr'
        casName1    = 'face'
        casName2    = 'cars'

        autoShot    = '0'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()
            autoShot = '0'
            if (runMode=='debug'):
                autoShot = '60'

        if (len(sys.argv) >= 3):
            cam1Dev  = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            val = str(sys.argv[3]).lower()
            if (val != 'default') and (val != 'auto'):
                cam1Mode = val
        if (len(sys.argv) >= 5):
            cam1Stretch = str(sys.argv[4]).lower()
        if (len(sys.argv) >= 6):
            cam1Rotate = str(sys.argv[5]).lower()
        if (len(sys.argv) >= 7):
            cam1Zoom = str(sys.argv[6]).lower()
        if (len(sys.argv) >= 8):
            cam2Dev  = str(sys.argv[7])
        if (len(sys.argv) >= 9):
            val = str(sys.argv[8]).lower()
            if (val != 'default') and (val != 'auto'):
                cam2Mode = val
        if (len(sys.argv) >= 10):
            cam2Stretch = str(sys.argv[9]).lower()
        if (len(sys.argv) >= 11):
            cam2Rotate = str(sys.argv[10]).lower()
        if (len(sys.argv) >= 12):
            cam2Zoom = str(sys.argv[11]).lower()

        if (len(sys.argv) >= 13):
            val = str(sys.argv[12]).lower()
            if (val != 'default') and (val != 'auto'):
                dspMode = val
        if (len(sys.argv) >= 14):
            dspStretch = str(sys.argv[13]).lower()
        if (len(sys.argv) >= 15):
            dspRotate = str(sys.argv[14]).lower()
        if (len(sys.argv) >= 16):
            dspZoom = str(sys.argv[15]).lower()

        if (len(sys.argv) >= 14):
            codeRead = str(sys.argv[13])
        if (len(sys.argv) >= 15):
            casName1 = str(sys.argv[14])
        if (len(sys.argv) >= 16):
            casname2 = str(sys.argv[15])
        if (len(sys.argv) >= 17):
            qApiCV   = str(sys.argv[16]).lower()
            qApiOCR  = qApiCV
            qApiTrn  = qApiCV
        if (len(sys.argv) >= 18):
            qApiOCR  = str(sys.argv[17]).lower()
        if (len(sys.argv) >= 19):
            qApiTrn  = str(sys.argv[18]).lower()
        if (len(sys.argv) >= 20):
            qLangCV  = str(sys.argv[19]).lower()
            qLangOCR = qLangCV
        if (len(sys.argv) >= 21):
            qLangOCR = str(sys.argv[20]).lower()
        if (len(sys.argv) >= 22):
            qLangTrn = str(sys.argv[21]).lower()

        if (len(sys.argv) >= 23):
            autoShot = str(sys.argv[22]).lower()

        qFunc.logOutput(main_id + ':runMode  =' + str(runMode     ))
        qFunc.logOutput(main_id + ':cam1Dev  =' + str(cam1Dev     ))
        qFunc.logOutput(main_id + ':cam1Mode =' + str(cam1Mode    ))
        qFunc.logOutput(main_id + ':cam1Stre =' + str(cam1Stretch ))
        qFunc.logOutput(main_id + ':cam1Rote =' + str(cam1Rotate  ))
        qFunc.logOutput(main_id + ':cam1Zoom =' + str(cam1Zoom    ))
        qFunc.logOutput(main_id + ':cam2Dev  =' + str(cam2Dev     ))
        qFunc.logOutput(main_id + ':cam2Mode =' + str(cam2Mode    ))
        qFunc.logOutput(main_id + ':cam2Stre =' + str(cam2Stretch ))
        qFunc.logOutput(main_id + ':cam2Rote =' + str(cam2Rotate  ))
        qFunc.logOutput(main_id + ':cam2Zoom =' + str(cam2Zoom    ))
        qFunc.logOutput(main_id + ':dspMode  =' + str(dspMode     ))
        qFunc.logOutput(main_id + ':dspStre  =' + str(dspStretch  ))
        qFunc.logOutput(main_id + ':dspRote  =' + str(dspRotate   ))
        qFunc.logOutput(main_id + ':dspZoom  =' + str(dspZoom     ))

        qFunc.logOutput(main_id + ':codeRead =' + str(codeRead    ))
        qFunc.logOutput(main_id + ':casName1 =' + str(casName1    ))
        qFunc.logOutput(main_id + ':casName2 =' + str(casName2    ))
        qFunc.logOutput(main_id + ':qApiCV   =' + str(qApiCV      ))
        qFunc.logOutput(main_id + ':qApiOCR  =' + str(qApiOCR     ))
        qFunc.logOutput(main_id + ':qApiTrn  =' + str(qApiTrn     ))
        qFunc.logOutput(main_id + ':qLangCV  =' + str(qLangCV     ))
        qFunc.logOutput(main_id + ':qLangOCR =' + str(qLangOCR    ))
        qFunc.logOutput(main_id + ':qLangTrn =' + str(qLangTrn    ))

        qFunc.logOutput(main_id + ':autoShot =' + str(autoShot    ))

    # 初期設定

    qFunc.remove(qCtrl_control_vision     )

    qFunc.remove(qCtrl_result_photo       )
    qFunc.remove(qCtrl_result_screen      )
    qFunc.remove(qCtrl_result_vision      )
    qFunc.remove(qCtrl_result_cv          )
    qFunc.remove(qCtrl_result_cv_sjis     )
    qFunc.remove(qCtrl_result_ocr         )
    qFunc.remove(qCtrl_result_ocr_sjis    )
    qFunc.remove(qCtrl_result_ocrTrn      )
    qFunc.remove(qCtrl_result_ocrTrn_sjis )

    qFunc.makeDirs(qPath_v_ctrl,   True )
    qFunc.makeDirs(qPath_v_inp,    True )
    qFunc.makeDirs(qPath_v_jpg,    True )
    qFunc.makeDirs(qPath_v_detect, True )
    qFunc.makeDirs(qPath_v_cv,     True )
    qFunc.makeDirs(qPath_v_photo,  True )
    qFunc.makeDirs(qPath_v_msg,    True )
    qFunc.makeDirs(qPath_d_prtscn, True )

    qFunc.statusReset_vision(False)

    if (runMode == 'background'):
        qFunc.statusSet(qBusy_dev_cam, True)
        qFunc.statusSet(qBusy_dev_dsp, True)

    display_img = None
    display = None

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

        main_vision = main_vision(main_id, '0', 
                                runMode=runMode,
                                cam1Dev=cam1Dev, cam1Mode=cam1Mode, cam1Stretch=cam1Stretch, cam1Rotate=cam1Rotate, cam1Zoom=cam1Zoom,
                                cam2Dev=cam2Dev, cam2Mode=cam2Mode, cam2Stretch=cam2Stretch, cam2Rotate=cam2Rotate, cam2Zoom=cam2Zoom,
                                dspMode=dspMode, dspStretch=dspStretch, dspRotate=dspRotate, dspZoom=dspZoom,
                                codeRead=codeRead, casName1=casName1, casName2=casName2,
                                qApiCV=qApiCV, qApiOCR=qApiOCR, qApiTrn=qApiTrn,
                                qLangCV=qLangCV, qLangOCR=qLangOCR, qLangTrn=qLangTrn,
                                )

        main_vision.begin()

    # 待機ループ

    show_onece = True

    while (True):

        # 終了確認

        control = ''
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            qFunc.logOutput(main_id + ':' + str(txt))
            if (txt == '_end_'):
                break
            else:
                qFunc.remove(qCtrl_control_self)
                control = txt

        # ディスプレイ設定
        if  (display is None) \
        and (    (qFunc.statusCheck(qBusy_dev_dsp  ) == False) \
             and (qFunc.statusCheck(qBusy_d_play   ) == False) \
             and (qFunc.statusCheck(qBusy_d_browser) == False)):
            cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
            #cv2.namedWindow('Display', cv2.WINDOW_AUTOSIZE)
            cv2.moveWindow( 'Display', 0, 0)
            if (dspMode == 'full'):
                cv2.setWindowProperty('Display', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN,)
            #qFunc.winBoarder(winTitle='Display', boarder=False, )
            cv2.waitKey(1)
            display = True
            show_onece = True
        if  (not display is None) \
        and (   (qFunc.statusCheck(qBusy_dev_dsp  ) == True) \
             or (qFunc.statusCheck(qBusy_d_play   ) == True) \
             or (qFunc.statusCheck(qBusy_d_browser) == True)):
            cv2.destroyWindow('Display')
            cv2.waitKey(1)
            display = None

        while (main_vision.proc_r.qsize() != 0) and (control == ''):
            res_data  = main_vision.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == 'control'):
                control  = res_value
                break
            if (res_name == '[display_img]'):
                display_img = res_value.copy()

                if (display == True):

                    # 初回表示
                    if (show_onece == True):
                        cv2.imshow('Display', display_img )
                        cv2.setMouseCallback('Display', DisplayMouseEvent)
                        if (dspMode == 'full+') or (dspMode == 'full-'):
                            cv2.moveWindow( 'Display', -20, -50)
                            qFunc.moveWindowSize(winTitle='Display', posX=-20, posY=-50, dspMode=dspMode, )
                        else:
                            cv2.moveWindow( 'Display',   0,   0)
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
                        #break

                    else:
                        # CLICK
                        mouse1, mouse2 = main_vision.check_mouse_click(DisplayEvent, MousePointX, MousePointY, )
                        DisplayEvent = None
                        MousePointX  = None
                        MousePointY  = None
                        if (mouse1 !=''):
                            qFunc.logOutput(mouse1 + ', ' + mouse2 )
                            #break
                    
                    # 画面出力
                    cv2.imshow('Display', display_img )

                    # キーボード操作検査(2)
                    if (cv2.waitKey(1) >= 0):
                        qFunc.logOutput('key accept !', )
                        #break

                    # ボタン操作
                    if (mouse2 == 'enter') \
                    or (mouse2 == 'cancel') \
                    or (mouse2 == 'close'):
                        control = '_' + mouse2 + '_'

                    # 左クリック　写真撮影と入力画像をＡＩ画像認識処理へ
                    if (mouse1 == 'click_l') and (mouse2 == 'l'):
                        control = '_shutter_'
                        main_vision.put(['control', control])

                    # ズーム操作
                    if (mouse2 == 'camzoom_reset'):
                        main_vision.put(['control', '_camzoom_reset_'])
                    if (mouse2 == 'camzoom_zoom'):
                        main_vision.put(['control', '_camzoom_zoom_'])
                    if (mouse2 == 'dspzoom_reset'):
                        main_vision.put(['control', '_dspzoom_reset_'])
                    if (mouse2 == 'dspzoom_zoom'):
                        main_vision.put(['control', '_dspzoom_zoom_'])

                break



        # シャッター
        if (control == '_shutter_'):

            if (display == True):

                # 白表示
                display_height, display_width = display_img.shape[:2]
                white_img = np.zeros((display_height,display_width,3), np.uint8)
                cv2.rectangle(white_img,(0,0),(display_width,display_height),(255,255,255),-1)
                alpha_img = cv2.addWeighted(display_img, 0.5, white_img, 0.5, 0.0)
                cv2.imshow('Display', alpha_img )
                if (cv2.waitKey(1) >= 0):
                    qFunc.logOutput('key accept !', )

                # シャッター音
                qFunc.guide('_shutter', sync=False)



        # カメラ操作
        if (runMode == 'camera'):
            if (control == '_enter_') \
            or (control == '_cancel_') \
            or (control == '_close_'):
                qFunc.txtsWrite(qCtrl_result_vision, txts=[control], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_main, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_self, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        # バックグラウンドクリック操作
        if (runMode == 'background'):
            if (control == '_enter_') \
            or (control == '_cancel_') \
            or (control == '_close_'):
                qFunc.txtsWrite(qCtrl_result_vision, txts=[control], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusSet(qBusy_dev_cam, True)
                qFunc.statusSet(qBusy_dev_dsp, True)

        # アイドリング
        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif ((qFunc.statusCheck(qBusy_dev_cam) == True) \
           or (qFunc.statusCheck(qBusy_dev_dsp) == True)) \
        and   (qFunc.statusCheck(qRdy__v_reader)  == False) \
        and   (qFunc.statusCheck(qRdy__v_sendkey) == False):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.02)

    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        if (display == True):
            cv2.destroyWindow('Display')
            cv2.waitKey(1)

        main_vision.abort()
        del main_vision

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)



