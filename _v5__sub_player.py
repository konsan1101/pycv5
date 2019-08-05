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

import multiprocessing

import pyautogui
if (os.name == 'nt'):
    import ctypes

import random

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_self       = qCtrl_control_player



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



runMode = 'debug'



def qFFplay(id='qFFplay', file='', vol=100, order='normal', left=100, top=100, width=320, height=240,):

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs

    if (width != 0) or (height != 0):
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', str(id), \
                                    '-noborder', '-autoexit', \
                                    '-x', str(width), '-y', str(height), \
                                    '-loglevel', 'warning', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        w, h = pyautogui.size()
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', str(id), \
                                    '-noborder', '-autoexit', \
                                    #'-fs', \
                                    '-x', str(w), '-y', str(h), \
                                    '-loglevel', 'warning', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    z_order = 0
    if (order == 'top'):
        z_order = -1

    if (os.name == 'nt'):
        hwnd = 0
        chktime = time.time()
        while (hwnd == 0) and ((time.time() - chktime) < 3):
            hwnd = ctypes.windll.user32.FindWindowW(None, str(id))
            time.sleep(0.10)

    if (width != 0) or (height != 0):
        if (os.name == 'nt'):
            if (hwnd != 0):
                ctypes.windll.user32.SetWindowPos(hwnd,z_order,int(left),int(top),0,0,1)
    else:
        if (os.name == 'nt'):
            if (hwnd != 0):
                ctypes.windll.user32.SetWindowPos(hwnd,z_order,0,0,0,0,1)

    ffplay.wait()
    ffplay.terminate()
    ffplay = None

    return True



def panelPlay(panel, path, vol, order, loop,):
    #left, top, width, height = getPanelPos(panel,)

    count = 0
    while (loop > 0):

        if (os.path.isfile(path)):
            p = panel

            left, top, width, height = getPanelPos(p,)
            res = qFFplay(p, path, vol, order, left, top, width, height, )
            count += 1

        if (os.path.isdir(path)):
            files = glob.glob(path + '/*.*')
            random.shuffle(files)
            for fn in files:
                p = panel
                if (panel == '1397'):
                    p = panel[(count % 4):(count % 4)+1] + '-'
                if (panel == '19'):
                    p = panel[(count % 2):(count % 2)+1] + '-'
                if (panel == '28'):
                    p = '82'[(count % 2):(count % 2)+1] + '-'
                if (panel == '37'):
                    p = panel[(count % 2):(count % 2)+1] + '-'
                if (panel == '46'):
                    p = '64'[(count % 2):(count % 2)+1] + '-'

                left, top, width, height = getPanelPos(p,)
                res = qFFplay(p, fn, vol, order, left, top, width, height, )
                count += 1

        if (loop < 9):
            loop -= 1



def getPanelPos(id='0-', ):
    w, h = pyautogui.size()
    wa = int(w/100) 
    ha = int(h/100) 
    wb = int(w/20) 
    hb = int(h/20) 
    if   (id == '0'):
        return 0, 0, w, h
    elif (id == '0-'):
        return wb, hb, int(w-wb*2), int(h-hb*2)
    elif (id == '1'):
        return 0, 0, int(w/3), int(h/3)
    elif (id == '1-'):
        return 0+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '2'):
        return int(w/3), 0, int(w/3), int(h/3)
    elif (id == '2-'):
        return int(w/3)+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '3'):
        return w-int(w/3), 0, int(w/3), int(h/3)
    elif (id == '3-'):
        return w-int(w/3)+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '4'):
        return 0, int(h/3), int(w/3), int(h/3)
    elif (id == '4-'):
        return 0+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '5'):
        return int(w/3), int(h/3), int(w/3), int(h/3)
    elif (id == '5-'):
        return int(w/3)+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '6'):
        return w-int(w/3), int(h/3), int(w/3), int(h/3)
    elif (id == '6-'):
        return w-int(w/3)+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '7'):
        return 0, h-int(h/3), int(w/3), int(h/3)
    elif (id == '7-'):
        return 0+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '8'):
        return int(w/3), h-int(h/3), int(w/3), int(h/3)
    elif (id == '8-'):
        return int(w/3)+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    elif (id == '9'):
        return w-int(w/3), h-int(h/3), int(w/3), int(h/3)
    elif (id == '9-'):
        return w-int(w/3)+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
    else:
        return int(w/4), int(h/4), int(w/2), int(h/2)



