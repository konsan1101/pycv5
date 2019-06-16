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



class proc_adintool:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='on', micLevel='777', ):

        self.path      = qPath_a_inp

        self.runMode   = runMode
        self.micDev    = micDev
        self.micType   = micType
        self.micGuide  = micGuide
        self.micLevel  = micLevel

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

        adin_rewind   = '555'
        adin_headmg   = '333'
        adin_tailmg   = '444'
        vadLevel      = '1'
        if (self.micLevel == '1'):
            vadLevel  = '3'

        adintool_exe = None
        adintool_gui = None

        # ガイド音
        if (self.micGuide != 'off'):
            qFunc.guide('_up')

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
                out_value = '!ready'
                if (not adintool_exe is None):
                    files = glob.glob(self.path + '*')
                    if (len(files) == 0):
                        out_value = 'ready'
                    else:
                        out_value = 'busy'

                cn_s.put([out_name, out_value])



            # 処理
            if (True):

                # on ?
                sw = 'off'
                if  (qFunc.busyCheck(qBusy_dev_mic, 1) != 'busy'):
                    if (self.micDev.isdigit()):
                        if (self.micType == 'usb'):
                                sw = 'on'
                        else:
                            if  (qFunc.busyCheck(qBusy_a_ctrl,  1) != 'busy') \
                            and (qFunc.busyCheck(qBusy_a_wav,   1) != 'busy') \
                            and (qFunc.busyCheck(qBusy_a_STT,   1) != 'busy') \
                            and (qFunc.busyCheck(qBusy_a_TTS,   1) != 'busy') \
                            and (qFunc.busyCheck(qBusy_a_TRA,   1) != 'busy') \
                            and (qFunc.busyCheck(qBusy_a_play,  1) != 'busy'):
                                sw = 'on'

                # off -> on
                if (sw == 'on'):
                    if (adintool_exe is None):

                        # 実行カウンタ
                        self.proc_last = time.time()
                        self.proc_seq += 1
                        if (self.proc_seq > 9999):
                            self.proc_seq = 1

                        # ビジー設定 (ready)
                        if (not os.path.exists(fileBsy)):
                            qFunc.txtsWrite(fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )
                        if (str(self.id) == '0'):
                            qFunc.busySet(qBusy_a_inp, True)

                        # ガイド音
                        if (self.micGuide == 'on' or self.micGuide == 'sound'):
                            qFunc.guide('_ready')

                        if (True):
                            nowTime = datetime.datetime.now()
                            filename = self.path + nowTime.strftime('%Y%m%d.%H%M%S') +'.adintool'
                            adintool_exe = subprocess.Popen(['adintool', '-in', 'mic', \
                                            '-rewind', adin_rewind, '-headmargin', adin_headmg, '-tailmargin', adin_tailmg, \
                                            '-fvad', vadLevel, '-lv', self.micLevel, \
                                            '-out', 'file', '-filename', filename, '-startid', '5001', ] , \
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    if (adintool_gui is None) and (os.name == 'nt'):
                        if (self.micGuide == 'on' or self.micGuide == 'display'):
                            adintool_gui = subprocess.Popen(['adintool-gui', '-in', 'mic', \
                                            '-rewind', adin_rewind, '-headmargin', adin_headmg, '-tailmargin', adin_tailmg, \
                                            '-lv', self.micLevel,] , \
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                # off, accept ?
                sw = 'on'
                if (qFunc.busyCheck(qBusy_dev_mic, 0) == 'busy'):
                        sw = 'off'
                if (self.micType == 'bluetooth'):
                    if (qFunc.busyCheck(qBusy_a_ctrl,  0) == 'busy') \
                    or (qFunc.busyCheck(qBusy_a_wav,   0) == 'busy') \
                    or (qFunc.busyCheck(qBusy_a_STT,   0) == 'busy') \
                    or (qFunc.busyCheck(qBusy_a_TTS,   0) == 'busy') \
                    or (qFunc.busyCheck(qBusy_a_TRA,   0) == 'busy') \
                    or (qFunc.busyCheck(qBusy_a_play,  0) == 'busy'):
                        sw = 'off'
                if (not adintool_exe is None):
                    files = glob.glob(self.path + '*')
                    if (len(files) > 0):
                        chktime = time.time()
                        while (len(files) > 0) and ((time.time() - chktime) < 2):
                            time.sleep(0.20)
                            files = glob.glob(self.path + '*')
                        if (len(files) == 0):
                            sw = 'accept'

                # on -> off, accept
                if (sw == 'off') or (sw == 'accept'):

                    # adintool 終了
                    if (not adintool_gui is None):
                        adintool_gui.terminate()
                        adintool_gui = None

                    if (self.micType == 'bluetooth'):

                        # adintool 終了
                        if (not adintool_exe is None):
                            adintool_exe.terminate()
                            adintool_exe = None

                        # ビジー解除 (!ready)
                        qFunc.remove(fileBsy)
                        if (str(self.id) == '0'):
                            qFunc.busySet(qBusy_a_inp, False)

                    # ガイド音
                    if (sw == 'accept'):
                        if (self.micGuide == 'on') or (self.micGuide == 'sound'):
                            qFunc.guide('_accept')

                            if (self.runMode == 'debug') \
                            or (self.runMode == 'handsfree') \
                            or (self.runMode == 'translator'):
                                time.sleep(4.00)



            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_mic, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # adintool 終了
            if (not adintool_gui is None):
                adintool_gui.terminate()
                adintool_gui = None

            if (not adintool_exe is None):
                adintool_exe.terminate()
                adintool_exe = None

            # ビジー解除 (!ready)
            qFunc.remove(fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_a_inp, False)

            # ガイド音
            if (self.micGuide != 'off'):
                qFunc.guide('_down')

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

    qFunc.busySet(qBusy_a_ctrl,  False)
    qFunc.busySet(qBusy_a_inp,   False)
    qFunc.busySet(qBusy_a_wav,   False)
    qFunc.busySet(qBusy_a_STT,   False)
    qFunc.busySet(qBusy_a_TTS,   False)
    qFunc.busySet(qBusy_a_TRA,   False)
    qFunc.busySet(qBusy_a_play,  False)

    qFunc.kill('adintool')
    qFunc.kill('adintool-gui')



    adintool_thread = proc_adintool('adintool', '0', )
    adintool_thread.start()

    chktime = time.time()
    while (int(time.time() - chktime) < 15):

        res_data  = adintool_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (adintool_thread.proc_s.qsize() == 0):
            adintool_thread.put(['status', ''])

        time.sleep(0.05)

    time.sleep(1.00)
    adintool_thread.stop()
    del adintool_thread



    qFunc.kill('adintool')
    qFunc.kill('adintool-gui')


