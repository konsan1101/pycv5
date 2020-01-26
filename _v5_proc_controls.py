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

import pyautogui



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
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
        self.last_text     = ''
        self.last_time     = time.time()

        self.run_vision    = True
        self.run_desktop   = True
        self.run_bgm       = True
        self.run_browser   = True
        self.run_player    = True
        self.run_chatting  = True
        self.run_knowledge = True

        # フォース
        self.force_last    = 0

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
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # フォース リセット
            if (qFunc.statusCheck(qRdy__s_force) == False):
                if (self.force_last != 0):
                    self.force_last  = 0
            else:
                if (self.force_last == 0):
                    self.force_last  = time.time()

            # フォース 自動終了（有効１０秒）
            if (qFunc.statusCheck(qRdy__s_force) == True):
                if ((time.time() - self.force_last) > 10):
                    qFunc.statusSet(qRdy__s_force, False)
                    qFunc.statusSet(qRdy__s_fproc, False)
                    self.force_last  = 0

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
                                if (qFunc.statusCheck(self.fileBsy) == False):
                                    qFunc.statusSet(self.fileBsy, True)
                                    if (str(self.id) == '0'):
                                        qFunc.statusSet(qBusy_s_ctrl, True)

                                    if (self.micType == 'bluetooth') or (self.micGuide == 'on' or self.micGuide == 'sound'):
                                        qFunc.statusWait_false(qBusy_s_inp , 3)

                                # フォース 覚醒
                                force = False
                                if (qFunc.checkWakeUpWord(proc_text) == True):
                                    if (qFunc.statusCheck(qRdy__s_force) == False):
                                        qFunc.statusSet(qRdy__s_force, True)
                                        qFunc.statusSet(qRdy__s_fproc, True)
                                        force = True

                                # フォース 状態
                                if  (qFunc.statusCheck(qRdy__s_force) == False) \
                                and (qFunc.statusCheck(qRdy__s_fproc) == True):
                                    force = True

                                # フォース リセット
                                if (qFunc.statusCheck(qRdy__s_force) == False):
                                    if (self.force_last != 0):
                                        self.force_last  = 0
                                else:
                                    if (self.force_last == 0):
                                        self.force_last  = time.time()

                                # 処理
                                self.proc_last = time.time()
                                self.sub_proc(seq4, proc_file, work_file, proc_name, proc_text, force, cn_s, )

                                # フォース 終了
                                if  (qFunc.statusCheck(qRdy__s_force) == False):
                                    qFunc.statusSet(qRdy__s_fproc, False)

                #except:
                #    pass



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_ctrl, False)

            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.25)
                else:
                    time.sleep(0.10)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_ctrl, False)

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



    def sub_proc(self, seq4, proc_file, work_file, proc_name, proc_text, force, cn_s, ):

        jp_true = qFunc.in_japanese(proc_text)
        if (proc_text == self.last_text) and ((time.time() - self.last_time) < 15):
            word_true = False
        else:
            word_true = True
            self.last_text = proc_text
            self.last_time = time.time()

        # インターフェース
        #if (self.run_vision    == True):
        #    qFunc.txtsWrite(qCtrl_control_vision   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_desktop   == True):
        #    qFunc.txtsWrite(qCtrl_control_desktop  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_bgm       == True):
                qFunc.txtsWrite(qCtrl_control_bgm       ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_browser   == True):
            if (jp_true == True):
                qFunc.txtsWrite(qCtrl_control_browser   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_player    == True):
        #        qFunc.txtsWrite(qCtrl_control_player    ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_chatting  == True):
            if (jp_true == True):
                qFunc.txtsWrite(qCtrl_control_chatting  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_knowledge == True):
            if (jp_true == True):
                qFunc.txtsWrite(qCtrl_control_knowledge ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )

        print('controls:force',force)

        # 外部プログラム '__ext_program.bat'
        if ((proc_text.find(u'プログラム') >= 0) \
        and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0))):
        or ((proc_text.find(u'サープ') >= 0) \
        and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0))) \
            if (os.name == 'nt'):
                ext_program = subprocess.Popen(['__ext_program.bat' ], )
                              #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 画面操作
        if (proc_text.find(u'メイン') >= 0) and (proc_text.find(u'スクリーン') >= 0):
            pyautogui.keyDown('ctrlleft')
            pyautogui.keyDown('winleft')
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.press('left')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp('ctrlleft')

        if (proc_text.find(u'サブ') >= 0) and (proc_text.find(u'スクリーン') >= 0):
            pyautogui.keyDown('ctrlleft')
            pyautogui.keyDown('winleft')
            pyautogui.press('right')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp('ctrlleft')

        if (proc_text.find(u'スクリーン') >= 0) and (proc_text.find(u'キーボード') >= 0):
            pyautogui.keyDown('ctrlleft')
            pyautogui.keyDown('winleft')
            pyautogui.press('o')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp('ctrlleft')

        # キーボード操作
        if (proc_text[-3:] == u'を入力'):
            qFunc.sendKey(proc_text[:-3],cr=True, lf=False)
        elif (proc_text[-2:] == u'入力'):
            qFunc.sendKey(proc_text[:-2],cr=True, lf=False)

        if (proc_text == u'改行') or (proc_text.lower() == 'enter'):
            pyautogui.press('enter')

        if (proc_text.lower() == 'f1') or (proc_text.lower() == 'f 1'):
            pyautogui.press('f1')
        if (proc_text.lower() == 'f2') or (proc_text.lower() == 'f 2'):
            pyautogui.press('f2')
        if (proc_text.lower() == 'f3') or (proc_text.lower() == 'f 3'):
            pyautogui.press('f3')
        if (proc_text.lower() == 'f4') or (proc_text.lower() == 'f 4'):
            pyautogui.press('f4')
        if (proc_text.lower() == 'f5') or (proc_text.lower() == 'f 5'):
            pyautogui.press('f5')
        if (proc_text.lower() == 'f6') or (proc_text.lower() == 'f 6'):
            pyautogui.press('f6')
        if (proc_text.lower() == 'f7') or (proc_text.lower() == 'f 7'):
            pyautogui.press('f7')
        if (proc_text.lower() == 'f8') or (proc_text.lower() == 'f 8'):
            pyautogui.press('f8')
        if (proc_text.lower() == 'f9') or (proc_text.lower() == 'f 9'):
            pyautogui.press('f9')
        if (proc_text.lower() == 'f10') or (proc_text.lower() == 'f 10'):
            pyautogui.press('f10')
        if (proc_text.lower() == 'f11') or (proc_text.lower() == 'f 11'):
            pyautogui.press('f11')
        if (proc_text.lower() == 'f12') or (proc_text.lower() == 'f 12'):
            pyautogui.press('f12')

        if (proc_text == u'ポーズ') \
        or (proc_text == u'閉じる'):
            pyautogui.press('pause')
        if (proc_text[-3:] == u'を検索'):
            qFunc.sendKey(proc_text[:-3],cr=False, lf=False)
            pyautogui.press('f9')

        if (cn_s.qsize() < 99):

            # システム制御
            if (proc_text.find(u'リセット') >= 0):
                out_name  = 'control'
                out_value = '_reset_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_vision , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_desktop, txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            elif ((proc_text.find(u'システム') >= 0) and (proc_text.find(u'終了') >= 0)) \
            or    (proc_text == u'バルス'):
                out_name  = 'control'
                out_value = '_end_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            elif (proc_text.find(u'リブート') >= 0) \
              or (proc_text.find(u'再起動') >= 0):
                out_name  = 'control'
                out_value = '_reboot_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False
                self.run_browser = False
                self.run_player = False
                self.run_chatting = False
                self.run_knowledge = False

            # 機能制御
            elif (proc_text.find(u'画面') >= 0) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True
                qFunc.statusWait_false(qCtrl_control_kernel, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = True

            elif (proc_text.find(u'画面') >= 0) and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = False
                qFunc.statusWait_false(qCtrl_control_kernel, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = False

            elif (proc_text.find(u'ビジョン') >= 0) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = True

            elif (proc_text.find(u'ビジョン') >= 0) and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = False

            elif (proc_text.find(u'デスクトップ') >= 0) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True

            elif (proc_text.find(u'デスクトップ') >= 0) and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = False

            elif ((proc_text.find(u'ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_bgm_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = True

            elif ((proc_text.find(u'ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_bgm_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False

            elif ((proc_text.find(u'ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and ((proc_text.find(u'停止') >= 0) or (proc_text.find(u'ストップ') >= 0)):
                qFunc.txtsWrite(qCtrl_control_bgm ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            elif (proc_text.find(u'動画') >= 0) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_player_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = True
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=[u'動画メニュー'], encoding='utf-8', exclusive=True, mode='w', )

            elif (proc_text.find(u'動画') >= 0) and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_player_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = False

            elif (proc_text.find(u'動画') >= 0) \
            and ((proc_text.find(u'停止') >= 0) or (proc_text.find(u'ストップ') >= 0)):
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            elif (self.run_player == True) \
            and  (proc_text.find(u'動画') >=0) and (proc_text.find(u'メニュー') >=0):
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=[u'動画メニュー'], encoding='utf-8', exclusive=True, mode='w', )

            elif (self.run_player == True) \
            and  (word_true == True) \
            and  (proc_text.lower() >= '01') and (proc_text.lower() <= '09'):
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusWait_false(qCtrl_control_player, 5)
                time.sleep(5.00)
                qFunc.txtsWrite(qCtrl_control_player ,txts=[proc_text.lower()], encoding='utf-8', exclusive=True, mode='w', )

            elif ((proc_text.find(u'ブラウザ') >= 0) or (proc_text.find(u'ウェブ') >= 0)) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_browser_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_browser = True

            elif ((proc_text.find(u'ブラウザ') >= 0) or (proc_text.find(u'ウェブ') >= 0)) \
            and (proc_text.find(u'終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_browser_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_browser = False

            elif ((proc_text.find(u'ブラウザ') >= 0) or (proc_text.find(u'ウェブ') >= 0)) \
            and ((proc_text.find(u'停止') >= 0) or (proc_text.find(u'ストップ') >= 0)):
                qFunc.txtsWrite(qCtrl_control_browser ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            elif ((proc_text.find(u'チャット') >= 0) or (proc_text.find(u'雑談') >= 0)) \
            and ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_chatting_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_chatting = True

            elif ((proc_text.find(u'チャット') >= 0) or (proc_text.find(u'雑談') >= 0)) \
            and   (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_chatting_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_chatting = False

            elif ((proc_text.find(u'チャット') >= 0) or (proc_text.find(u'雑談') >= 0)) \
            and  ((proc_text.find(u'停止') >= 0) or (proc_text.find(u'ストップ') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_chatting_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_chatting = False

            elif ((proc_text.find(u'知識') >= 0) or (proc_text.find(u'ナレッジ') >= 0)) \
            and  ((proc_text.find(u'開始') >= 0) or (proc_text.find(u'起動') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_knowledge_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_knowledge = True

            elif ((proc_text.find(u'知識') >= 0) or (proc_text.find(u'ナレッジ') >= 0)) \
            and   (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_knowledge_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_knowledge = False

            elif ((proc_text.find(u'知識') >= 0) or (proc_text.find(u'ナレッジ') >= 0)) \
            and  ((proc_text.find(u'停止') >= 0) or (proc_text.find(u'終了') >= 0)):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_knowledge_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_knowledge = False

        self.last_text = proc_text
        self.last_time = time.time()



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )



    controls_thread = proc_controls('controls', '0', )
    controls_thread.begin()

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
    controls_thread.abort()
    del controls_thread


