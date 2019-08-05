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



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS            = qFunc.getValue('qOS'           )
qHOSTNAME      = qFunc.getValue('qHOSTNAME'     )
qPath_log      = qFunc.getValue('qPath_log'     )
qPath_work     = qFunc.getValue('qPath_work'    )
qPath_rec      = qFunc.getValue('qPath_rec'     )

qPath_s_ctrl   = qFunc.getValue('qPath_s_ctrl'  )
qPath_s_inp    = qFunc.getValue('qPath_s_inp'   )
qPath_s_wav    = qFunc.getValue('qPath_s_wav'   )
qPath_s_jul    = qFunc.getValue('qPath_s_jul'   )
qPath_s_STT    = qFunc.getValue('qPath_s_STT'   )
qPath_s_TTS    = qFunc.getValue('qPath_s_TTS'   )
qPath_s_TRA    = qFunc.getValue('qPath_s_TRA'   )
qPath_s_play   = qFunc.getValue('qPath_s_play'  )
qPath_v_ctrl   = qFunc.getValue('qPath_v_ctrl'  )
qPath_v_inp    = qFunc.getValue('qPath_v_inp'   )
qPath_v_jpg    = qFunc.getValue('qPath_v_jpg'   )
qPath_v_detect = qFunc.getValue('qPath_v_detect')
qPath_v_cv     = qFunc.getValue('qPath_v_cv'    )
qPath_v_photo  = qFunc.getValue('qPath_v_photo' )
qPath_v_msg    = qFunc.getValue('qPath_v_msg'   )
qPath_d_ctrl   = qFunc.getValue('qPath_d_ctrl'  )
qPath_d_prtscn = qFunc.getValue('qPath_d_prtscn')
qPath_d_movie  = qFunc.getValue('qPath_d_movie' )
qPath_d_play   = qFunc.getValue('qPath_d_play' )

qBusy_dev_cpu  = qFunc.getValue('qBusy_dev_cpu' )
qBusy_dev_com  = qFunc.getValue('qBusy_dev_com' )
qBusy_dev_mic  = qFunc.getValue('qBusy_dev_mic' )
qBusy_dev_spk  = qFunc.getValue('qBusy_dev_spk' )
qBusy_dev_cam  = qFunc.getValue('qBusy_dev_cam' )
qBusy_dev_dsp  = qFunc.getValue('qBusy_dev_dsp' )
qBusy_s_ctrl   = qFunc.getValue('qBusy_s_ctrl'  )
qBusy_s_inp    = qFunc.getValue('qBusy_s_inp'   )
qBusy_s_wav    = qFunc.getValue('qBusy_s_wav'   )
qBusy_s_STT    = qFunc.getValue('qBusy_s_STT'   )
qBusy_s_TTS    = qFunc.getValue('qBusy_s_TTS'   )
qBusy_s_TRA    = qFunc.getValue('qBusy_s_TRA'   )
qBusy_s_play   = qFunc.getValue('qBusy_s_play'  )
qBusy_v_ctrl   = qFunc.getValue('qBusy_v_ctrl'  )
qBusy_v_inp    = qFunc.getValue('qBusy_v_inp'   )
qBusy_v_QR     = qFunc.getValue('qBusy_v_QR'    )
qBusy_v_jpg    = qFunc.getValue('qBusy_v_jpg'   )
qBusy_v_CV     = qFunc.getValue('qBusy_v_CV'    )
qBusy_d_ctrl   = qFunc.getValue('qBusy_d_ctrl'  )
qBusy_d_inp    = qFunc.getValue('qBusy_d_inp'   )
qBusy_d_QR     = qFunc.getValue('qBusy_d_QR'    )
qBusy_d_rec    = qFunc.getValue('qBusy_d_rec'   )
qBusy_d_play   = qFunc.getValue('qBusy_d_play'  )
qBusy_d_web    = qFunc.getValue('qBusy_d_web'   )



