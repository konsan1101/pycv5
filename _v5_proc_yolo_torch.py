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

import torch 
import torch.nn as nn
from torch.autograd import Variable

import pickle as pkl
import random 

from yolo3_util import *
from yolo3_preprocess import prep_image, inp_to_image, letterbox_image
from yolo3_Darknet import Darknet



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS             = qFunc.getValue('qOS'            )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
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



class proc_yolo_torch:

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
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        # YOLO
        confidence = float(0.5)
        nms_thesh = float(0.45)
        CUDA = torch.cuda.is_available()
        num_classes = 80
        #CUDA = torch.cuda.is_available()
        bbox_attrs = 5 + num_classes
        
        print("Loading network.....")
        #model = Darknet('yolo3_weights/yolov3.cfg')
        #model.load_weights('yolo3_weights/yolov3.weights')
        #model.net_info["height"] = 416
        model = Darknet('yolo3_weights/yolov3-tiny.cfg')
        model.load_weights('yolo3_weights/yolov3-tiny.weights')
        model.net_info["height"] = 416
        print("Network successfully loaded")

        inp_dim = int(model.net_info["height"])
        assert inp_dim % 32 == 0 
        assert inp_dim > 32

        #If there's a GPU availible, put the model on GPU
        if CUDA:
            model.cuda()

        #Set the model in evaluation mode
        model.eval()

        classes = load_classes("yolo3_torch/data/coco.names")
        colors = pkl.load(open("yolo3_torch/data/pallete", "rb"))

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


                frame = inp_value.copy()

                orig_im = frame
                dim = orig_im.shape[1], orig_im.shape[0]
                img = (letterbox_image(orig_im, (inp_dim, inp_dim)))
                img_ = img[:,:,::-1].transpose((2,0,1)).copy()
                img2 = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
                img = img2

                im_dim = torch.FloatTensor(dim).repeat(1,2)

                if CUDA:
                    im_dim = im_dim.cuda()
                    img = img.cuda()
                
                with torch.no_grad():   
                    output = model(Variable(img), CUDA)

                output = write_results(output, confidence, num_classes, nms = True, nms_conf = nms_thesh)

                im_dim = im_dim.repeat(output.size(0), 1)
                scaling_factor = torch.min(inp_dim/im_dim,1)[0].view(-1,1)
                
                output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim[:,0].view(-1,1))/2
                output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim[:,1].view(-1,1))/2
                
                output[:,1:5] /= scaling_factor
        
                for i in range(output.shape[0]):
                    output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim[i,0])
                    output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim[i,1])
                                
                out_img = orig_im.copy()
                for detect in output:
                    try:
                        x1 = int(detect[1])
                        y1 = int(detect[2])
                        x2 = int(detect[3])
                        y2 = int(detect[4])
                        cl = int(detect[-1])
                        sc = float(detect[-2])

                        if ((x2-x1)>10) and ((y2-y1)>10):

                            label = '{} {:.2f}'.format(classes[cl], sc)
                            color = random.choice(colors)
                            #color = colors[ cl % len(colors) ]

                            cv2.rectangle(out_img, (x1, y1), (x2, y2), color, 2)

                            # 認識画像出力
                            if (classes[cl] == 'person') \
                            or (classes[cl] == 'car'):

                                # 結果出力
                                out_name  = '[array]'
                                out_value = orig_im[y1:y2, x1:x2].copy()
                                cn_s.put([out_name, out_value])

                        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
                        x2 = x1 + t_size[0] + 3
                        y1 = y2 - t_size[1] - 4
                        cv2.rectangle(out_img, (x1, y1), (x2, y2), color, -1)
                        cv2.putText(out_img, label, (x1, y1 + t_size[1] + 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)

                    except:
                        pass


                out_height, out_width = out_img.shape[:2]

                # ＦＰＳ計測
                fps = qFPS_class.get()
                if ((time.time() - qFPS_last) > 5):
                    qFPS_last  = time.time()

                    # 結果出力(fps)
                    out_name  = '_fps_'
                    out_value = '{:.2f}'.format(fps)
                    cn_s.put([out_name, out_value])

                    # 結果出力(reso)
                    out_name  = '_reso_'
                    out_value = str(out_width) + 'x' + str(out_height)
                    cn_s.put([out_name, out_value])

                # 結果出力
                out_name  = '[img]'
                out_value = out_img.copy()
                cn_s.put([out_name, out_value])

                #time.sleep(0.50)




            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # アイドリング
            if (qFunc.statusCheck(qBusy_dev_cpu, 0) == True) \
            or (qFunc.statusCheck(qBusy_dev_cam, 0) == True):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

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



    yolo_torch_thread = proc_yolo_torch('yolotorch', '0', )
    yolo_torch_thread.start()

    inp = cv2.imread('cv2dnn/dog.jpg')
    inp = cv2.resize(inp, (960, 540))

    chktime = time.time()
    while ((time.time() - chktime) < 120):

        if (yolo_torch_thread.proc_s.qsize() == 0):
            yolo_torch_thread.put(['[img]', inp.copy()])

        while (yolo_torch_thread.proc_r.qsize() != 0):
            res_data  = yolo_torch_thread.get()
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
    yolo_torch_thread.stop()
    del yolo_torch_thread



    cv2.destroyAllWindows()


