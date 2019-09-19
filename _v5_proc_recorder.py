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

import unicodedata



# インターフェース
qCtrl_control_desktop    = 'temp/control_desktop.txt'



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



def dshow_dev():
    cam = []
    mic = []

    if (os.name == 'nt'):

        ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'dshow', '-list_devices', 'true', '-i', 'dummy', ],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        flag = ''
        while True:
            # バッファから1行読み込む.
            line = ffmpeg.stderr.readline()
            # バッファが空 + プロセス終了.
            if (not line) and (not ffmpeg.poll() is None):
                break
            # テキスト
            txt = line.decode('utf-8')
            if   (txt.find('DirectShow video devices') >=0):
                flag = 'cam'
            elif (txt.find('DirectShow audio devices') >=0):
                flag = 'mic'
            elif (flag == 'cam') and (txt.find(']  "') >=0):
                st = txt.find(']  "') + 4
                en = txt[st:].find('"')
                cam.append(txt[st:st+en])
                #print('cam:', txt[st:st+en])
            elif (flag == 'mic') and (txt.find(']  "') >=0):
                st = txt.find(']  "') + 4
                en = txt[st:].find('"')
                mic.append(txt[st:st+en])
                #print('mic:', txt[st:st+en])

        ffmpeg.terminate()
        ffmpeg = None

    return cam, mic

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False



def movie2mp4(inpPath='', inpName='',outPath1='', outPath2='', ):

    # パラメータ
    inpFile = inpPath + inpName
    if (outPath1 == ''):
        outPath1 = qPath_d_movie
    if (outPath2 == ''):
        outPath2 = qPath_rec
    outFile1 = outPath1 + inpName[:-4] + '.mp4'
    outFile2 = outPath2 + inpName[:-4] + '.mp4'

    #try:
    if (True):

        # 動画処理
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFile, \
            '-vcodec', 'libx264', '-r', '2', outFile1, \
            #], )
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        logb, errb = ffmpeg.communicate()
        ffmpeg.terminate()
        ffmpeg = None

        # コピー
        qFunc.copy(outFile1, outFile2)
        #os.remove(inpFile)

    #except:
    #    pass



def movie2jpg(inpPath='', inpName='',outPath1='', outPath2='', wrkPath=''):

    # パラメータ
    inpFile = inpPath + inpName
    if (outPath1 == ''):
        outPath1 = qPath_d_movie
    if (outPath2 == ''):
        outPath2 = qPath_rec
    if (wrkPath == ''):
        wrkPath = qPath_work + 'movie2jpeg/'

    # ファイルに日時
    dt1 = None
    f = inpName
    yyyy = int(f[:4])
    mm   = int(f[4:6])
    dd   = int(f[6:8])
    h    = int(f[9:11])
    m    = int(f[11:13])
    s    = int(f[13:15])
    dt1=datetime.datetime(yyyy,mm,dd,h,m,s,0)

    hit = False

    #try:
    if (True):

        # 作業ディレクトリ
        qFunc.makeDirs(wrkPath, remove=True, )

        # 動画処理
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFile, \
            '-vf', 'select=gt(scene\,0.1), scale=0:0,showinfo', \
            '-vsync', 'vfr', \
            wrkPath + '%04d.jpg', \
            #], )
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        logb, errb = ffmpeg.communicate()
        ffmpeg.terminate()
        ffmpeg = None

        #log = logb.decode()
        log = errb.decode()
        txts = log.split('\n')
        for txt in txts:
            #print(txt)

            if (txt.find('Parsed_showinfo')>0) and (txt.find('] n:')>0):
                # n, pts_time
                n = ''
                pts_time = ''
                x_n        = txt.find(' n:')
                x_pts      = txt.find(' pts:')
                x_pts_time = txt.find(' pts_time:')
                x_pos      = txt.find(' pos:')
                if (x_n != 0) and (x_pts != 0):
                    n = txt[x_n+3:x_pts].strip()
                if (x_pts_time != 0) and (x_pos != 0):
                    pts_time = txt[x_pts_time+10:x_pos].strip()

                if (n == '') or (pts_time == ''):
                    #print(txt)
                    pass
                else:
                    #print(n,pts_time)

                    # s => hhmmss
                    dt2=datetime.timedelta(seconds=float(pts_time))
                    dtx=dt1+dt2
                    stamp = dtx.strftime('%Y%m%d.%H%M%S.%f')
                    #print(stamp[:-7])

                    # コピー
                    seq4 = '{:04}'.format(int(n) + 1)
                    f0 =  wrkPath + seq4 + '.jpg'
                    if (os.path.exists(f0)):
                        f1 =  wrkPath + stamp[:-3] + '.jpg'
                        f2 =  outPath1 + stamp[:-3] + '.jpg'
                        f3 =  outPath2 + stamp[:-3] + '.jpg'
                        os.rename(f0, f1)
                        qFunc.copy(f1, f2)
                        qFunc.copy(f1, f3)
                        os.remove(f1)

                        hit = True

    #except:
    #    pass

    #try:
    #if (hit == True):
    if (True):

        # 作業ディレクトリ
        qFunc.makeDirs(wrkPath, remove=True, )

        # 動画処理
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFile, \
            '-ss', '0', '-t', '2', '-r', '1', \
            '-qmin', '1', '-q', '1', \
            wrkPath + '%04d.jpg', \
            #], )
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        logb, errb = ffmpeg.communicate()
        ffmpeg.terminate()
        ffmpeg = None

        stamp = dt1.strftime('%Y%m%d.%H%M%S.000000')

        # コピー
        seq4 = '0001'
        f0 =  wrkPath + seq4 + '.jpg'
        if (os.path.exists(f0)):
            f1 =  wrkPath + stamp[:-3] + '.jpg'
            f2 =  outPath1 + stamp[:-3] + '.jpg'
            f3 =  outPath2 + stamp[:-3] + '.jpg'
            os.rename(f0, f1)
            qFunc.copy(f1, f2)
            qFunc.copy(f1, f3)
            os.remove(f1)

    #except:
    #    pass



