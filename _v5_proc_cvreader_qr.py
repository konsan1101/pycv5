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

    def abort(self, waitMax=5, ):
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

        # ２重読取防止
        read_time = {}

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
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

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
                if (qFunc.statusCheck(self.fileBsy) == False):
                    qFunc.statusSet(self.fileBsy, True)
                    if (str(self.id) == '0') or (str(self.id) == 'v'):
                        qFunc.statusSet(qBusy_v_QR, True)
                    if (str(self.id) == 'd'):
                        qFunc.statusSet(qBusy_d_QR, True)

                # 処理

                image_img   = inp_value.copy()
                image_height, image_width = image_img.shape[:2]

                proc_img = image_img.copy()
                proc_height, proc_width = proc_img.shape[:2]
                
                gray_img = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                #gray_img = cv2.equalizeHist(gray_img)

                hit_count = 0
                res_count = 0

                if (self.reader == 'qr'):

                    rerun = True
                    while (rerun == True):
                        rerun = False

                        qr, p, qrx = qrdetector.detectAndDecode(gray_img)

                        read_text = ''
                        read_img  = None
                        if (qr):
                            rerun = True

                            # 読取状況確認 qr -> read
                            read_text = qr
                            if (read_text == 'http://localhost/v5/sendkey_on.py'):
                                read_text = '_sendkey_on_'

                            read_text = read_text.replace('\r\n', '[cr]')
                            read_text = read_text.replace('\r', '[cr]')
                            read_text = read_text.replace('\n', '[cr]')

                            # 透過変換 p -> matrix_img
                            perspective0 = np.float32([p[0][0],p[1][0],p[2][0],p[3][0]])
                            perspective1 = perspective0
                            print(perspective0)
                            sz = int(image_width/4)
                            perspective2 = np.float32([[0, 0],[sz, 0],[sz, sz],[0, sz]])

                            max_x = 0
                            min_x = proc_width
                            max_y = 0
                            min_y = proc_height
                            i = 0
                            for xy in p:
                                if (xy[0,0] > max_x):
                                    max_x = xy[0,0]
                                if (xy[0,0] < min_x):
                                    min_x = xy[0,0]
                                if (xy[0,1] > max_y):
                                    max_y = xy[0,1]
                                if (xy[0,1] < min_y):
                                    min_y = xy[0,1]

                                image_x  = int(xy[0,0] * image_width  / proc_width )
                                image_y  = int(xy[0,1] * image_height / proc_height)
                                if (image_x < 0):
                                    image_x = 0
                                if (image_y < 0):
                                    image_y = 0
                                perspective1[i, 0] = image_x
                                perspective1[i, 1] = image_y
                                i += 1

                            print(perspective1)
                            print(perspective2)
                            transform_matrix = cv2.getPerspectiveTransform(perspective1,perspective2)
                            read_img = cv2.warpPerspective(image_img, transform_matrix, (sz,sz))

                            # 読取位置の塗りつぶし
                            #gray_img = cv2.fillPoly(gray_img, pts=perspective0, color=(0,0,0), )
                            gray_img = cv2.rectangle(gray_img, (min_x,min_y), (max_x,max_y), 255, thickness=-1, )
                            #cv2.imshow('Debug', cv2.resize(gray_img, (640,480)) )
                            #cv2.waitKey(1)

                            # 経過時間計算
                            try:
                                sec = time.time() - read_time[read_text]
                            except:
                                sec = 999

                            # 新規
                            if (sec == 999):
                                read_time[read_text] = time.time()
                            # on 指令は最初だけ、あとは継続
                            elif (read_text[-4:] == '_on_'):
                                read_time[read_text] = time.time()
                                read_text = ''
                                read_img  = None
                            # ３秒経過は新規とみなす
                            elif (sec > 3):
                                read_time[read_text] = time.time()
                            # ３秒以内は無視
                            else:
                                read_text = ''
                                read_img  = None

                        # 読取ＯＫ
                        if (qr) and (read_text != ''):
                            hit_count += 1
                            qFunc.logOutput(self.proc_id + ':qrcode [' + qr + ']')
                            #qFunc.logOutput(self.proc_id + ':version ' + str(((qrx.shape[0] - 21) / 4) + 1))

                            # 読取文字
                            if (read_text != ''):
                                qFunc.logOutput(self.proc_id + ':reader [' + read_text + ']')

                                # 結果出力
                                out_name  = '[txts]'
                                out_value = read_text.split('[cr]')
                                cn_s.put([out_name, out_value])
                                res_count += 1

                            # 読取画像
                            if (not read_img is None):

                                # 結果出力
                                out_name  = '[img]'
                                out_value = read_img.copy()
                                #out_value = cv2.resize(gray_img, (640,480))
                                cn_s.put([out_name, out_value])
                                res_count += 1

                                # ファイル出力
                                nowTime = datetime.datetime.now()
                                stamp = nowTime.strftime('%Y%m%d.%H%M%S')

                                fn1 = qPath_rec      + stamp + '.qrcode.jpg'
                                fn2 = qPath_v_detect + stamp + '.qrcode.jpg'
                                if (not os.path.exists(fn1)) and (not os.path.exists(fn2)):
                                    try:
                                        cv2.imwrite(fn1, read_img)
                                        cv2.imwrite(fn2, read_img)
                                    except:
                                        pass

                # 読取記録
                if (hit_count > 0):

                    fn3 = qPath_rec     + stamp + '.reader.jpg'
                    fn4 = qPath_v_photo + stamp + '.reader.jpg'
                    if (not os.path.exists(fn3)) and (not os.path.exists(fn4)):
                        try:
                            cv2.imwrite(fn3, image_img)
                            cv2.imwrite(fn4, image_img)
                        except:
                            pass

                # on 指令の自動解除
                for key in list(read_time):
                    if ((time.time() - read_time[key]) > 3):

                        # 自動解除
                        read_time.pop(key)
                        k=key[-4:]
                        if (key[-4:] == '_on_'):
                            read_text = key[:-4] + '_off_'
                            qFunc.logOutput(self.proc_id + ':reader [' + read_text + ']')

                            # 結果出力
                            out_name  = '[txts]'
                            out_value = [read_text]
                            cn_s.put([out_name, out_value])
                            res_count += 1

                # 無応答防止
                if (res_count == 0):

                    # 結果出力
                    out_name  = ''
                    out_value = ''
                    cn_s.put([out_name, out_value])

                time.sleep(0.50)



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0') or (str(self.id) == 'v'):
                qFunc.statusSet(qBusy_v_QR, False)
            if (str(self.id) == 'd'):
                qFunc.statusSet(qBusy_d_QR, False)

            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif (str(self.id) == '0') or (str(self.id) == 'v'):
                if ((qFunc.statusCheck(qBusy_dev_cam) == True) \
                 or (qFunc.statusCheck(qBusy_dev_dsp) == True)) \
                and (qFunc.statusCheck(qRdy__v_reader)  == False) \
                and (qFunc.statusCheck(qRdy__v_sendkey) == False):
                    slow = True
            elif (str(self.id) == 'd'):
                if  (qFunc.statusCheck(qBusy_dev_scn) == True) \
                and (qFunc.statusCheck(qRdy__d_reader)  == False) \
                and (qFunc.statusCheck(qRdy__d_sendkey) == False):
                    slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.50)
                else:
                    time.sleep(0.25)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0') or (str(self.id) == 'v'):
                qFunc.statusSet(qBusy_v_QR, False)
            if (str(self.id) == 'd'):
                qFunc.statusSet(qBusy_d_QR, False)

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
    cvreader_thread.begin()

    inp = cv2.imread('_photos/_photo_qrcode.jpg')
    cvreader_thread.put(['[img]', inp.copy()])

    chktime = time.time()
    while ((time.time() - chktime) < 15):
        res_data  = cvreader_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            elif (res_name == '[txts]'):
                print(res_name, res_value[0], )

        time.sleep(0.05)

    time.sleep(1.00)
    cvreader_thread.abort()
    del cvreader_thread



    cv2.destroyAllWindows()


