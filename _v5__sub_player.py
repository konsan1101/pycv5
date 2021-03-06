#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import datetime
import codecs
import glob

import queue
import threading
import subprocess

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



# qLog,qFunc 共通ルーチン
import  _v5__qLog
qLog  = _v5__qLog.qLog_class()
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



# フォント
qFONT_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}



runMode = 'debug'



def qFFplay(id='qFFplay', file='', vol=100, order='normal', left=100, top=100, width=320, height=240, fps=5, overText=''):

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit[out0],showspectrum[out1]"
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit[out0],showwaves[out1]"
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit=3[out1][a][b]; [a]showwaves=s=320x100[waves]; [b]showspectrum=s=320x100[spectrum]; [waves][spectrum] vstack[out0]"

    vf = 'fps=' + str(fps)
    if (overText != ''):
        vf += ',drawtext=fontfile=' + qFONT_default['file'] + ':fontsize=256:fontcolor=white:text=' + overText

    if (file[-4:].lower() == '.wav') \
    or (file[-4:].lower() == '.mp3') \
    or (file[-4:].lower() == '.m4a'):
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(width), '-y', str(height), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        if (width != 0) or (height != 0):
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-vf', vf, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(width), '-y', str(height), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        else:
            w, h = pyautogui.size()
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-vf', vf, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        #'-fs', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(w), '-y', str(h), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    time.sleep(1.00)

    z_order = 0
    if (order == 'top'):
        z_order = -1

    if (os.name == 'nt'):
        hwnd = 0
        chktime = time.time()
        while (hwnd == 0) and ((time.time() - chktime) < 8):
            hwnd = ctypes.windll.user32.FindWindowW(None, str(id))
            time.sleep(0.10)

        if (hwnd != 0):
            if (width != 0) or (height != 0):
                ctypes.windll.user32.SetWindowPos(hwnd,z_order,int(left),int(top),0,0,1)

    ffplay.wait()
    ffplay.terminate()
    ffplay = None

    return True



def panelPlay(panel, path, vol, order, loop, overtext):

    count = 0
    while (loop > 0):

        if (os.path.isfile(path)):
            fn = path
            p  = panel

            fps = 15
            if (vol == 0):
                if (p=='0') or (p=='0-') or (p=='5'):
                    fps = 5
                else:
                    fps = 2

            if (fn[-4:].lower() == '.wav') \
            or (fn[-4:].lower() == '.mp3') \
            or (fn[-4:].lower() == '.m4a'):
                if (p=='0') or (p=='0-'):
                    p = '5+'

            left, top, width, height = qFunc.getPanelPos(p,)
            res = qFFplay(p, fn, vol, order, left, top, width, height, fps, overtext)
            count += 1

            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_') or (txt == '_stop_'):
                    loop = 0

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

                fps = 15
                if (vol == 0):
                    if (p=='0') or (p=='0-') or (p=='5'):
                        fps = 5
                    else:
                        fps = 2

                if (fn[-4:].lower() == '.wav') \
                or (fn[-4:].lower() == '.mp3') \
                or (fn[-4:].lower() == '.m4a'):
                    if (p=='0') or (p=='0-'):
                        p = '5+'

                left, top, width, height = qFunc.getPanelPos(p,)
                res = qFFplay(p, fn, vol, order, left, top, width, height, fps, overtext)
                count += 1

                txts, txt = qFunc.txtsRead(qCtrl_control_self)
                if (txts != False):
                    if (txt == '_end_') or (txt == '_stop_'):
                        loop = 0
                        break

        if (loop < 9):
            loop -= 1