class proc_recorder:

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

        # 変数設定
        self.rec_max   = 10
        self.rec_id    = {}
        self.rec_start = {}
        self.rec_limit = {}
        self.rec_file  = {}
        for i in range(1, self.rec_max+1):
            self.rec_id[i]    = None
            self.rec_start[i] = time.time()
            self.rec_limit[i] = None
            self.rec_file[i]  = ''

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

    def stop(self, waitMax=20, ):
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

        # 録画開始
        if (self.runMode == 'recorder'):
            self.sub_proc(u'録画開始', )

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

            # 制限時間、自動停止
            for i in range(1, self.rec_max+1):
                if (not self.rec_limit[i] is None):
                    if (time.time() > self.rec_limit[i]):
                        self.rec_limit[i] = None
                        
                        # 録画ストップ
                        if (not self.rec_id[i] is None):
                            self.sub_stop(i, '_rec_stop_', )

            # 一定時間（5分毎）、自動リスタート
            for i in range(1, self.rec_max+1):
                if (not self.rec_id[i] is None):
                    if ((time.time() - self.rec_start[i]) > (60 * 1)):

                        # 録画リスタート
                        self.sub_start(0, '_rec_restart_', )

                        # 録画ストップ
                        self.sub_stop(i, '_rec_stop_', )

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 処理
            elif (inp_name.lower() != ''):
                self.sub_proc(inp_value, )

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == '_busy_'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(self.fileRdy)

            # 録画終了
            self.sub_proc(u'録画終了')

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

            # 全録画ストップ
            for i in range(1, self.rec_max+1):
                if (not self.rec_id[i] is None):
                    self.sub_stop(i, '_rec_stop_', )

        elif (proc_text.lower() == '_rec_stop_') \
          or (proc_text.find(u'録画') >=0) and (proc_text.find(u'停止') >=0) \
          or (proc_text.find(u'録画') >=0) and (proc_text.find(u'終了') >=0):

            # 全録画ストップ
            for i in range(1, self.rec_max+1):
                if (not self.rec_id[i] is None):
                    self.sub_stop(i, '_rec_stop_', )

        elif (proc_text.lower() == '_rec_start_') \
          or (proc_text.find(u'録画') >=0):

            # 録画スタート
            self.sub_start(0, proc_text, )



    # 録画開始
    def sub_start(self, index, proc_text, ):

        # index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (self.rec_id[i] is None):
                    index = i
                else:
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i

        # 開始処理
        if (index != 0):

            # ビジー設定
            if (not os.path.exists(self.fileBsy)):
                qFunc.txtsWrite(self.fileBsy, txts=['_busy_'], encoding='utf-8', exclusive=False, mode='a', )
                if (str(self.id) == '0'):
                    qFunc.busySet(qBusy_d_rec, True)

            # メッセージ
            if (proc_text.lower() == '_rec_start_') \
            or (proc_text.find(u'録画') >=0):
                speechs = []
                speechs.append({ 'text':u'録画を開始します。', 'wait':0, })
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            elif (proc_text.lower() == '_rec_restart_'):
                speechs = []
                speechs.append({ 'text':u'録画が継続中です。', 'wait':0, })
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (proc_text.lower() == '_rec_start_') \
            or (proc_text.lower() == '_rec_restart_') \
            or (proc_text.find(u'録画') >=0):

                # デバイス名取得
                cam, mic = dshow_dev()

                # 開始
                nowTime    = datetime.datetime.now()
                stamp      = nowTime.strftime('%Y%m%d.%H%M%S')
                if (proc_text.lower() == '_rec_start_') \
                or (proc_text.lower() == '_rec_restart_') \
                or (proc_text.find(u'開始') >=0):
                    self.rec_limit[index] = None
                    self.rec_file[index]  = qPath_work + stamp + '.flv'
                else:
                    rec_txt = '.' + qFunc.txt2filetxt(proc_text)
                    self.rec_limit[index] = time.time() + 30
                    self.rec_file[index]  = qPath_work + stamp + rec_txt + '.flv'

                if (os.name != 'nt'):
                    # ffmpeg -f avfoundation -list_devices true -i ""
                    self.rec_id[index] = subprocess.Popen(['ffmpeg', \
                                '-f', 'avfoundation', \
                                '-i', '1:2', \
                                '-q:v', '0', \
                                '-r', '5', self.rec_file[index], \
                                '-loglevel', 'warning', \
                                ], stdin=subprocess.PIPE, )
                                #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    self.rec_start[index] = time.time()
                else:
                    # ffmpeg -f gdigrab -i desktop -r 5 temp_flv.flv
                    # ffmpeg -f gdigrab -i desktop -f dshow -i audio="mic" -vcodec libx264 temp_mp4.mp4
                    if (len(mic) > 0) and (not is_japanese(mic[0])):
                        microphone = 'audio="' + mic[0] + '"'
                        self.rec_id[index] = subprocess.Popen(['ffmpeg', \
                                '-f', 'gdigrab', '-i', 'desktop', \
                                '-f', 'dshow', '-i', microphone, \
                                '-q:v', '0', \
                                '-r', '5', self.rec_file[index], \
                                '-loglevel', 'warning', \
                                ], stdin=subprocess.PIPE, )
                                #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        #cmd = 'ffmpeg -f gdigrab -i desktop -f dshow -i ' + microphone + ' -loglevel warning -r 5 ' + self.rec_file[index]
                        #print(cmd)
                        #self.rec_id[index] = subprocess.Popen(['powershell', ], \
                        #            stdin=subprocess.PIPE, )
                        #            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        #self.rec_id[index].stdin.write(b'chcp 65001\n')
                        #self.rec_id[index].stdin.write(cmd.encode())
                        #self.rec_id[index].stdin.write(b'\n')

                    else:
                        self.rec_id[index] = subprocess.Popen(['ffmpeg', \
                                '-f', 'gdigrab', '-i', 'desktop', \
                                '-q:v', '0', \
                                '-r', '5', self.rec_file[index], \
                                '-loglevel', 'warning', \
                                ], stdin=subprocess.PIPE, )
                                #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    self.rec_start[index] = time.time()

                # ログ
                qFunc.logOutput(self.proc_id + ':' + u'desktop recorder → ' + self.rec_file[index] + ' start', display=True,)

    # 録画停止
    def sub_stop(self, index, proc_text, ):

        # index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (not self.rec_id[i] is None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # 停止処理
        if (index != 0):
            if (not self.rec_id[index] is None):

                # 録画停止
                if (os.name != 'nt'):
                    self.rec_id[index].stdin.write(b'q\n')
                    try:
                        self.rec_id[index].stdin.flush()
                    except:
                        pass
                    time.sleep(2.00)
                    #self.rec_id[index].send_signal(signal.SIGINT)
                else:
                    self.rec_id[index].stdin.write(b'q\n')
                    try:
                        self.rec_id[index].stdin.flush()
                    except:
                        pass
                    time.sleep(2.00)
                    #self.rec_id[index].send_signal(signal.CTRL_C_EVENT)

                time.sleep(2.00)
                self.rec_id[index].wait()
                self.rec_id[index].terminate()
                self.rec_id[index] = None

                # ログ
                qFunc.logOutput(self.proc_id + ':' + u'desktop recorder → ' + self.rec_file[index] + ' stop', display=True,)

                # サムネイル抽出
                inpName = self.rec_file[index].replace(qPath_work ,'')
                movie2jpg(inpPath = qPath_work, inpName=inpName, outPath1 = qPath_d_movie, outPath2 = qPath_rec, wrkPath=qPath_work + 'movie2jpeg/', )
                movie2mp4(inpPath = qPath_work, inpName=inpName, outPath1 = qPath_d_movie, outPath2 = qPath_rec, )

        # index
        index = 0
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (not self.rec_id[i] is None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # リセット
        if (index == 0):
            qFunc.kill('ffmpeg', )

            # メッセージ
            speechs = []
            speechs.append({ 'text':u'録画を終了しました。', 'wait':0, })
            qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            # ビジー解除
            qFunc.remove(self.fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_d_rec, False)



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    # 開始
    recorder_thread = proc_recorder('recorder', '0', )
    recorder_thread.start()



    # 単体実行
    if (len(sys.argv) < 2):

        recorder_thread.put(['control', u'録画開始'])
        time.sleep(45)

        recorder_thread.put(['control', u'デスクトップの録画'])
        time.sleep(45)

        recorder_thread.put(['control', u'録画終了'])
        time.sleep(10)



    # バッチ実行
    if (len(sys.argv) >= 2):

        # 初期設定
        qFunc.remove(qCtrl_control_desktop)

        # 録画開始
        recorder_thread.put(['control', '_rec_start_'])

        # 待機ループ
        while (True):

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_desktop)
            if (txts != False):
                qFunc.logOutput(str(txt))
                if (txt == '_end_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_desktop)
                    control = txt
            
            time.sleep(0.50)



    # 終了
    recorder_thread.stop()
    del recorder_thread