class proc_julius:

    def __init__(self, name='thread', id='00', runMode='debug', ):
        self.runMode   = runMode

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-3] + '_{:02}'.format(int(id))
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

        fileLog = qPath_work + self.proc_id + '.log'
        qFunc.remove(fileLog)

        portId  = str(5500 + int(self.id))

        # julius 起動
        if (self.runMode == 'number'):
            if (os.name == 'nt'):
                julius = subprocess.Popen(['julius', '-input', 'adinnet', '-adport', portId, \
                                        '-C', 'julius/_jconf_20180313dnn999.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                        '-charconv', 'utf-8', 'sjis', '-logfile', fileLog, '-quiet', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
            else:
                julius = subprocess.Popen(['julius', '-input', 'adinnet', '-adport', portId, \
                                        '-C', 'julius/_jconf_20180313dnn999.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                        '-logfile', fileLog, '-quiet', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
        else:
            if (os.name == 'nt'):
                julius = subprocess.Popen(['julius', '-input', 'adinnet', '-adport', portId, \
                                        '-C', 'julius/_jconf_20180313dnn.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                        '-charconv', 'utf-8', 'sjis', '-logfile', fileLog, '-quiet', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
            else:
                julius = subprocess.Popen(['julius', '-input', 'adinnet', '-adport', portId, \
                                        '-C', 'julius/_jconf_20180313dnn.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                        '-logfile', fileLog, '-quiet', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
        time.sleep(0.50)

        # julius 待機
        chktime = time.time()
        chkhit  = ''
        while ((time.time() - chktime) < 5):
            t = julius.stdout.readline()
            t = t.replace('\r', '')
            t = t.replace('\n', '')
            #print('julius:' + str(t))
            if t != '':
                chkhit = t
            else:
                if chkhit != '':
                    break
            time.sleep(0.01)
            chktime = time.time()

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

            # レディー設定
            if (not os.path.exists(self.fileRdy)):
                qFunc.txtsWrite(self.fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )
                qFunc.logOutput(self.proc_id + ':ready', display=self.logDisp,)

            # 処理
            if (inp_name.lower() == 'filename'):
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ログ
                # qFunc.logOutput(self.proc_id + ':' + str(inp_name) + ' , ' + str(inp_value), display=self.logDisp, )

                # ビジー設定
                if (not os.path.exists(self.fileBsy)):
                    qFunc.txtsWrite(self.fileBsy, txts=[inp_value], encoding='utf-8', exclusive=False, mode='a', )

                # lst ファイル用意
                fileLst = qPath_work + self.proc_id + '.{:04}'.format(self.proc_seq) + '.lst'
                qFunc.txtsWrite(fileLst, txts=[inp_value], encoding='utf-8', exclusive=False, mode='w', )
                
                # adintool 起動
                adintool = subprocess.Popen(['adintool', '-input', 'file', '-filelist', fileLst, \
                                            '-out', 'adinnet', '-server', 'localhost', '-port', portId, '-nosegment',], \
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, )
                adintool.wait()
                adintool.terminate()
                qFunc.remove(fileLst)

                # julius 待機
                jultxt  = ''

                chktime = time.time()
                chkhit  = ''
                while ((time.time() - chktime) < 5):
                    t = julius.stdout.readline()
                    t = t.replace('\r', '')
                    t = t.replace('\n', '')
                    #print('julius:' + str(t))
                    if t != '':
                        chkhit = t
                        if t[:15]=='<search failed>':
                            jultxt = ' '
                        if t[:10]=='sentence1:':
                            jultxt = t[10:]
                    else:
                        if chkhit != '':
                            break
                    time.sleep(0.01)
                    chktime = time.time()

                    jultxt = jultxt.strip()
                    jultxt = jultxt.replace(u'　', '')
                    jultxt = jultxt.replace(u'。', '')
                    jultxt = jultxt.replace(' ', '')

                # 結果出力
                if (jultxt == ''):
                    jultxt = '!'
                out_name  = '[txts]'
                out_value = jultxt
                cn_s.put([out_name, [out_value]])

                if (self.runMode=='debug'):
                    qFunc.logOutput(self.proc_id + ':' + str(out_name) + ', ' + str(out_value), display=self.logDisp, )
                else:
                    #qFunc.logOutput(' ' + self.proc_id + ':Recognize /' + str(out_value) + '/ ja (julius) pass!', display=True, )
                    pass

                # txt ファイル出力
                fileTxt = inp_value[:-4] + '.txt'
                fileTxt = fileTxt.replace(qPath_work, '')
                fileTxt = fileTxt.replace(qPath_rec,  '')
                fileTxt = fileTxt.replace(qPath_s_wav,  '')
                fileTxt = fileTxt.replace(qPath_s_jul,  '')
                fileTxt = qPath_s_jul + fileTxt
                qFunc.txtsWrite(fileTxt, txts=[jultxt], encoding='utf-8', exclusive=True, mode='w', )

            # ビジー解除
            qFunc.remove(self.fileBsy)

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

            # julius 終了
            julius.terminate()

            # ビジー解除
            qFunc.remove(self.fileBsy)

            # レディー解除
            qFunc.remove(self.fileRdy)

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

    qFunc.kill('julius')
    qFunc.kill('adintool')



    julius_thread = proc_julius('julius', '00', )
    julius_thread.start()
    time.sleep(3.00)

    for _ in range(3):
        julius_thread.put(['filename', '_sounds/_sound_hallo.wav'])
        res_data  = julius_thread.checkGet()

    time.sleep(1.00)
    julius_thread.stop()
    del julius_thread



    qFunc.kill('julius')
    qFunc.kill('adintool')


