#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
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

qPLATFORM       = qFunc.getValue('qPLATFORM'      )
qRUNATTR        = qFunc.getValue('qRUNATTR'       )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
qPath_cache     = qFunc.getValue('qPath_cache'    )
qPath_sounds    = qFunc.getValue('qPath_sounds'   )
qPath_icons     = qFunc.getValue('qPath_icons'    )
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



class proc_camera:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    camDev='0', camMode='harf', camStretch='0', camRotate='0', camZoom='1.0', camFps='5', ):
        self.runMode    = runMode
        self.camDev     = camDev
        self.camMode    = camMode
        self.camStretch = camStretch
        self.camRotate  = camRotate
        self.camZoom    = camZoom
        self.camSquare  = '0.05' #面積1/20以上
        self.camFps     = '5'
        if (camFps.isdigit()):
            self.camFps = str(camFps)

        self.camWidth   = 0
        self.camHeight  = 0
        if (camMode != 'default') and (camMode != 'auto'):
            camWidth, camHeight = qFunc.getResolution(camMode)
            self.camWidth   = camWidth
            self.camHeight  = camHeight

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
        self.blue_img = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.blue_img,(0,0),(320,240),(255,0,0),-1)
        cv2.putText(self.blue_img, 'No Image !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

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

        # デバイス設定
        capture = None
        if (not self.camDev.isdigit()):
            capture = cv2.VideoCapture(self.camDev)

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

            # デバイス設定
            if (self.camDev.isdigit()):
                if (capture is None):
                    if ((qFunc.statusCheck(qBusy_dev_cam) == False) \
                    or  (qFunc.statusCheck(qRdy__v_sendkey) == True)):

                        if (os.name != 'nt'):
                            capture = cv2.VideoCapture(int(self.camDev))
                        else:
                            capture = cv2.VideoCapture(int(self.camDev), cv2.CAP_DSHOW)
                        try:
                            if (int(self.camWidth ) != 0):
                                capture.set(cv2.CAP_PROP_FRAME_WIDTH,  int(self.camWidth ))
                            if (int(self.camHeight) != 0):
                                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.camHeight))
                            if (int(self.camFps) != 0):
                                capture.set(cv2.CAP_PROP_FPS,          int(self.camFps   ))
                        except:
                            pass

                        # ビジー設定 (ready)
                        if (qFunc.statusCheck(self.fileBsy) == False):
                            qFunc.statusSet(self.fileBsy, True)
                            if (str(self.id) == '0'):
                                qFunc.statusSet(qBusy_v_inp, True)

                if  (not capture is None):
                    if ((qFunc.statusCheck(qBusy_dev_cam) == True) \
                    and (qFunc.statusCheck(qRdy__v_sendkey) == False)):
                        capture.release()
                        capture = None

                        # ビジー解除 (!ready)
                        qFunc.statusSet(self.fileBsy, False)
                        if (str(self.id) == '0'):
                            qFunc.statusSet(qBusy_v_inp, False)

            # レディ設定
            if (not capture is None) and (not os.path.exists(self.fileRdy)):
                qFunc.statusSet(self.fileRdy, True)
            if (capture is None) and (os.path.exists(self.fileRdy)):
                qFunc.statusSet(self.fileRdy, False)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                if (not capture is None):
                    out_value = '_ready_'
                else:
                    out_value = '!ready'
                cn_s.put([out_name, out_value])

            # 連携情報
            if (inp_name.lower() == '_camstretch_'):
                self.camStretch = inp_value
                qFPS_last = time.time() - 60
            if (inp_name.lower() == '_camrotate_'):
                self.camRotate = inp_value
                qFPS_last = time.time() - 60
            if (inp_name.lower() == '_camzoom_'):
                self.camZoom = inp_value
                qFPS_last = time.time() - 60



            # 画像処理
            if (cn_s.qsize() == 0):
            #if (True):

                # 画像取得
                if (not capture is None):
                    ret, frame = capture.read()
                else:
                    ret = True
                    frame = self.blue_img.copy()

                if (ret == False):
                    qFunc.logOutput(self.proc_id + ':capture error!', display=self.logDisp,)
                    time.sleep(5.00)
                    self.proc_step = '9'
                    break

                else:

                    # 実行カウンタ
                    self.proc_last = time.time()
                    self.proc_seq += 1
                    if (self.proc_seq > 9999):
                        self.proc_seq = 1

                    # frame_img
                    frame_img = frame.copy()
                    frame_height, frame_width = frame_img.shape[:2]
                    input_img = frame.copy()
                    input_height, input_width = input_img.shape[:2]

                    # 台形補正
                    if (int(self.camStretch) != 0):
                        x = int((input_width/2) * abs(int(self.camStretch))/100)
                        if (int(self.camStretch) > 0):
                            perspective1 = np.float32([ [x, 0], [input_width-x, 0], [input_width, input_height], [0, input_height] ])
                        else:
                            perspective1 = np.float32([ [0, 0], [input_width, 0], [input_width-x, input_height], [x, input_height] ])
                        perspective2 = np.float32([ [0, 0], [input_width, 0], [input_width, input_height], [0, input_height] ])
                        transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                        input_img = cv2.warpPerspective(input_img, transform_matrix, (input_width, input_height))

                    # 画像回転
                    if   (int(self.camRotate) == -180):
                        input_img = cv2.flip(input_img, 0) # 180 Rotation Y
                    elif (int(self.camRotate) == -360):
                        input_img = cv2.flip(input_img, 1) # 180 Rotation X
                    elif (abs(int(self.camRotate)) !=   0):
                        width2    = int((input_width - input_height)/2)
                        rect_img  = cv2.resize(input_img[0:input_height, width2:width2+input_height], (960,960))
                        rect_mat  = cv2.getRotationMatrix2D((480, 480), -int(self.camRotate), 1.0)
                        rect_r    = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        input_img = cv2.resize(rect_r, (input_height, input_height))
                        input_height, input_width = input_img.shape[:2]

                    # ズーム
                    if (float(self.camZoom) != 1):
                        zm = float(self.camZoom)
                        x1 = int((input_width-(input_width/zm))/2)
                        x2 = input_width - x1
                        y1 = int((input_height-(input_height/zm))/2)
                        y2 = input_height - y1
                        zm_img = input_img[y1:y2, x1:x2]
                        input_img = zm_img.copy()
                        input_height, input_width = input_img.shape[:2]

                    # 4角形補足
                    if (float(self.camSquare) != 0):
                        if (self.runMode == 'debug') \
                        or (self.runMode == 'camera'):
                            if  (qFunc.statusCheck(qBusy_d_rec) == False):

                                square_contours = []
                                gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

                                # 0:黒字に白、1:白地に黒
                                for bw in range(2):

                                    # 画像補正
                                    if (bw == 0):
                                        _, thresh = cv2.threshold(gray, 192, 255, cv2.THRESH_BINARY_INV)
                                    else:
                                        gray2 = cv2.bitwise_not(gray)
                                        _, thresh = cv2.threshold(gray2, 192, 255, cv2.THRESH_BINARY_INV)
                                    thresh_not = cv2.bitwise_not(thresh)

                                    # 輪郭抽出・幾何図形取得（黒字に白）
                                    contours, hierarchy = cv2.findContours(thresh_not, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                    for i, cnt in enumerate(contours):

                                        # 面積で選別
                                        area = cv2.contourArea(cnt)
                                        if (area > ((input_height * input_width) * float(self.camSquare))):

                                            # 輪郭長さで輪郭を近似化する。
                                            arclen = cv2.arcLength(cnt, True)
                                            epsilon_len = arclen * 0.05
                                            approx_cnt = cv2.approxPolyDP(cnt, epsilon=epsilon_len, closed=True)

                                            # 画数で選別
                                            if (len(approx_cnt) == 4):

                                                # 座標ずらす
                                                x = np.array([])
                                                y = np.array([])
                                                for i in range(4):
                                                    x = np.append(x, approx_cnt[i][0][0])
                                                    y = np.append(y, approx_cnt[i][0][1])
                                                ave_x = np.mean(x)
                                                ave_y = np.mean(y)

                                                hit1 = False
                                                hit2 = False
                                                hit3 = False
                                                hit4 = False
                                                for i in range(4):
                                                    if (x[i] <= ave_x) and (y[i] <= ave_y):
                                                        hit1 = True
                                                        approx_cnt[0][0][0]=x[i]
                                                        approx_cnt[0][0][1]=y[i]
                                                    if (x[i] <= ave_x) and (y[i] > ave_y):
                                                        hit2 = True
                                                        approx_cnt[1][0][0]=x[i]
                                                        approx_cnt[1][0][1]=y[i]
                                                    if (x[i] > ave_x) and (y[i] > ave_y):
                                                        hit3 = True
                                                        approx_cnt[2][0][0]=x[i]
                                                        approx_cnt[2][0][1]=y[i]
                                                    if (x[i] > ave_x) and (y[i] <= ave_y):
                                                        hit4 = True
                                                        approx_cnt[3][0][0]=x[i]
                                                        approx_cnt[3][0][1]=y[i]

                                                if  (hit1 == True) and (hit2 == True) \
                                                and (hit3 == True) and (hit4 == True):
                                                    square_contours.append(approx_cnt)

                                # 4角形透過変換
                                for i, cnt in enumerate(square_contours):

                                    # 輪郭に外接する長方形を取得する。
                                    x, y, width, height = cv2.boundingRect(cnt)

                                    # 透過変換
                                    dst = []
                                    pts1 = np.float32(cnt)
                                    pts2 = np.float32([[0,0],[0,height],[width,height],[width,0]])

                                    M = cv2.getPerspectiveTransform(pts1,pts2)
                                    dst = cv2.warpPerspective(input_img,M,(width,height))

                                    #input_img = dst.copy()

                                    # オーバーレイ
                                    over_x = x
                                    over_y = y
                                    over_img = dst.copy()
                                    over_height, over_width = over_img.shape[:2]

                                    if  (over_x >=0) and (over_y >=0) \
                                    and ((over_x + over_width) < input_width) \
                                    and ((over_y + over_height) < input_height):
                                        input_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                                        cv2.rectangle(input_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)



                    # ＦＰＳ計測
                    fps = qFPS_class.get()
                    if ((time.time() - qFPS_last) > 5):
                        qFPS_last  = time.time()

                        # 結果出力(fps)
                        out_name  = '_fps_'
                        out_value = '{:.1f}'.format(fps)
                        cn_s.put([out_name, out_value])

                        # 結果出力(reso)
                        out_name  = '_reso_'
                        out_value = str(input_width) + 'x' + str(input_height)
                        if (float(self.camZoom) != 1):
                            out_value += ' (Zoom=' + self.camZoom + ')'
                        cn_s.put([out_name, out_value])

                    # 結果出力
                    if (cn_s.qsize() == 0):
                        out_name  = '[img]'
                        out_value = input_img.copy()
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
                time.sleep((1/int(self.camFps))/2)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # デバイス開放
            if (not capture is None): 
                capture.release()
                capture = None

            # ビジー解除 (!ready)
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_v_inp, False)

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

    #camDev='http://192.168.200.250/nphMotionJpeg?Resolution=640x480'
    camDev='0'
    camera_thread = proc_camera(name='camera', id='0', runMode='debug', 
                    camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='5',)
    camera_thread.begin()

    chktime = time.time()
    while ((time.time() - chktime) < 15):

        res_data  = camera_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
            else:
                print(res_name, res_value, )

        #if (camera_thread.proc_s.qsize() == 0):
        #    camera_thread.put(['_status_', ''])

        time.sleep(0.02)

    time.sleep(1.00)
    camera_thread.abort()
    del camera_thread



    cv2.destroyAllWindows()



