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



class proc_cvreader:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    reader='qr', ):
        self.runMode   = runMode
        self.reader    = reader

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

        # リーダー
        qrdetector = cv2.QRCodeDetector()

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
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

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

                proc_img = image_img.copy()
                proc_height, proc_width = proc_img.shape[:2]

                #proc_width  = int(image_width/4)
                #proc_height = int(proc_width * image_height / image_width)
                #proc_img = cv2.resize(image_img, (proc_width, proc_height))
                
                gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                #gray2 = cv2.equalizeHist(gray1)

                hit_count = 0

                if (self.reader == 'qr'):

                    #try:
                    if (True):

                        #dt, p, qrx = qrdetector.detectAndDecode(proc_img)
                        dt, p, qrx = qrdetector.detectAndDecode(gray1)
                        #dt, p, qrx = qrdetector.detectAndDecode(gray2)

                        if (dt):

                            qFunc.logOutput(self.proc_id + ':qrcode [' + dt + ']')
                            qFunc.logOutput(self.proc_id + ':version ' + str(((qrx.shape[0] - 21) / 4) + 1))

                            # 透過変換
                            perspective1 = np.float32([p[0][0],p[1][0],p[2][0],p[3][0]])
                            sz = int(image_width/4)
                            perspective2 = np.float32([[0, 0],[sz, 0],[sz, sz],[0, sz]])
                            i = 0
                            for xy in p:
                                #print(xy[0,0],xy[0,1])
                                x  = int(xy[0,0] * image_width  / proc_width )
                                y  = int(xy[0,1] * image_height / proc_height)
                                if (x < 0):
                                    x = 0
                                if (y < 0):
                                    y = 0
                                perspective1[i, 0] = x
                                perspective1[i, 1] = y
                                i += 1
                            transform_matrix = cv2.getPerspectiveTransform(perspective1,perspective2)
                            matrix_img = cv2.warpPerspective(image_img, transform_matrix, (sz,sz))
                            
                            hit_count += 1

                            # 結果出力
                            out_name  = '[img]'
                            out_value = matrix_img.copy()
                            cn_s.put([out_name, out_value])

                            # 結果出力
                            #out_name  = '[photo]'
                            #out_value = image_img.copy()
                            #cn_s.put([out_name, out_value])

                            # 結果出力
                            out_name  = 'qrcode'
                            out_value = dt
                            cn_s.put([out_name, out_value])

                            # ファイル出力
                            nowTime = datetime.datetime.now()
                            stamp = nowTime.strftime('%Y%m%d.%H%M%S')

                            fn1 = qPath_rec      + stamp + '.qrcode.jpg'
                            fn2 = qPath_v_detect + stamp + '.qrcode.jpg'
                            if (not os.path.exists(fn1)) and (not os.path.exists(fn2)):
                                try:
                                    cv2.imwrite(fn1, matrix_img)
                                    cv2.imwrite(fn2, matrix_img)
                                except:
                                    pass

                            fn3 = qPath_rec     + stamp + '.reader.jpg'
                            fn4 = qPath_v_photo + stamp + '.reader.jpg'
                            if (not os.path.exists(fn3)) and (not os.path.exists(fn4)):
                                try:
                                    cv2.imwrite(fn3, image_img)
                                    cv2.imwrite(fn4, image_img)
                                except:
                                    pass

                    #except:
                    #    pass

                if (hit_count == 0):

                    # 結果出力
                    out_name  = ''
                    out_value = ''
                    cn_s.put([out_name, out_value])

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
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)



    cvreader_thread = proc_cvreader('reader', '0', )
    cvreader_thread.start()

    inp = cv2.imread('_photos/_photo_qrcode.jpg')
    cvreader_thread.put(['[img]', inp.copy()])

    chktime = time.time()
    while (int(time.time() - chktime) < 15):
        res_data  = cvreader_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            else:
                print(res_name, res_value, )

        time.sleep(0.05)

    time.sleep(1.00)
    cvreader_thread.stop()
    del cvreader_thread



    cv2.destroyAllWindows()


