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



class proc_vin2jpg:

    def __init__(self, name='thread', id='0', runMode='debug', 
        camDev='0', ):

        self.path      = qPath_v_inp

        self.runMode   = runMode
        self.camDev    = camDev

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



            # 処理
            if (True):

                path = self.path
                path_files = glob.glob(path + '*')
                if (len(path_files) > 0):

                    #try:
                    if (True):

                        for f in path_files:

                            # 停止要求確認
                            if (self.breakFlag.is_set()):
                                self.breakFlag.clear()
                                self.proc_step = '9'
                                break

                            proc_file = f.replace('\\', '/')

                            if (proc_file[-4:].lower() == '.jpg' and proc_file[-8:].lower() != '.wrk.jpg'):
                                f1 = proc_file
                                f2 = proc_file[:-4] + '.wrk.jpg'
                                try:
                                    os.rename(f1, f2)
                                    proc_file = f2
                                except:
                                    pass

                            if (proc_file[-8:].lower() == '.wrk.jpg'):
                                f1 = proc_file
                                f2 = proc_file[:-8] + proc_file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    proc_file = f2
                                except:
                                    pass

                                # 実行カウンタ
                                self.proc_last = time.time()
                                self.proc_seq += 1
                                if (self.proc_seq > 9999):
                                    self.proc_seq = 1
                                seq4 = '{:04}'.format(self.proc_seq)
                                seq2 = '{:02}'.format(self.proc_seq)

                                proc_name = proc_file.replace(path, '')
                                proc_name = proc_name[:-4]

                                work_name = self.proc_id + '.' + seq2
                                work_file = qPath_work + work_name + '.jpg'
                                if (os.path.exists(work_file)):
                                    os.remove(work_file)

                                shutil.copy2(proc_file, work_file, )

                                if (os.path.exists(work_file)):

                                    if (self.camDev.isdigit()):
                                        os.remove(proc_file)

                                    # ログ
                                    if (self.runMode == 'debug') or (not self.camDev.isdigit()):
                                        qFunc.logOutput(self.proc_id + ':' + proc_name + u' → ' + work_name, display=self.logDisp,)

                                    # ビジー設定
                                    if (not os.path.exists(fileBsy)):
                                        qFunc.txtsWrite(fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )
                                        if (str(self.id) == '0'):
                                            qFunc.busySet(qBusy_v_jpg, True)

                                    # ＡＩ処理
                                    self.proc_last = time.time()
                                    self.sub_proc(seq4, proc_file, work_file, cn_s, )

                                    time.sleep(0.50)

                    #except:
                    #    pass



            # ビジー解除
            qFunc.remove(fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_v_jpg, False)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_cam, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # ビジー解除
            qFunc.remove(fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_v_jpg, False)

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



    def sub_proc(self, seq4, proc_file, work_file, cn_s, ):

        # 結果出力
        if (cn_s.qsize() < 99):
            out_name  = 'filename'
            out_value = work_file
            cn_s.put([out_name, out_value])

        # コピー
        filename = proc_file
        filename = filename.replace(qPath_v_inp, '')
        filename = filename.replace(qPath_v_jpg, '')
        filename = filename.replace(qPath_work,  '')
        filename = qPath_v_jpg + filename
        shutil.copy2(work_file, filename, )



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )



    vin2jpg_thread = proc_vin2jpg('vin2jpg', '0', )
    vin2jpg_thread.start()

    shutil.copy2('vision__cv_qrcode.jpg', qPath_v_inp + 'vision__cv_qrcode.jpg')
    shutil.copy2('vision__ocr_photo.jpg', qPath_v_inp + 'vision__ocr_photo.jpg')

    chktime = time.time()
    while (int(time.time() - chktime) < 15):

        res_data  = vin2jpg_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (vin2jpg_thread.proc_s.qsize() == 0):
            vin2jpg_thread.put(['status', ''])

        time.sleep(0.05)

    time.sleep(1.00)
    vin2jpg_thread.stop()
    del vin2jpg_thread


