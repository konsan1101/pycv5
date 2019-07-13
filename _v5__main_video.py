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

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)


# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_audio      = 'temp/control_audio.txt'
qCtrl_control_video      = 'temp/control_video.txt'
qCtrl_recognize          = 'temp/result_recognize.txt'
qCtrl_translate          = 'temp/result_translate.txt'

# 出力インターフェース
qCtrl_result_video       = 'temp/result_video.txt'
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

# thread ルーチン群
import _v5_proc_controlv
import _v5_proc_overlay
import _v5_proc_camera
import _v5_proc_txt2img
import _v5_proc_cvreader
import _v5_proc_cvdetect
import _v5_proc_yolo_keras
import _v5_proc_yolo_torch
import _v5_proc_vin2jpg
import _v5_proc_coreCV



runMode    = 'hud'

qApiCV     = 'google'
qApiOCR    = qApiCV
qApiTrn    = 'free'
qLangCV    = 'ja'
qLangOCR   = qLangCV
qLangTrn   = 'en'



class main_video:

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
        self.cam1Mode    = cam1Mode
        self.cam1Stretch = cam1Stretch
        self.cam1Rotate  = cam1Rotate
        self.cam1Zoom    = cam1Zoom
        self.cam2Dev     = cam2Dev
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
        self.flag_camzoom    = 'off'
        self.flag_dspzoom    = 'off'
        self.flag_enter      = 'off'
        self.flag_cancel     = 'off'
        self.flag_background = 'on'
        self.flag_blackwhite = 'black'
        if (self.runMode == 'debug'):
            self.flag_camzoom    = 'on'
            self.flag_dspzoom    = 'on'
            self.flag_enter      = 'on'
            self.flag_cancel     = 'on'
        if (self.runMode == 'handsfree'):
            self.flag_camzoom    = 'on'
            self.flag_dspzoom    = 'on'
        if (self.runMode == 'hud'):
            self.flag_blackwhite = 'white'
        if (self.runMode == 'camera'):
            self.flag_camzoom    = 'on'
            self.flag_enter      = 'on'
            self.flag_cancel     = 'on'

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

        # 変数
        controlv_thread   = None
        controlv_switch   = 'on'
        overlay_thread    = None
        overlay_switch    = 'on'
        camera_thread1    = None
        camera_switch1    = 'on'
        camera_thread2    = None
        camera_switch2    = 'on'
        txt2img_thread    = None
        txt2img_switch    = 'on'
        cvreader_thread   = None
        cvreader_switch   = 'on'
        cvdetect_thread1  = None
        cvdetect_switch1  = 'on'
        cvdetect_thread2  = None
        cvdetect_switch2  = 'on'
        yolo_keras_thread = None
        yolo_keras_switch = 'on'
        yolo_torch_max    = 2
        yolo_torch_seq    = 0
        yolo_torch_thread = {}
        yolo_torch_switch = 'on'
        for i in range(yolo_torch_max):
            yolo_torch_thread[i] = None
        vin2jpg_thread    = None
        vin2jpg_switch    = 'on'
        coreCV_thread     = None
        coreCV_switch     = 'on'

        if (self.runMode == 'debug'):
            camera_switch2    = 'on'
            cvreader_switch   = 'on'
            cvdetect_switch1  = 'on'
            cvdetect_switch2  = 'on'
            yolo_keras_switch = 'on'
            yolo_torch_switch = 'on'
            vin2jpg_switch    = 'on'
            coreCV_switch     = 'on'
        if (self.runMode == 'handsfree'):
            camera_switch2    = 'on'
            cvreader_switch   = 'on'
            cvdetect_switch1  = 'off'
            cvdetect_switch2  = 'off'
            yolo_keras_switch = 'off'
            yolo_torch_switch = 'on'
            vin2jpg_switch    = 'on'
            coreCV_switch     = 'on'
        if (self.runMode == 'hud'):
            camera_switch2    = 'off'
            cvreader_switch   = 'on'
            cvdetect_switch1  = 'off'
            cvdetect_switch2  = 'off'
            yolo_keras_switch = 'off'
            yolo_torch_switch = 'off'
            vin2jpg_switch    = 'off'
            coreCV_switch     = 'off'
        if (self.runMode == 'camera'):
            camera_switch2    = 'off'
            cvreader_switch   = 'on'
            cvdetect_switch1  = 'off'
            cvdetect_switch2  = 'off'
            yolo_keras_switch = 'off'
            yolo_torch_switch = 'off'
            vin2jpg_switch    = 'off'
            coreCV_switch     = 'off'

        if (self.cam2Dev == 'none'):
            camera_switch2    = 'off'

        busy_status_txts = _v5__qFunc.qBusy_status_txts_class()

        # 待機ループ
        self.proc_step = '5'

        cvreader_last_put  = time.time()
        cvdetect1_last_put = time.time()
        cvdetect2_last_put = time.time()
        yolo_last_put      = time.time()

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

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            try:
                txts, txt = qFunc.txtsRead(qCtrl_control_video)
                if (txt == '_close_'):
                    break
            except:
                pass

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

            # スレッド設定

            speechs = []

            if (controlv_thread is None) and (controlv_switch == 'on'):
                controlv_thread = _v5_proc_controlv.proc_controlv(
                                    name='controlv', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                controlv_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ制御」の機能が有効になりました。', 'wait':0, })

            if (not controlv_thread is None) and (controlv_switch != 'on'):
                controlv_thread.stop()
                del controlv_thread
                controlv_thread = None

            if (overlay_thread is None) and (overlay_switch == 'on'):
                overlay_thread = _v5_proc_overlay.proc_overlay(
                                    name='overlay', id='0',
                                    runMode=self.runMode,
                                    dspMode=self.dspMode, dspStretch=self.dspStretch, dspRotate=self.dspRotate, dspZoom=self.dspZoom,
                                    )
                overlay_thread.start()

                overlay_thread.put(['flag_camzoom'   , flag_camzoom    ])
                overlay_thread.put(['flag_dspzoom'   , flag_dspzoom    ])
                overlay_thread.put(['flag_enter'     , flag_enter      ])
                overlay_thread.put(['flag_cancel'    , flag_cancel     ])
                overlay_thread.put(['flag_background', flag_background ])
                overlay_thread.put(['flag_blackwhite', flag_blackwhite ])

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「画面表示」の機能が有効になりました。', 'wait':0, })

            if (not overlay_thread is None) and (overlay_switch != 'on'):
                overlay_thread.stop()
                del overlay_thread
                overlay_thread = None

            if (camera_thread1 is None) and (camera_switch1 == 'on'):
                camera_thread1 = _v5_proc_camera.proc_camera(
                                    name='camera', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev, camMode=self.cam1Mode, camStretch=self.cam1Stretch, camRotate=self.cam1Rotate, camZoom=self.cam1Zoom, camFps='15',
                                    )
                camera_thread1.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ１入力」の機能が有効になりました。', 'wait':0, })

            if (not camera_thread1 is None) and (camera_switch1 != 'on'):
                camera_thread1.stop()
                del camera_thread1
                camera_thread1 = None

            if (camera_thread2 is None) and (camera_switch2 == 'on'):
                camera_thread2 = _v5_proc_camera.proc_camera(
                                    name='camera', id='1',
                                    runMode=self.runMode,
                                    camDev=self.cam2Dev, camMode=self.cam2Mode, camStretch=self.cam2Stretch, camRotate=self.cam2Rotate, camZoom=self.cam2Zoom, camFps='5',
                                    )
                camera_thread2.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「カメラ２入力」の機能が有効になりました。', 'wait':0, })

            if (not camera_thread2 is None) and (camera_switch2 != 'on'):
                camera_thread2.stop()
                del camera_thread2
                camera_thread2 = None

            if (txt2img_thread is None) and (txt2img_switch == 'on'):
                txt2img_thread = _v5_proc_txt2img.proc_txt2img(
                                    name='txt2img', id='0',
                                    runMode=self.runMode,
                                    )
                txt2img_thread.start()

                txt2img_thread.put(['flag_background', flag_background ])
                txt2img_thread.put(['flag_blackwhite', flag_blackwhite ])

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「認識文字の表示」の機能が有効になりました。', 'wait':0, })

            if (not txt2img_thread is None) and (txt2img_switch != 'on'):
                txt2img_thread.stop()
                del txt2img_thread
                txt2img_thread = None

            if (cvreader_thread is None) and (cvreader_switch == 'on'):
                cvreader_thread = _v5_proc_cvreader.proc_cvreader(
                                    name='reader', id='0',
                                    runMode=self.runMode, 
                                    reader=self.codeRead,
                                    )
                cvreader_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＱＲコード認識」の機能が有効になりました。', 'wait':0, })

            if (not cvreader_thread is None) and (cvreader_switch != 'on'):
                cvreader_thread.stop()
                del cvreader_thread
                cvreader_thread = None

            if (cvdetect_thread1 is None) and (cvdetect_switch1 == 'on'):
                cvdetect_thread1 = _v5_proc_cvdetect.proc_cvdetect(
                                    name='detect', id='0',
                                    runMode=self.runMode, 
                                    casName=self.casName1, procMode='640x480',
                                    )
                cvdetect_thread1.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「オープンＣＶ画像認識」の機能が有効になりました。', 'wait':0, })

            if (not cvdetect_thread1 is None) and (cvdetect_switch1 != 'on'):
                cvdetect_thread1.stop()
                del cvdetect_thread1
                cvdetect_thread1 = None

            if (cvdetect_thread2 is None) and (cvdetect_switch2 == 'on'):
                cvdetect_thread2 = _v5_proc_cvdetect.proc_cvdetect(
                                    name='detect', id='1',
                                    runMode=self.runMode, 
                                    casName=self.casName2, procMode='640x480',
                                    )
                cvdetect_thread2.start()

            if (not cvdetect_thread2 is None) and (cvdetect_switch2 != 'on'):
                cvdetect_thread2.stop()
                del cvdetect_thread2
                cvdetect_thread2 = None

            if (yolo_keras_thread is None) and (yolo_keras_switch == 'on'):
                yolo_keras_thread = _v5_proc_yolo_torch.proc_yolo_torch(
                                    name='yolokeras', id='0',
                                    runMode=self.runMode, 
                                    procMode='320x240',
                                    )
                yolo_keras_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「画像認識（Ｋｅｒａｓ）」の機能が有効になりました。', 'wait':0, })

            if (not yolo_keras_thread is None) and (yolo_keras_switch != 'on'):
                yolo_keras_thread.stop()
                del yolo_keras_thread
                yolo_keras_thread = None

            for i in range(yolo_torch_max):
                if (yolo_torch_thread[i] is None) and (yolo_torch_switch == 'on'):
                    yolo_torch_thread[i] = _v5_proc_yolo_torch.proc_yolo_torch(
                                        name='yolotorch', id=str(i),
                                        runMode=self.runMode, 
                                        procMode='320x240',
                                        )
                    yolo_torch_thread[i].start()

                    if (i == 0):
                        if (self.runMode == 'debug') \
                        or (self.runMode == 'handsfree'):
                            speechs.append({ 'text':u'「画像認識（Ｐｙｔｏｒｃｈ）」の機能が有効になりました。', 'wait':0, })

            for i in range(yolo_torch_max):
                if (not yolo_torch_thread[i] is None) and (yolo_torch_switch != 'on'):
                    yolo_torch_thread[i].stop()
                    del yolo_torch_thread[i]
                    yolo_torch_thread[i] = None

            if (vin2jpg_thread is None) and (vin2jpg_switch == 'on'):
                vin2jpg_thread = _v5_proc_vin2jpg.proc_vin2jpg(
                                    name='vin2jpg', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                vin2jpg_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「写真認識」の機能が有効になりました。', 'wait':0, })

            if (not vin2jpg_thread is None) and (vin2jpg_switch != 'on'):
                vin2jpg_thread.stop()
                del vin2jpg_thread
                vin2jpg_thread = None

            if (coreCV_thread is None) and (coreCV_switch == 'on'):
                coreCV_thread = _v5_proc_coreCV.proc_coreCV(
                                    name='coreCV', id='0',
                                    runMode=self.runMode,
                                    camDev=self.cam1Dev,
                                    )
                coreCV_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＡＩ画像認識」の機能が有効になりました。', 'wait':0, })

            if (not coreCV_thread is None) and (coreCV_switch != 'on'):
                coreCV_thread.stop()                
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
            if (not os.path.exists(fileRdy)):
                qFunc.txtsWrite(fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])

            # 動画ファイル処理（バッチ）時の自動終了
            if (not self.cam1Dev.isdigit()):
                if  (int(time.time() - camera_thread1.proc_last) > 60):
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
                                message_txts = res_value
                                message_time = time.time()
                                message_img  = None
                                # 結果出力
                                if (cn_s.qsize() < 99):
                                    txt2img_thread.put(['[message_txts]', message_txts])

            # リセット
            if (control == 'reset'):
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
                    camera_thread1.put(['camstretch'     , cam1Stretch     ])
                    camera_thread1.put(['camrotate'      , cam1Rotate      ])
                    camera_thread1.put(['camzoom'        , cam1Zoom        ])
                if (not camera_thread2 is None):
                    camera_thread2.put(['camstretch'     , cam2Stretch     ])
                    camera_thread2.put(['camrotate'      , cam2Rotate      ])
                    camera_thread2.put(['camzoom'        , cam2Zoom        ])
                if (not overlay_thread is None):
                    overlay_thread.put(['dspstretch'     , dspStretch      ])
                    overlay_thread.put(['dsprotate'      , dspRotate       ])
                    overlay_thread.put(['dspzoom'        , dspZoom         ])
                    overlay_thread.put(['flag_camzoom'   , flag_camzoom    ])
                    overlay_thread.put(['flag_dspzoom'   , flag_dspzoom    ])
                    overlay_thread.put(['flag_background', flag_background ])
                    overlay_thread.put(['flag_blackwhite', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['flag_background', flag_background ])
                    txt2img_thread.put(['flag_blackwhite', flag_blackwhite ])

            # カメラ操作
            if (control == 'zoomout') or (control == 'camzoom-reset'):
                cam1Zoom    = '1.0'
                if (not camera_thread1 is None):
                    camera_thread1.put(['camzoom', cam1Zoom ])
            if (control == 'zoomin') or (control == 'camzoom-zoom'):
                cam1Zoom    = '{:.1f}'.format(float(cam1Zoom) + 0.5)
                print(cam1Zoom)
                if (not camera_thread1 is None):
                    camera_thread1.put(['camzoom', cam1Zoom ])
            if (control == 'stretch'):
                cam1Stretch = str(int(cam1Stretch) + 10)
                if (not camera_thread1 is None):
                    camera_thread1.put(['camstretch',  cam1Stretch ])
            if (control == 'rotate'):
                cam1Rotate  = str(int(cam1Rotate)  + 45)
                if (not camera_thread1 is None):
                    camera_thread1.put(['camrotate',   cam1Rotate  ])

            # 表示操作
            if (control == 'dspzoom-reset'):
                dspZoom    = '1.0'
                if (not overlay_thread is None):
                    overlay_thread.put(['dspzoom', dspZoom ])
            if (control == 'dspzoom-zoom'):
                dspZoom    = '{:.1f}'.format(float(dspZoom) + 0.5)
                if (not overlay_thread is None):
                    overlay_thread.put(['dspzoom', dspZoom ])

            # 背景操作
            if (control == 'background'):
                if   (flag_background == 'on'):
                    flag_background = 'off'
                elif (flag_background == 'off'):
                    flag_background = 'on'
                if (not overlay_thread is None):
                    overlay_thread.put(['flag_background', flag_background ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['flag_background', flag_background ])
            if (control == 'black'):
                flag_blackwhite = 'black'
                if (not overlay_thread is None):
                    overlay_thread.put(['flag_blackwhite', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['flag_blackwhite', flag_blackwhite ])
            if (control == 'white'):
                flag_blackwhite = 'white'
                if (not overlay_thread is None):
                    overlay_thread.put(['flag_blackwhite', flag_blackwhite ])
                if (not txt2img_thread is None):
                    txt2img_thread.put(['flag_blackwhite', flag_blackwhite ])

            # シャッター
            if (control == 'shutter'):

                # 撮影ログ
                logset = False
                if (not photo_img is None):
                    if ((time.time() - photo_time) < 5.00):
                        overlay_thread.put(['[shutter]', photo_img ])
                        overlay_thread.put(['[array]',   photo_img ])
                        logset = True
                if (logset == False):
                    if (not main_img is None):
                        overlay_thread.put(['[shutter]', main_img ])
                        overlay_thread.put(['[array]',   main_img ])

                # ＡＩ画像認識処理へ
                nowTime = datetime.datetime.now()
                stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                filename0 = qPath_v_inp   + stamp + '.photo.jpg'
                #try:
                if (not main_img is None):
                    cv2.imwrite(filename0, main_img)
                #except:
                #    pass

                # 写真保存
                self.save_photo(stamp, main_img, display_img, message_txts, message_time, photo_img, photo_time, )

            if  (cn_s.qsize() == 0) \
            and (overlay_thread.proc_s.qsize() == 0):

                # 画像入力（メインカメラ）
                while (camera_thread1.proc_r.qsize() != 0):
                    res_data  = camera_thread1.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == 'fps'):
                        overlay_thread.put(['cam1_fps', res_value ])
                    if (res_name == 'reso'):
                        overlay_thread.put(['cam1_reso', res_value ])
                    if (res_name == '[img]'):
                        main_img = res_value.copy()

                        if (qFunc.busyCheck(qBusy_dev_cam, 0) != 'busy'):

                            # 画像識別（ＱＲ）
                            if (int(time.time() - cvreader_last_put) >= 1):
                                if (not cvreader_thread is None):
                                    if (cvreader_thread.proc_s.qsize() == 0):
                                        cvreader_thread.put(['[img]', main_img ])
                                        cvreader_last_put = time.time()

                            # 画像識別（顔等）
                            if  (int(time.time() - cvdetect1_last_put) >= 1):
                                if (not cvdetect_thread1 is None):
                                    if (cvdetect_thread1.proc_s.qsize() == 0):
                                        cvdetect_thread1.put(['[img]', main_img ])
                                        cvdetect1_last_put = time.time()
                            
                            # 画像識別（自動車等）
                            if  (int(time.time() - cvdetect2_last_put) >= 1):
                                if (not cvdetect_thread2 is None):
                                    if (cvdetect_thread2.proc_s.qsize() == 0):
                                        cvdetect_thread2.put(['[img]', main_img ])
                                        cvdetect2_last_put = time.time()

                            # 画像識別（YOLO）keras
                            if  (int(time.time() - yolo_last_put) >= 1):
                                if (not yolo_keras_thread is None):
                                    if (yolo_keras_thread.proc_s.qsize() == 0):
                                        yolo_keras_thread.put(['[img]', main_img ])
                                        yolo_last_put = time.time()

                            # 画像識別（YOLO）torch
                            if (int(time.time() - yolo_last_put) >= (1/yolo_torch_max)/2):
                                i = yolo_torch_seq
                                if (not yolo_torch_thread[i] is None):
                                    if (yolo_torch_thread[i].proc_s.qsize() == 0):
                                        yolo_torch_thread[i].put(['[img]', main_img ])
                                        yolo_last_put = time.time()
                                        #print('yolo put ' + str(i))
                                        yolo_torch_seq += 1
                                        yolo_torch_seq = yolo_torch_seq % yolo_torch_max
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
                        if (res_name == 'fps'):
                            overlay_thread.put(['cam2_fps', res_value ])
                        if (res_name == 'reso'):
                            overlay_thread.put(['cam2_reso', res_value ])
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

                # 画像合成（YOLO識別結果）keras
                if (not yolo_keras_thread is None):
                    while (yolo_keras_thread.proc_r.qsize() != 0):
                        res_data  = yolo_keras_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == 'fps'):
                            overlay_thread.put(['comp_fps', res_value ])
                        if (res_name == 'reso'):
                            overlay_thread.put(['comp_reso', res_value ])
                        if (res_name == '[img]'):
                            yolo_img = res_value.copy()
                            overlay_thread.put(['[comp]', yolo_img ])
                        if (res_name == '[array]'):
                            ary_imgy = res_value.copy()
                            overlay_thread.put(['[array]', ary_imgy ])
                            if (cvdetect_thread1 is None):
                                overlay_thread.put(['[detect1]', ary_imgy ])

                # 画像合成（YOLO識別結果）torch
                for i in range(yolo_torch_max):
                    if (not yolo_torch_thread[i] is None):
                        while (yolo_torch_thread[i].proc_r.qsize() != 0):
                            res_data  = yolo_torch_thread[i].get()
                            res_name  = res_data[0]
                            res_value = res_data[1]
                            if (res_name == 'fps'):
                                overlay_thread.put(['comp_fps', '{:.2f}'.format(float(res_value) * yolo_torch_max) ])
                            if (res_name == 'reso'):
                                overlay_thread.put(['comp_reso', res_value ])
                            if (res_name == '[img]'):
                                #print('yolo get '+str(i))
                                yolo_img = res_value.copy()
                                overlay_thread.put(['[comp]', yolo_img ])
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
                    if (self.runMode == 'debug') \
                    or (self.runMode == 'handsfree') \
                    or (self.runMode == 'hud'):
                        res_txts = busy_status_txts.get()
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
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_cam, 0) == 'busy'):
                time.sleep(1.00)
            time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # スレッド停止
            if (not controlv_thread is None):
                controlv_thread.stop()
                del controlv_thread
                controlv_thread = None

            if (not overlay_thread is None):
                overlay_thread.stop()
                del overlay_thread
                overlay_thread = None

            if (not camera_thread1 is None):
                camera_thread1.stop()
                del camera_thread1
                camera_thread1 = None

            if (not camera_thread2 is None):
                camera_thread2.stop()
                del camera_thread2
                camera_thread2 = None

            if (not txt2img_thread is None):
                txt2img_thread.stop()
                del txt2img_thread
                txt2img_thread = None

            if (not cvreader_thread is None):
                cvreader_thread.stop()
                del cvreader_thread
                cvreader_thread = None

            if (not cvdetect_thread1 is None):
                cvdetect_thread1.stop()
                del cvdetect_thread1
                cvdetect_thread1 = None

            if (not cvdetect_thread2 is None):
                cvdetect_thread2.stop()
                del cvdetect_thread2
                cvdetect_thread2 = None

            if (not yolo_keras_thread is None):
                yolo_keras_thread.stop()
                del yolo_keras_thread
                yolo_keras_thread = None

            for i in range(yolo_torch_max):
                if (not yolo_torch_thread[i] is None):
                    yolo_torch_thread[i].stop()
                    del yolo_torch_thread[i]
                    yolo_torch_thread[i] = None

            if (not vin2jpg_thread is None):                    
                vin2jpg_thread.stop()
                del vin2jpg_thread
                vin2jpg_thread = None

            if (not coreCV_thread is None):
                coreCV_thread.stop()                
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
            self.proc_beat = None



    def save_photo(self, stamp, main_img, display_img, message_txts, message_time, photo_img, photo_time, ):

        # 写真保存
        main_file = ''
        try:
            if (not main_img is None):
                main_file = qPath_rec + 'photo.' + stamp + '.jpg'
                cv2.imwrite(main_file, main_img)
        except:
            main_file = ''
        screen_file = ''
        try:
            if (not display_img is None):
                screen_file = qPath_rec + 'screen.' + stamp + '.jpg'
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
        if (photo_file == ''):
            main_file = ''

        # 写真コピー保存
        filename1 = qPath_v_photo + 'photo.' + stamp + '.jpg'
        filename2 = qCtrl_result_photo
        filename3 = qPath_v_photo + 'screen.' + stamp + '.jpg'
        filename4 = qCtrl_result_screen
        filename5 = qPath_rec     + stamp + photo_txt + '.jpg'
        filename6 = qPath_v_photo + stamp + photo_txt + '.jpg'
        if (main_file != ''):
            try:
                shutil.copy2(main_file,   filename1)
                shutil.copy2(main_file,   filename2)
            except:
                pass
        if (screen_file != ''):
            try:
                shutil.copy2(screen_file, filename3)
                shutil.copy2(screen_file, filename4)
            except:
                pass
        if (photo_file != ''):
            try:
                shutil.copy2(photo_file,  filename5)
                shutil.copy2(photo_file,  filename6)
            except:
                pass



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
    main_name = 'main_video'
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

    # パラメータ

    if (True):

        cam1Dev     = '9'
        cam1Mode    = 'default'
        cam1Stretch = '0'
        cam1Rotate  = '0'
        cam1Zoom    = '1.0'

        cam2Dev     = 'none'
        cam2Mode    = 'vga'
        cam2Stretch = '0'
        cam2Rotate  = '0'
        cam2Zoom    = '1.0'

        dspMode     = 'full'
        dspStretch  = '0'
        dspRotate   = '0'
        dspZoom     = '1.0'

        chk = False
        while (chk == False) and (cam1Dev > '0'):
            try:
                dev = cv2.VideoCapture(int(cam1Dev))
                ret, frame = dev.read()
                if ret == True:
                    dev.release()
                    chk = True
                else:
                    cam1Dev = str(int(cam1Dev)-1)
            except:
                cam1Dev = str(int(cam1Dev)-1)
        if (cam1Dev == '0'):
            cam1Mode = 'vga'
        if (cam1Dev > '0'):
            cam2Dev  = '0'

        if (os.name == 'nt'):
            if (cam1Dev == '1') and (cam2Dev == '0'):
                cam1Dev  = '0'
                cam2Dev  = '1'

        #if (cam1Dev == cam2Dev):
        #    print('cam1Dev == cam2Dev')
        #    cam2Dev = 'none'

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

    qFunc.remove(qCtrl_control_video     )

    qFunc.remove(qCtrl_result_video       )
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

    qFunc.busyReset_v(False)

    qFunc.busySet(qBusy_dev_cpu, False)
    qFunc.busySet(qBusy_dev_com, False)
    qFunc.busySet(qBusy_dev_cam, False)
    qFunc.busySet(qBusy_dev_dsp, False)

    display_img = None

    display = None

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

        main_video = main_video('main_video', '0', 
                                runMode=runMode,
                                cam1Dev=cam1Dev, cam1Mode=cam1Mode, cam1Stretch=cam1Stretch, cam1Rotate=cam1Rotate, cam1Zoom=cam1Zoom,
                                cam2Dev=cam2Dev, cam2Mode=cam2Mode, cam2Stretch=cam2Stretch, cam2Rotate=cam2Rotate, cam2Zoom=cam2Zoom,
                                dspMode=dspMode, dspStretch=dspStretch, dspRotate=dspRotate, dspZoom=dspZoom,
                                codeRead=codeRead, casName1=casName1, casName2=casName2,
                                qApiCV=qApiCV, qApiOCR=qApiOCR, qApiTrn=qApiTrn,
                                qLangCV=qLangCV, qLangOCR=qLangOCR, qLangTrn=qLangTrn,
                                )

        main_video.start()

    # 待機ループ

    show_onece = True

    while (True):

        # 終了確認
        try:
            txts, txt = qFunc.txtsRead(qCtrl_control_video)
            if (txt == '_close_'):
                break
        except:
            pass

        # ディスプレイ設定
        if (display is None) and (qFunc.busyCheck(qBusy_dev_dsp, 0) != 'busy'): 
            cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
            cv2.moveWindow( 'Display', 0, 0)
            if (dspMode == 'full'):
                cv2.setWindowProperty('Display', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN,)
            cv2.waitKey(1)
            display = True
            show_onece = True
        if (not display is None) and (qFunc.busyCheck(qBusy_dev_dsp, 0) == 'busy'): 
            cv2.destroyWindow('Display')
            cv2.waitKey(1)
            display = None

        control = ''

        while (main_video.proc_r.qsize() != 0) and (control == ''):
            res_data  = main_video.get()
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
                            cv2.moveWindow( 'Display', -20, -40)
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
                        mouse1, mouse2 = main_video.check_mouse_click(DisplayEvent, MousePointX, MousePointY, )
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
                        control = mouse2

                    # 左クリック　写真撮影と入力画像をＡＩ画像認識処理へ
                    if (mouse1 == 'l-click') and (mouse2 == 'l'):
                        control = 'shutter'
                        main_video.put(['control', 'shutter'])

                    # ズーム操作
                    if (mouse2 == 'camzoom-reset'):
                        main_video.put(['control', 'camzoom-reset'])
                        main_video.put(['control', 'background'])
                    if (mouse2 == 'camzoom-zoom'):
                        main_video.put(['control', 'camzoom-zoom'])
                    if (mouse2 == 'dspzoom-reset'):
                        main_video.put(['control', 'dspzoom-reset'])
                    if (mouse2 == 'dspzoom-zoom'):
                        main_video.put(['control', 'dspzoom-zoom'])

                break



        # シャッター
        if (control == 'shutter'):

            ## 白表示
            display_height, display_width = display_img.shape[:2]
            white_img = np.zeros((display_height,display_width,3), np.uint8)
            cv2.rectangle(white_img,(0,0),(display_width,display_height),(255,255,255),-1)
            alpha_img = cv2.addWeighted(display_img, 0.5, white_img, 0.5, 0.0)
            cv2.imshow('Display', alpha_img )
            if (cv2.waitKey(1) >= 0):
                qFunc.logOutput('key accept !', )

            # シャッター音
            qFunc.guide('_shutter', sync=False)



        # 終了操作
        if (runMode == 'camera') \
        or (runMode == 'hud'):
            if (qFunc.busyCheck(qBusy_dev_dsp, 0) == 'busy'): 
                qFunc.txtsWrite(qCtrl_control_main,  txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_video, txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
                break

            if (control == 'enter') \
            or (control == 'cancel') \
            or (control == 'close'):
                qFunc.txtsWrite(qCtrl_result_video, txts=[mouse2], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.busySet(qBusy_dev_dsp, True)

        # アイドリング
        if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
        or (qFunc.busyCheck(qBusy_dev_cam, 0) == 'busy'):
            time.sleep(1.00)
        time.sleep(0.02)



    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        if (display == True):
            cv2.destroyWindow('Display')
            cv2.waitKey(1)

        qFunc.logOutput(main_id + ':bye!')

        main_video.stop()
        del main_video


