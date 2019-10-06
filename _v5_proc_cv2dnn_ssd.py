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

import numpy as np
import cv2



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



class proc_cv2dnn_ssd:

    def __init__(self, name='thread', id='0', runMode='debug',
                    procMode='640x480', ):
        self.runMode   = runMode
        self.procMode  = procMode
        procWidth, procHeight = qFunc.getResolution(procMode)
        self.procWidth = procWidth
        self.procHeight= procHeight

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

    def __del__(self, ):
        qFunc.logOutput(self.proc_id + ':bye!', display=self.logDisp, )

    def start(self, ):
        #qFunc.logOutput(self.proc_id + ':start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.remove(self.fileRun)
        qFunc.remove(self.fileRdy)
        qFunc.remove(self.fileBsy)

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
        qFunc.txtsWrite(self.fileRun, txts=['run'], encoding='utf-8', exclusive=False, mode='a', )
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        # 定義ファイル
        file_config  = u'C:/Users/kondou/Documents/GitHub/py-etc/opencv_dnn/ssd_mobilenetv2/frozen_inference_graph.pb'
        file_weights = u'C:/Users/kondou/Documents/GitHub/py-etc/opencv_dnn/ssd_mobilenetv2/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
        file_labels  = u'C:/Users/kondou/Documents/GitHub/py-etc/opencv_dnn/ssd_mobilenetv2/labels.txt'

        print("Loading Network.....")
        model = cv2.dnn.readNetFromTensorflow(file_config, file_weights)
        print("Network successfully loaded")

        # モデルの中の訓練されたクラス名
        classNames  = {}
        classColors = {}
        r = codecs.open(file_labels, 'r', 'utf-8')
        i = 0
        for t in r:
            t = t.replace('\n', '')
            t = t.replace('\r', '')
            classNames[i]  = str(t).strip()
            classColors[i] = np.random.randint(low=0, high=255, size=3, dtype='uint8')
            i += 1

        # ＦＰＳ計測
        qFPS_class = _v5__qFunc.qFPS_class()
        qFPS_last  = time.time()

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
            if (not os.path.exists(self.fileRdy)):
                qFunc.txtsWrite(self.fileRdy, txts=['_ready_'], encoding='utf-8', exclusive=False, mode='a', )

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])



            # 画像受取
            if (inp_name.lower() == '[img]'):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ビジー設定
                if (not os.path.exists(self.fileBsy)):
                    qFunc.txtsWrite(self.fileBsy, txts=['_busy_'], encoding='utf-8', exclusive=False, mode='a', )



                # 画像の読み込み
                image = inp_value.copy()
                inp_image = image
                out_image = image

                # 画像の縦と横サイズを取得
                image_height, image_width = image.shape[:2]

                # Imageをセットする
                blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True)
                model.setInput(blob)

                # 画像から物体検出を行う
                output = model.forward()

                # outputは[1:1:100:7]のリストになっているため、後半の2つを取り出す
                detections = output[0, 0, :, :]

                # detectionには[?,id番号、予測確率、Xの開始点、Yの開始点、Xの終了点、Yの終了点]が入っている。
                for detection in detections:

                    # 予測確率を取り出し0.7以上か判定する。
                    confidence = detection[2]
                    if confidence > .7:

                        # id番号を取り出し、辞書からクラス名を取り出す。
                        classid = detection[1]
                        class_name  = classNames[classid]
                        class_color = [ int(c) for c in classColors[classid] ]

                        # 予測値に元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
                        axis = detection[3:7] * (image_width, image_height, image_width, image_height)

                        # floatからintに変換して、変数に取り出す。画像に四角や文字列を書き込むには、座標情報はintで渡す必要がある。
                        start_x, start_y, end_x, end_y = axis.astype(np.int)[:4]

                        # 一定の大きさ以上を有効とする
                        if ((end_x - start_x)>10) and ((end_y - start_y)>10):

                            # (画像、開始座標、終了座標、色、線の太さ)を指定
                            cv2.rectangle(out_image, (start_x, start_y), (end_x, end_y), class_color, thickness=2)

                            # (画像、文字列、開始座標、フォント、文字サイズ、色)を指定
                            cv2.putText(out_image, class_name, (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

                            # 認識画像出力
                            if (class_name == 'person') \
                            or (class_name == 'car'):

                                # 結果出力
                                out_name  = '[array]'
                                out_value = inp_image[start_y:end_y, start_x:end_x].copy()
                                cn_s.put([out_name, out_value])

                 # ＦＰＳ計測
                fps = qFPS_class.get()
                if ((time.time() - qFPS_last) > 5):
                    qFPS_last  = time.time()

                    # 結果出力(fps)
                    out_name  = '_fps_'
                    out_value = '{:.2f}'.format(fps)
                    cn_s.put([out_name, out_value])

                    # 結果出力(reso)
                    out_height, out_width = out_image.shape[:2]
                    out_name  = '_reso_'
                    out_value = str(out_width) + 'x' + str(out_height)
                    cn_s.put([out_name, out_value])

                # 結果出力
                out_name  = '[img]'
                out_value = out_image.copy()
                cn_s.put([out_name, out_value])

                #time.sleep(0.50)



            # ビジー解除
            qFunc.remove(self.fileBsy)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == '_busy_') \
            or (qFunc.busyCheck(qBusy_dev_cam, 0) == '_busy_'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(self.fileRdy)

            # ビジー解除
            qFunc.remove(self.fileBsy)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qFunc.logOutput(self.proc_id + ':end', display=self.logDisp, )
            qFunc.remove(self.fileRun)
            self.proc_beat = None



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )



    cv2dnn_ssd_thread = proc_cv2dnn_ssd('dnn_ssd', '0', )
    cv2dnn_ssd_thread.start()

    inp = cv2.imread('_photos/_photo_qrcode.jpg')
    inp = cv2.resize(inp, (960, 540))

    chktime = time.time()
    while ((time.time() - chktime) < 120):

        if (cv2dnn_ssd_thread.proc_s.qsize() == 0):
            cv2dnn_ssd_thread.put(['[img]', inp.copy()])

        while (cv2dnn_ssd_thread.proc_r.qsize() != 0):
            res_data  = cv2dnn_ssd_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                cv2.namedWindow('Display', 1)
                #cv2.moveWindow( 'Display', 0, 0)
                if (res_name == '[img]'):
                    cv2.imshow('Display', res_value.copy() )
                    cv2.waitKey(1)
                    #time.sleep(0.25)
                if (res_name == '[array]'):
                    cv2.imshow('Display', res_value.copy() )
                    cv2.waitKey(1)
                    #time.sleep(0.25)
                if (res_name == '_fps_'):
                    print(res_name, res_value, )
                #else:
                #    print(res_name, res_value, )

        time.sleep(0.05)

    #cv2.waitKey(0)
    time.sleep(1.00)
    cv2dnn_ssd_thread.stop()
    del cv2dnn_ssd_thread



    cv2.destroyAllWindows()