class main_player:

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
        qLog.log('info', self.proc_id, 'init', display=self.logDisp, )

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
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        #qLog.log('info', self.proc_id, 'start')

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
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )

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
        qLog.log('info', self.proc_id, 'start', display=self.logDisp, )
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        last_menu  = 0

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                qLog.log('info', self.proc_id, '' + str(txt))
                if (txt == '_end_'):
                    break

                if (txt == '_stop_'):
                    self.sub_proc('_stop_', )
                    time.sleep(2.00)

                qFunc.remove(qCtrl_control_self)
                control = txt

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', display=True, )
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
                qLog.log('warning', self.proc_id, 'queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 活動Ｑ検査
            if (os.path.exists(self.fileBsy)):
                self.sub_alive()

            # 選択アナウンス
            if (control.find(u'動画') >=0) and (control.find(u'メニュー') >=0):
                last_menu = time.time()
            if (control.lower() >= '01') and (control.lower() <= '09'):
                last_menu = 0

            if (last_menu != 0):
                if ((time.time() - last_menu) > 120):
                    if (onece == True):
                        onece = False

                        speechs = []
                        speechs.append({ 'text':u'画面表示位置を指定して再生はいかがですか？', 'wait':0, })
                        qFunc.speech(id='speech', speechs=speechs, lang='', )

            # 処理
            if (control != ''):
                self.sub_proc(control, )

            # アイドリング
            slow = False
            if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif (qFunc.statusCheck(qBusy_dev_mic) == True):
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

            # レディー解除
            qFunc.statusSet(self.fileRdy, False)

            # 停止
            self.sub_proc('_stop_', )

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_play, False)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



    # 処理
    def sub_proc(self, proc_text, ):
        path = {}
        if (qPLATFORM == 'windows'):
            path['00'] = u'C:/Users/Public/_動画_AppleTV'
            path['01'] = u'C:/Users/Public/_m4v__Clip/Perfume'
            path['02'] = u'C:/Users/Public/_m4v__Clip/BABYMETAL'
            path['03'] = u'C:/Users/Public/_m4v__Clip/OneOkRock'
            path['04'] = u'C:/Users/Public/_m4v__Clip/きゃりーぱみゅぱみゅ'
            path['05'] = u'C:/Users/Public/_m4v__Clip/etc'
            path['06'] = u'C:/Users/Public/_m4v__Clip/SekaiNoOwari'
            path['07'] = u'C:/Users/Public/_m4v__Clip/GB'
            path['08'] = path['02']
            path['09'] = path['01']
        elif (qPLATFORM == 'darwin'):
            path['00'] = u'/Users/kondou/Documents/_動画_AppleTV'
            path['01'] = u'/Users/kondou/Documents/_m4v__Clip/Perfume'
            path['02'] = u'/Users/kondou/Documents/_m4v__Clip/BABYMETAL'
            path['03'] = u'/Users/kondou/Documents/_m4v__Clip/OneOkRock'
            path['04'] = u'/Users/kondou/Documents/_m4v__Clip/きゃりーぱみゅぱみゅ'
            path['05'] = u'/Users/kondou/Documents/_m4v__Clip/GB'
            path['06'] = u'/Users/kondou/Documents/_m4v__Clip/SekaiNoOwari'
            path['07'] = u'/Users/kondou/Documents/_m4v__Clip/etc'
            path['08'] = path['02']
            path['09'] = path['01']

        if (proc_text.find(u'リセット') >=0):
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_stop_'):
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_start_'):
            pass

        elif (proc_text.lower() == '_demo0-'):
            #self.sub_stop('_stop_', )
            self.sub_start(path['01'], panel='0' , vol=0  , order='normal', loop=1, )
            self.sub_start(path['01'], panel='0-', vol=100, order='top'   , loop=1, )

        elif (proc_text.lower() == '_demo1397'):
            #self.sub_stop('_stop_', )
            self.sub_start(path['00'], panel='0'   , vol=0  , order='normal', loop=99, )
            self.sub_start(path['01'], panel='1397', vol=100, order='top'   , loop=99, )

        elif (proc_text.lower() == '_demo1234'):
            #self.sub_stop('_stop_', )
            self.sub_start(path['05'], panel='0' , vol=100, order='normal', loop=99, )
            self.sub_start(path['01'], panel='19', vol=0  , order='normal', loop=99, )
            self.sub_start(path['02'], panel='28', vol=0  , order='normal', loop=99, )
            self.sub_start(path['03'], panel='37', vol=0  , order='normal', loop=99, )
            self.sub_start(path['04'], panel='46', vol=0  , order='normal', loop=99, )

        elif ((proc_text.find(u'動画') >=0) and (proc_text.find(u'メニュー') >=0)) or (proc_text.lower() == '_test_'):
            #self.sub_stop('_stop_', )
            self.sub_start(path['00'], panel='0' , vol=0  , order='normal', loop=99, overtext='', )
            self.sub_start(path['01'], panel='1-', vol=0  , order='normal', loop=99, overtext='01', )
            self.sub_start(path['02'], panel='2-', vol=0  , order='normal', loop=99, overtext='02', )
            self.sub_start(path['03'], panel='3-', vol=0  , order='normal', loop=99, overtext='03', )
            self.sub_start(path['04'], panel='4-', vol=0  , order='normal', loop=99, overtext='04', )
            if (proc_text.find(u'動画') >=0) and (proc_text.find(u'メニュー') >=0):
                self.sub_start(path['05'], panel='5-', vol=0  , order='normal', loop=99, overtext='05', )
            if (proc_text.lower() == '_test_'):
                self.sub_start(path['05'], panel='5-', vol=100, order='top'   , loop=99, overtext='05', )
            self.sub_start(path['06'], panel='6-', vol=0  , order='normal', loop=99, overtext='06', )
            self.sub_start(path['07'], panel='7-', vol=0  , order='normal', loop=99, overtext='07', )
            self.sub_start(path['08'], panel='8-', vol=0  , order='normal', loop=99, overtext='08', )
            self.sub_start(path['09'], panel='9-', vol=0  , order='normal', loop=99, overtext='09', )

        elif (proc_text.lower() >= '01') and (proc_text.lower() <= '09'):
            #self.sub_stop('_stop_', )
            self.sub_start(path[proc_text], panel='0-', vol=100, order='top' , loop=99, )

        else:
            proc_path = qFunc.txtFilePath(proc_text)
            if (proc_path != False):
                #self.sub_stop('_stop_', )
                self.sub_start(proc_path, panel='0-', vol=100, order='top', loop=1, )



    # 活動Ｑ検査
    def sub_alive(self, ):
        hit = -1
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        #self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except Exception as e:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (not self.play_proc[i] is None):
                hit = i
                break
        if (hit == -1):
            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_play, False)
            return False
        else:
            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_play, True)
            return True

    # 開始
    def sub_start(self, proc_text, panel='0-', vol=100, order='normal', loop=1, overtext='', ):

        # ログ
        qLog.log('info', self.proc_id, 'open ' + proc_text, display=True,)

        # 空きＱ検索
        hit = -1
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        #self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except Exception as e:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (self.play_proc[i] is None):
                hit = i
                break

        # オープン
        if (hit >= 0):

            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_play, True)

            i = hit
            self.play_id[i]   = panel
            self.play_path[i] = proc_text
            self.play_proc[i] = threading.Thread(target=panelPlay, args=(
                self.play_id[i], self.play_path[i], vol, order, loop, overtext,
                ))
            #self.play_proc[i].setDaemon(True)
            self.play_proc[i].start()

            time.sleep(2.00)

    # 停止
    def sub_stop(self, proc_text, ):

        # リセット
        qFunc.kill('ffplay', )

        # 全Ｑリセット
        for i in range(1, self.play_max+1):
            if (not self.play_proc[i] is None):
                #try:
                    #self.play_proc[i].terminate()
                    del self.play_proc[i]
                    self.play_proc[i] = None
                    self.play_id[i]   = ''
                    self.play_path[i] = ''
                #except Exception as e:
                #    self.play_proc[i] = None
                #    self.play_id[i]   = ''
                #    self.play_path[i] = ''

        # リセット
        qFunc.kill('ffplay', )

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

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, ')

    # 初期設定

    if (True):

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        qFunc.kill('ffplay')

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        qLog.log('info', main_id, 'runMode  =' + str(runMode  ))

    # 起動

    if (True):

        qLog.log('info', main_id, 'start')

        main_core = main_player(main_name, '0', runMode=runMode, )
        main_core.begin()

        main_start = time.time()
        onece      = True

    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                break

        # デバッグ
        if (onece == True):
            onece = False
            if (runMode == 'debug'):
                #t = u'C:/Users/Public/_m4v__Clip/Perfume/Perfume_FLASH.m4v'
                #t = u'C:/Users/Public/_m4v__Clip/Perfume'
                #t = u'_demo0-'   # base + center
                #t = u'_demo1397' # base + 1,3,9,7
                #t = u'_demo1234' # base + 1234,6789
                t = u'_test_'      # base + 1-9
                qLog.log('debug', main_id, t, )
                qFunc.txtsWrite(qCtrl_control_self ,txts=[t], encoding='utf-8', exclusive=True, mode='w', )

        # デバッグ
        if (runMode == 'debug'):

            # テスト終了
            if  ((time.time() - main_start) > 30):
                    qLog.log('debug', main_id, '_stop_', )
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                    time.sleep(5.00)
                    qLog.log('debug', main_id, '_end_', )
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        # アイドリング
        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif (qFunc.statusCheck(qBusy_dev_mic) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.50)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        main_core.abort()
        del main_core

        qFunc.kill('ffplay', )

        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