class main_class:

    def __init__(self, name='thread', id='0', runMode='debug', ):
        self.runMode   = runMode

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

        self.play_max  = 10
        self.play_proc = {}
        self.play_id   = {}
        self.play_path = {}
        for i in range(1, self.play_max+1):
            self.play_proc[i] = None
            self.play_id[i]   = None
            self.play_path[i] = None

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

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_close_'):
                qFunc.remove(qCtrl_control_self)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                qFunc.logOutput(self.proc_id + ':' + str(txt))
                if (txt == '_close_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_self)
                    control = txt

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qFunc.logOutput(self.proc_id + ':alive', display=True, )
                last_alive = time.time()

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

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])

            # 活動Ｑ検査
            if (os.path.exists(self.fileBsy)):
                self.sub_alive()

            # 処理
            if (control != ''):
                self.sub_proc(control, )

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.50)
            else:
                time.sleep(0.25)

        # 終了処理
        if (True):

            # レディー解除
            qFunc.remove(self.fileRdy)

            # 停止
            self.sub_proc('_stop_', )

            # ビジー解除
            qFunc.remove(self.fileBsy)

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



    # 処理
    def sub_proc(self, proc_text, ):

        if (proc_text.find(u'リセット') >=0):

            # 停止
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_stop_'):

            # 停止
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_start_'):

            pass

        elif (proc_text.lower() == 'demo0-'):
            path0 = u'C:/Users/Public/_m4v__Clip/Perfume'
            self.sub_start(path1, panel='0' , vol=0  , order='normal', loop=1, )
            self.sub_start(path1, panel='0-', vol=100, order='top'   , loop=1, )

        elif (proc_text.lower() == 'demo1397'):
            path0 = u'C:/Users/Public/_動画_AppleTV'
            path1 = u'C:/Users/Public/_m4v__Clip/Perfume'
            self.sub_start(path0, panel='0'   , vol=0  , order='normal', loop=99, )
            self.sub_start(path1, panel='1397', vol=100, order='top'   , loop=99, )

        elif (proc_text.lower() == 'demo1234'):
            path0 = u'C:/Users/Public/_m4v__Clip/etc'
            path1 = u'C:/Users/Public/_m4v__Clip/Perfume'
            path2 = u'C:/Users/Public/_m4v__Clip/BABYMETAL'
            path3 = u'C:/Users/Public/_m4v__Clip/OneOkRock'
            path4 = u'C:/Users/Public/_m4v__Clip/きゃりーぱみゅぱみゅ'
            self.sub_start(path0, panel='0' , vol=100, order='normal', loop=99, )
            self.sub_start(path1, panel='19', vol=0  , order='normal', loop=99, )
            self.sub_start(path2, panel='28', vol=0  , order='normal', loop=99, )
            self.sub_start(path3, panel='37', vol=0  , order='normal', loop=99, )
            self.sub_start(path4, panel='46', vol=0  , order='normal', loop=99, )

        elif (proc_text.lower() == 'test'):
            path0 = u'C:/Users/Public/_動画_AppleTV'
            path1 = u'C:/Users/Public/_m4v__Clip/Perfume'
            path2 = u'C:/Users/Public/_m4v__Clip/BABYMETAL'
            path3 = u'C:/Users/Public/_m4v__Clip/OneOkRock'
            path4 = u'C:/Users/Public/_m4v__Clip/きゃりーぱみゅぱみゅ'
            path5 = u'C:/Users/Public/_m4v__Clip/etc'
            path6 = u'C:/Users/Public/_m4v__Clip/SekaiNoOwari'
            path7 = u'C:/Users/Public/_m4v__Clip/GB'
            path8 = path1
            path9 = path2
            self.sub_start(path0, panel='0' , vol=0  , order='normal', loop=99, )
            self.sub_start(path1, panel='1-', vol=0  , order='normal', loop=99, )
            self.sub_start(path2, panel='2-', vol=0  , order='normal', loop=99, )
            self.sub_start(path3, panel='3-', vol=0  , order='normal', loop=99, )
            self.sub_start(path4, panel='4-', vol=0  , order='normal', loop=99, )
            self.sub_start(path5, panel='5-', vol=100, order='top'   , loop=99, )
            self.sub_start(path6, panel='6-', vol=0  , order='normal', loop=99, )
            self.sub_start(path7, panel='7-', vol=0  , order='normal', loop=99, )
            self.sub_start(path8, panel='8-', vol=0  , order='normal', loop=99, )
            self.sub_start(path9, panel='9-', vol=0  , order='normal', loop=99, )

        else:

            # 開始
            self.sub_start(proc_text, panel='0-', vol=100, order='normal', loop=1, )



    # 活動Ｑ検査
    def sub_alive(self, ):
        hit = -1
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (not self.play_proc[i] is None):
                hit = i
                break
        if (hit == -1):
            # ビジー解除
            qFunc.remove(self.fileBsy)
            return False
        else:
            # ビジー設定
            if (not os.path.exists(self.fileBsy)):
                qFunc.txtsWrite(self.fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )
            return True

    # 開始
    def sub_start(self, proc_text, panel='0-', vol=100, order='normal', loop=1, ):

        # ログ
        qFunc.logOutput(self.proc_id + ':open ' + proc_text, display=True,)

        # 空きＱ検索
        hit = -1
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (self.play_proc[i] is None):
                hit = i
                break

        # オープン
        if (hit >= 0):

            # ビジー設定
            if (not os.path.exists(self.fileBsy)):
                qFunc.txtsWrite(self.fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )

            i = hit
            self.play_id[i]   = panel
            self.play_path[i] = proc_text
            self.play_proc[i] = multiprocessing.Process(target=panelPlay, \
                args=(self.play_id[i], self.play_path[i], vol, order, loop, ), )
            self.play_proc[i].daemon = True
            self.play_proc[i].start()

            if (os.name == 'nt'):
                time.sleep(1.00)

    # 停止
    def sub_stop(self, proc_text, ):

        # リセット
        qFunc.kill('ffplay', )

        # 全Ｑリセット
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    self.play_proc[i].terminate()
                    del self.play_proc[i]
                    self.play_proc[i] = None
                    self.play_id[i]   = ''
                    self.play_path[i] = ''
                #except:
                #    self.play_proc[i] = None
                #    self.play_id[i]   = ''
                #    self.play_path[i] = ''

        # ビジー解除
        self.sub_alive()



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'player'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qFunc.init()

    # ログ設定

    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput(main_id + ':init')
    qFunc.logOutput(main_id + ':exsample.py runMode, ')

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        qFunc.logOutput(main_id + ':runMode  =' + str(runMode  ))

    # 初期設定

    txts, txt = qFunc.txtsRead(qCtrl_control_self)
    if (txts != False):
        if (txt == '_close_'):
            qFunc.remove(qCtrl_control_self)

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

        main_class = main_class(main_name, '0', runMode=runMode, )
        main_class.start()

        main_start = time.time()
        onece      = True

    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_close_'):
                break

        # デバッグ
        if (onece == True):
            onece = False
            if (runMode == 'debug'):
                #t = u'C:/Users/Public/_m4v__Clip/Perfume/Perfume_FLASH.m4v'
                #t = u'C:/Users/Public/_m4v__Clip/Perfume'
                #t = u'demo0-'   # base + center
                #t = u'demo1397' # base + 1,3,9,7
                #t = u'demo1234' # base + 1234,6789
                t = u'test'      # base + 1-9
                qFunc.txtsWrite(qCtrl_control_self ,txts=[t], encoding='utf-8', exclusive=True, mode='w', )

        # デバッグ
        if (runMode == 'debug'):

            # テスト終了
            if  ((time.time() - main_start) > 120):
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                    time.sleep(5.00)
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )

        # アイドリング
        if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy'):
            time.sleep(1.00)
        time.sleep(0.50)



    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        main_class.stop()
        del main_class

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)


