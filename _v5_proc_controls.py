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



# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_chatting   = 'temp/control_chatting.txt'
qCtrl_control_knowledge  = 'temp/control_knowledge.txt'



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



class proc_controls:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='on', micLevel='777',  ):

        self.path      = qPath_s_ctrl

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

        # 変数
        self.run_vision    = True
        self.run_desktop   = True
        self.run_bgm       = True
        self.run_browser   = True
        self.run_player    = True
        self.run_chatting  = True
        self.run_knowledge = True

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
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])



            # 処理
            path = self.path
            path_files = glob.glob(path + '*.txt')
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

                        if (proc_file[-4:].lower() == '.txt' and proc_file[-8:].lower() != '.wrk.txt'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.txt'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.txt'):
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
                            work_file = qPath_work + work_name + '.txt'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            if (proc_file[-9:].lower() != '_sjis.txt'):
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='utf-8', exclusive=False, )
                            else:
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='shift_jis', exclusive=False, )
                            if (proc_text != '') and (proc_text != '!'):
                                qFunc.txtsWrite(work_file, txts=[proc_text], encoding='utf-8', exclusive=False, mode='w', )

                            if (os.path.exists(work_file)):

                                qFunc.remove(proc_file)

                                # ログ
                                #if (self.runMode == 'debug') or (not self.micDev.isdigit()):
                                #    qFunc.logOutput(self.proc_id + ':' + proc_name + u' → ' + work_name, display=self.logDisp,)

                                # 結果出力
                                if (cn_s.qsize() < 99):
                                    out_name  = '[txts]'
                                    out_value = proc_txts
                                    cn_s.put([out_name, out_value])

                                # ビジー設定
                                if (not os.path.exists(self.fileBsy)):
                                    qFunc.txtsWrite(self.fileBsy, txts=['_busy_'], encoding='utf-8', exclusive=False, mode='a', )
                                    if (str(self.id) == '0'):
                                        qFunc.busySet(qBusy_s_ctrl, True)

                                    #qFunc.busyCheck(qBusy_s_ctrl , 3)
                                    #qFunc.busyCheck(qBusy_s_STT  , 3)
                                    #qFunc.busyCheck(qBusy_s_TTS  , 3)
                                    #qFunc.busyCheck(qBusy_s_play , 3)
                                    if (self.micType == 'bluetooth') or (self.micGuide == 'on' or self.micGuide == 'sound'):
                                        qFunc.busyCheck(qBusy_s_inp , 3)

                                # 処理
                                self.proc_last = time.time()
                                self.sub_proc(seq4, proc_file, work_file, proc_name, proc_text, cn_s, )

                #except:
                #    pass

                time.sleep(0.50)



            # ビジー解除
            qFunc.remove(self.fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_s_ctrl, False)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == '_busy_'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.50)
            else:
                time.sleep(0.25)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(self.fileRdy)

            # ビジー解除
            qFunc.remove(self.fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_s_ctrl, False)

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



    def sub_proc(self, seq4, proc_file, work_file, proc_name, proc_text, cn_s, ):

        # インターフェース
        #if (self.run_vision    == True):
        #    qFunc.txtsWrite(qCtrl_control_vision   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_desktop   == True):
        #    qFunc.txtsWrite(qCtrl_control_desktop  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_bgm       == True):
            qFunc.txtsWrite(qCtrl_control_bgm       ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_browser   == True):
            qFunc.txtsWrite(qCtrl_control_browser   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_player    == True):
            qFunc.txtsWrite(qCtrl_control_player    ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_chatting  == True):
            qFunc.txtsWrite(qCtrl_control_chatting  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_knowledge == True):
            qFunc.txtsWrite(qCtrl_control_knowledge ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )

        if (cn_s.qsize() < 99):

            if (proc_text.find(u'リセット') >= 0):
                out_name  = 'control'
                out_value = '_reset_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_main   , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_vision , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_desktop, txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            elif ((proc_text.find(u'システム') >= 0) and (proc_text.find(u'終了') >= 0)) \
            or    (proc_text == u'バルス'):
                out_name  = 'control'
                out_value = '_end_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_main ,txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            elif ((proc_text.find(u'画面') >= 0) and (proc_text.find(u'開始') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True
                chktime = time.time()
                while (os.path.exists(qCtrl_control_main)) and ((time.time() - chktime) < 5):
                    time.sleep(0.50)
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = True

            elif ((proc_text.find(u'画面') >= 0) and (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = False
                chktime = time.time()
                while (os.path.exists(qCtrl_control_main)) and ((time.time() - chktime) < 5):
                    time.sleep(0.50)
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = False

            elif ((proc_text.find(u'ビジョン') >= 0) and (proc_text.find(u'開始') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = True

            elif ((proc_text.find(u'ビジョン') >= 0) and (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = False

            elif ((proc_text.find(u'デスクトップ') >= 0) and (proc_text.find(u'開始') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True

            elif ((proc_text.find(u'デスクトップ') >= 0) and (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = False

            elif ((proc_text.find(u'ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and (proc_text.find(u'開始') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_bgm_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = True

            elif ((proc_text.find(u'ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_bgm_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False

            elif ((proc_text.find(u'ウェブ') >= 0) or (proc_text.find(u'ブラウザ') >= 0)) \
            and (proc_text.find(u'開始') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_browser_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = True

            elif ((proc_text.find(u'ウェブ') >= 0) or (proc_text.find(u'ブラウザ') >= 0)) \
            and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_browser_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False

            elif ((proc_text.find(u'動画') >= 0) and (proc_text.find(u'開始') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_player_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = True
                time.sleep(5)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_test'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player  = False

            elif ((proc_text.find(u'動画') >= 0) and (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_player_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = False

            elif ((proc_text.find(u'チャット') >= 0) or (proc_text.find(u'雑談') >= 0)) \
            and (proc_text.find(u'開始') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_chatting_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_chatting = True

            elif ((proc_text.find(u'チャット') >= 0) or (proc_text.find(u'雑談') >= 0)) \
            and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_chatting_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_chatting = False

            elif ((proc_text.find(u'知識') >= 0) and (proc_text.find(u'開始') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_knowledge_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_knowledge = True

            elif ((proc_text.find(u'知識') >= 0) and (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_main ,txts=['_knowledge_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_knowledge = False



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )



    controls_thread = proc_controls('controls', '0', )
    controls_thread.start()

    chktime = time.time()
    while ((time.time() - chktime) < 15):

        res_data  = controls_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (controls_thread.proc_s.qsize() == 0):
            controls_thread.put(['_status_', ''])

        time.sleep(0.05)

    time.sleep(1.00)
    controls_thread.stop()
    del controls_thread


