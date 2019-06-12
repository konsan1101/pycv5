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



class proc_cvdetect:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    casName='face', procMode='640x480', ):
        self.runMode   = runMode

        self.casName   = casName
        if (casName == 'cars'):
            self.casName = '_xml/_vision_opencv_cars.xml'
        if (casName == 'face'):
            self.casName = '_xml/_vision_opencv_face.xml'
        if (casName == 'fullbody'):
            self.casName = '_xml/_vision_opencv_fullbody.xml'
        if (self.casName != 'none'):
            self.cas_nm  = self.casName[:-4]
            self.cas_nm  = self.cas_nm.replace('_vision_opencv_', '')
            self.cascade = cv2.CascadeClassifier(self.casName)
            self.haar_scale    = 1.1
            self.min_neighbors = 10
            self.min_size      = ( 15, 15)
            if (self.casName == '_vision_opencv_cars.xml'):
                self.haar_scale    = 1.1
                self.min_neighbors = 3
                self.min_size      = ( 15, 15)

        self.procMode  = procMode
        procWidth, procHeight = qFunc.getResolution(procMode)
        self.procWidth = procWidth
        self.procHeight= procHeight

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

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])



            # 画像受取
            if (inp_name.lower() == '[img]'):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ビジー設定
                if (not os.path.exists(fileBsy)):
                    qFunc.txtsWrite(fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )

                # 処理

                image_img   = inp_value.copy()
                image_height, image_width = image_img.shape[:2]

                output_img  = image_img.copy()

                proc_width  = self.procWidth
                proc_height = int(proc_width * image_height / image_width)
                proc_img    = cv2.resize(image_img, (proc_width, proc_height))

                gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.equalizeHist(gray1)

                nowTime = datetime.datetime.now()
                stamp = nowTime.strftime('%Y%m%d.%H%M%S')

                hit_count = 0
                hit_img   = None

                if (self.casName != 'none'):

                    rects = self.cascade.detectMultiScale(gray2, scaleFactor=self.haar_scale, minNeighbors=self.min_neighbors, minSize=self.min_size)
                    if (not rects is None):
                        for (hit_x, hit_y, hit_w, hit_h) in rects:
                            hit_count += 1
                            x  = int(hit_x * image_width  / proc_width )
                            y  = int(hit_y * image_height / proc_height)
                            w  = int(hit_w * image_width  / proc_width )
                            h  = int(hit_h * image_height / proc_height)
                            if (self.cas_nm == 'face'):
                                if (x > 10):
                                    x -= 10
                                    w += 20
                                if (y > 10):
                                    y -= 10
                                    h += 20
                            if (x < 0):
                                x = 0
                            if (y < 0):
                                y = 0
                            if ((x + w) > image_width):
                                    w = image_width - x
                            if ((y + h) > image_height):
                                    h = image_height - y
                            cv2.rectangle(output_img, (x,y), (x+w,y+h), (0,0,255), 2)

                            hit_img = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                            if (hit_count == 1):

                                # 結果出力
                                out_name  = '[detect]'
                                out_value = hit_img.copy()
                                cn_s.put([out_name, out_value])

                                # ファイル出力
                                fn1 = qPath_rec      + stamp + '.' + self.cas_nm + '.jpg'
                                fn2 = qPath_v_detect + stamp + '.' + self.cas_nm + '.jpg'
                                if (not os.path.exists(fn1)) and (not os.path.exists(fn2)):
                                    try:
                                        cv2.imwrite(fn1, hit_img)
                                        cv2.imwrite(fn2, hit_img)
                                    except:
                                        pass

                            # 結果出力
                            out_name  = '[array]'
                            out_value = hit_img.copy()
                            cn_s.put([out_name, out_value])

                if (hit_count == 0):

                    # 結果出力
                    out_name  = ''
                    out_value = ''
                    cn_s.put([out_name, out_value])

                else:

                    # 結果出力
                    #out_name  = '[photo]'
                    #out_value = image_img.copy()
                    #cn_s.put([out_name, out_value])

                    # 結果出力
                    out_name  = '[img]'
                    out_value = output_img.copy()
                    cn_s.put([out_name, out_value])

                    # ファイル出力
                    fn3 = qPath_rec     + stamp + '.detect.jpg'
                    fn4 = qPath_v_photo + stamp + '.detect.jpg'
                    if (not os.path.exists(fn3)) and (not os.path.exists(fn4)):
                        try:
                            cv2.imwrite(fn3, image_img)
                            cv2.imwrite(fn4, image_img)
                        except:
                            pass

                time.sleep(0.50)



            # ビジー解除
            qFunc.remove(fileBsy)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_cam, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.50)
            else:
                time.sleep(0.25)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # ビジー解除
            qFunc.remove(fileBsy)

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



    cvdetect_thread = proc_cvdetect('detect', '0', )
    cvdetect_thread.start()

    inp = cv2.imread('vision__cv_face.jpg')
    cvdetect_thread.put(['[img]', inp.copy()])

    chktime = time.time()
    while (int(time.time() - chktime) < 15):
        res_data  = cvdetect_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            if (res_name == '[array]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            if (res_name == '[photo]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            if (res_name == '[detect]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            #else:
            #    print(res_name, res_value, )

        time.sleep(0.05)

    time.sleep(1.00)
    cvdetect_thread.stop()
    del cvdetect_thread



    cv2.destroyAllWindows()


