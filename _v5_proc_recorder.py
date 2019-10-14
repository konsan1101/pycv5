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



# インターフェース
qCtrl_control_desktop    = 'temp/control_desktop.txt'



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



def check_sox():
    result = True

    try:
        sox = subprocess.Popen(['sox', '-q', '-d', '-r', '16000', '-b', '16', '-c', '1', \
                qPath_work + 'check_sox.wav', 'trim', '0', '0.5', \
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        sox.wait()
        sox.terminate()
        sox = None
    except:
        return False
    
    return result

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



def movie2jpg(inpPath='', inpNamev='',outPath='', wrkPath='', sfps=1, scene=0.1, ):

    # パラメータ
    inpFilev = inpPath + inpNamev
    if (outPath == ''):
        outPath = qPath_rec
    if (wrkPath == ''):
        wrkPath = qPath_work + 'movie2jpeg/'
    inpTime = inpNamev[:15]
    inpText = inpNamev[15:-4]

    # ファイルに日時
    dt1 = None
    f = inpNamev
    yyyy = int(f[:4])
    mm   = int(f[4:6])
    dd   = int(f[6:8])
    h    = int(f[9:11])
    m    = int(f[11:13])
    s    = int(f[13:15])
    dt1=datetime.datetime(yyyy,mm,dd,h,m,s,0)

    result = False

    #try:
    if (True):

        # 作業ディレクトリ
        qFunc.makeDirs(wrkPath, remove=True, )

        # 動画処理
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFilev, \
            '-ss', '0', '-t', '2', '-r', '1', \
            '-qmin', '1', '-q', '1', \
            wrkPath + '%04d.jpg', \
            '-loglevel', 'warning', \
            ], )
            #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        #logb, errb = ffmpeg.communicate()
        ffmpeg.wait()
        ffmpeg.terminate()
        ffmpeg = None

        stamp = dt1.strftime('%Y%m%d.%H%M%S.000000')

        # コピー
        seq4 = '0001'
        f0 =  wrkPath + seq4 + '.jpg'
        if (os.path.exists(f0)):
            if (inpText == ''):
                f1 =  wrkPath + '_' + stamp[:-3] + '.jpg'
                f2 =  outPath + '_' + stamp[:-3] + '.jpg'
            else:
                f1 =  wrkPath + stamp[:-3] + inpText + '.jpg'
                f2 =  outPath + stamp[:-3] + inpText + '.jpg'
            os.rename(f0, f1)
            qFunc.copy(f1, f2)
            os.remove(f1)

            if (result == False):
                result = []
            result.append(f2)

    #except:
    #    pass

    #try:
    if (True):

        # 作業ディレクトリ
        qFunc.makeDirs(wrkPath, remove=True, )

        # 動画処理
        if (scene == None):
            ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFilev, \
                '-filter:v', 'fps=fps=' + str(sfps) + ':round=down, showinfo', \
                wrkPath + '%04d.jpg', \
                #'-loglevel', 'warning', \
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        else:
            ffmpeg = subprocess.Popen(['ffmpeg', '-i', inpFilev, \
                #'-filter:v', 'fps=fps=' + str(sfps) + ':round=down, select=gt(scene\,' + str(scene) + '), scale=0:0, showinfo', \
                '-filter:v', 'select=gt(scene\,' + str(scene) + '), scale=0:0, showinfo', \
                '-vsync', 'vfr', \
                wrkPath + '%04d.jpg', \
                #'-loglevel', 'warning', \
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        logb, errb = ffmpeg.communicate()
        ffmpeg.wait()
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
                        if (inpText == ''):
                            f1 =  wrkPath + '_' + stamp[:-3] + '.jpg'
                            f2 =  outPath + '_' + stamp[:-3] + '.jpg'
                        else:
                            f1 =  wrkPath + stamp[:-3] + inpText + '.jpg'
                            f2 =  outPath + stamp[:-3] + inpText + '.jpg'
                        os.rename(f0, f1)
                        qFunc.copy(f1, f2)
                        os.remove(f1)

                        if (result == False):
                            result = []
                        result.append(f2)

    #except:
    #    pass

    return result

def movie2mp4(inpPath='', inpNamev='', inpNamea='', outPath='', ):

    # パラメータ
    inpFilev = inpPath + inpNamev
    inpFilea = ''
    if (inpNamea != ''):
        inpFilea = inpPath + inpNamea
    if (outPath == ''):
        outPath = qPath_rec
    inpTime = inpNamev[:15]
    inpText = inpNamev[15:-4]
    if (inpText == ''):
        outFile = outPath + '_' + inpTime + '.___' + '.mp4'
    else:
        outFile = outPath + inpTime + '.___' + inpText + '.mp4'

    result = False

    #try:
    if (True):

        # 動画処理
        if (inpFilea == ''):
            ffmpeg = subprocess.Popen(['ffmpeg', \
                '-i', inpFilev, \
                '-vcodec', 'libx264', '-r', '2', \
                outFile, \
                '-loglevel', 'warning', \
                ], )
                #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        else:
            ffmpeg = subprocess.Popen(['ffmpeg', \
                '-i', inpFilev, '-i', inpFilea, \
                '-vcodec', 'libx264', '-r', '2', \
                '-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '44100', \
                outFile, \
                '-loglevel', 'warning', \
                ], )
                #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        #logb, errb = ffmpeg.communicate()
        ffmpeg.wait()
        ffmpeg.terminate()
        ffmpeg = None

        # 戻り値
        return [outFile]

    #except:
    #    pass

    return result

def movie_proc(proc_id, index, rec_filev, rec_namev, rec_filea, rec_namea, ):

    # ログ
    print(proc_id + ':thread ' + str(index) + ':start')

    # サムネイル抽出
    wrkPath = qPath_work + 'movie2jpg' + str(index) + '/'
    res = movie2jpg(inpPath=qPath_work, inpNamev=rec_namev, outPath=qPath_rec, wrkPath=wrkPath, sfps=1, scene=0.1, )
    if (res != False):
        for f in res:
            outFile = f.replace(qPath_rec, '')
            qFunc.copy(f, qPath_d_movie  + outFile)
            qFunc.copy(f, qPath_d_upload + outFile)

            # ログ
            print(proc_id + ':thread ' + str(index) + ':' + rec_namev + u' → ' + outFile)

    # 動画変換
    res = movie2mp4(inpPath=qPath_work, inpNamev=rec_namev, inpNamea=rec_namea, outPath = qPath_rec, )
    if (res != False):
        for f in res:
            outFile = f.replace(qPath_rec, '')
            qFunc.copy(f, qPath_d_movie  + outFile)
            qFunc.copy(f, qPath_d_upload + outFile)

            # ログ
            print(proc_id + ':thread ' + str(index) + ':' + rec_namev + u' → ' + outFile)

    # ワーク削除
    if (rec_filev != ''):
        qFunc.remove(rec_filev)
    if (rec_filea != ''):
        qFunc.remove(rec_filea)

    # ログ
    print(proc_id + ':thread ' + str(index) + ':complete')



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
        self.rec_max    = 10
        self.rec_ffmpeg = {}
        self.rec_sox    = {}
        self.rec_start  = {}
        self.rec_limit  = {}
        self.rec_filev  = {}
        self.rec_filea  = {}
        for i in range(1, self.rec_max+1):
            self.rec_ffmpeg[i] = None
            self.rec_sox[i]    = None
            self.rec_start[i]  = time.time()
            self.rec_limit[i]  = None
            self.rec_filev[i]  = ''
            self.rec_filea[i]  = ''
        self.batch_max    = 10
        self.batch_index  = 0
        self.batch_thread = {}
        for i in range(self.batch_max):
            self.batch_thread[i] = None

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

            # 制限時間、自動停止
            for i in range(1, self.rec_max+1):
                if (not self.rec_limit[i] is None):
                    if (time.time() > self.rec_limit[i]):
                        self.rec_limit[i] = None
                        
                        # 記録ストップ
                        if (not self.rec_ffmpeg[i] is None):
                            self.sub_stop(i, '_rec_stop_', )

            # 一定時間（5分毎）、自動リスタート
            for i in range(1, self.rec_max+1):
                if (not self.rec_ffmpeg[i] is None):
                    if (self.runMode != 'debug'):
                        limit_sec = 60 * 5
                    else:
                        limit_sec = 60 * 1
                    if ((time.time() - self.rec_start[i]) > limit_sec):

                        # 記録リスタート
                        self.sub_start(0, '_rec_restart_', )

                        # 記録ストップ
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
            if (qFunc.statusCheck(qBusy_dev_cpu, 0) == True):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)



        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # 記録終了
            self.sub_proc(u'記録終了')
            time.sleep(15.0)

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



    # 処理
    def sub_proc(self, proc_text, ):

        if (proc_text.find(u'リセット') >=0):

            # 全記録ストップ
            for i in range(1, self.rec_max+1):
                if (not self.rec_ffmpeg[i] is None):
                    self.sub_stop(i, '_rec_stop_', )

        elif (proc_text.lower() == '_rec_stop_') \
          or (proc_text.find(u'記録') >=0) and (proc_text.find(u'停止') >=0) \
          or (proc_text.find(u'記録') >=0) and (proc_text.find(u'終了') >=0) \
          or (proc_text.find(u'録画') >=0) and (proc_text.find(u'停止') >=0) \
          or (proc_text.find(u'録画') >=0) and (proc_text.find(u'終了') >=0):

            # 全記録ストップ
            for i in range(1, self.rec_max+1):
                if (not self.rec_ffmpeg[i] is None):
                    self.sub_stop(i, '_rec_stop_', )

        elif (proc_text.lower() == '_rec_start_') \
          or (proc_text.find(u'記録') >=0) \
          or (proc_text.find(u'録画') >=0):

            # 記録スタート
            self.sub_start(0, proc_text, )



    # 記録開始
    def sub_start(self, index, proc_text, ):

        # index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is None):
                    if (index == 0):
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
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_rec, True)

            # メッセージ
            if (proc_text.lower() == '_rec_start_') \
            or (proc_text.find(u'記録') >=0) \
            or (proc_text.find(u'録画') >=0):
                speechs = []
                speechs.append({ 'text':u'記録を開始します。', 'wait':0, })
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            elif (proc_text.lower() == '_rec_restart_'):
                speechs = []
                speechs.append({ 'text':u'記録は継続しています。', 'wait':0, })
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (proc_text.lower() == '_rec_start_') \
            or (proc_text.lower() == '_rec_restart_') \
            or (proc_text.find(u'記録') >=0) \
            or (proc_text.find(u'録画') >=0):

                # 記録・録音開始
                check = False
                while (check == False):

                    # デバイス名取得
                    cam, mic = dshow_dev()

                    # soxのチェック
                    sox_enable = check_sox()
                    #print('sox_enable', sox_enable)

                    nowTime    = datetime.datetime.now()
                    stamp      = nowTime.strftime('%Y%m%d.%H%M%S')
                    if (proc_text.lower() == '_rec_start_') \
                    or (proc_text.lower() == '_rec_restart_') \
                    or (proc_text.find(u'開始') >=0):
                        self.rec_start[index] = time.time()
                        self.rec_limit[index] = None
                        self.rec_filev[index] = qPath_work + stamp + '.flv'
                        self.rec_filea[index] = ''
                        if (len(mic) > 0) and (sox_enable == True):
                            self.rec_filea[index] = qPath_work + stamp + '.wav'
                    else:
                        rec_txt = '.' + qFunc.txt2filetxt(proc_text)
                        self.rec_start[index] = time.time()
                        if (self.runMode != 'debug'):
                            self.rec_limit[index] = time.time() + 60
                        else:
                            self.rec_limit[index] = time.time() + 30
                        self.rec_filev[index] = qPath_work + stamp + rec_txt + '.flv'
                        self.rec_filea[index] = ''
                        if (len(mic) > 0) and (sox_enable == True):
                            self.rec_filea[index] = qPath_work + stamp + rec_txt + '.wav'

                    # 記録開始
                    if (os.name != 'nt'):

                        # ffmpeg -f avfoundation -list_devices true -i ""
                        self.rec_ffmpeg[index] = subprocess.Popen(['ffmpeg', \
                                    '-f', 'avfoundation', \
                                    '-i', '1:2', \
                                    '-vcodec', 'flv1', \
                                    '-q:v', '0', \
                                    '-r', '5', self.rec_filev[index], \
                                    '-loglevel', 'warning', \
                                    ], stdin=subprocess.PIPE, )
                                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    else:

                        # ffmpeg -f gdigrab -i desktop -r 5 temp_flv.flv
                        # ffmpeg -f gdigrab -i desktop -f dshow -i audio="mic" -vcodec libx264 temp_mp4.mp4
                        if (len(mic) > 0) and (not qFunc.in_japanese(mic[0])):
                            microphone = 'audio="' + mic[0] + '"'
                            self.rec_ffmpeg[index] = subprocess.Popen(['ffmpeg', \
                                    '-f', 'gdigrab', '-i', 'desktop', \
                                    '-f', 'dshow', '-i', microphone, \
                                    '-vcodec', 'flv1', \
                                    '-q:v', '0', \
                                    '-r', '5', self.rec_filev[index], \
                                    '-loglevel', 'warning', \
                                    ], stdin=subprocess.PIPE, )
                                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                            if (self.rec_filea[index] != ''):
                                self.rec_filea[index] = ''

                            #cmd = 'ffmpeg -f gdigrab -i desktop -f dshow -i ' + microphone + ' -loglevel warning -r 5 ' + self.rec_filev[index]
                            #print(cmd)
                            #self.rec_ffmpeg[index] = subprocess.Popen(['powershell', ], \
                            #            stdin=subprocess.PIPE, )
                            #            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #self.rec_ffmpeg[index].stdin.write(b'chcp 65001\n')
                            #self.rec_ffmpeg[index].stdin.write(cmd.encode())
                            #self.rec_ffmpeg[index].stdin.write(b'\n')

                        else:

                            self.rec_ffmpeg[index] = subprocess.Popen(['ffmpeg', \
                                    '-f', 'gdigrab', '-i', 'desktop', \
                                    '-vcodec', 'flv1', \
                                    '-q:v', '0', \
                                    '-r', '5', self.rec_filev[index], \
                                    '-loglevel', 'warning', \
                                    ], stdin=subprocess.PIPE, )
                                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    # 録音開始
                    if (self.rec_filea[index] != ''):

                        self.rec_sox[index] = subprocess.Popen(['sox', \
                            '-q', '-d', '-r', '16000', '-b', '16', '-c', '1', \
                            self.rec_filea[index], \
                            ], stdin=subprocess.PIPE, )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    rec_namev = self.rec_filev[index].replace(qPath_work, '')
                    rec_namea = self.rec_filea[index].replace(qPath_work, '')

                    # 起動確認
                    time.sleep(1.00)

                    check = True
                    if (not os.path.exists(self.rec_filev[index])):
                        check = False
                    if (self.rec_filea[index] != ''):
                        if (not os.path.exists(self.rec_filea[index])):
                            check = False

                    if (check == False):
                        # ログ
                        qFunc.logOutput(self.proc_id + ':' + rec_namev + ' rec start error!', display=True,)

                        self.rec_ffmpeg[index].terminate()
                        self.rec_ffmpeg[index] = None
                        if (self.rec_filea[index] != ''):
                            self.rec_sox[index].terminate()
                            self.rec_sox[index] = None

                # ログ
                qFunc.logOutput(self.proc_id + ':' + rec_namev + ' rec start (ch=' + str(index) + ')', display=True,)
                if (self.rec_filea[index] != ''):
                    qFunc.logOutput(self.proc_id + ':' + rec_namea + ' rec start (ch=' + str(index) + ')', display=True,)



    # 記録停止
    def sub_stop(self, index, proc_text, ):

        # index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (not self.rec_ffmpeg[i] is None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # 停止処理
        rec_filev = ''
        rec_filea = ''
        rec_namev = ''
        rec_namea = ''
        if (index != 0):

            if (os.name != 'nt'):

                # 記録停止
                if (not self.rec_ffmpeg[index] is None):
                    self.rec_ffmpeg[index].stdin.write(b'q\n')
                    try:
                        self.rec_ffmpeg[index].stdin.flush()
                    except:
                        pass

                # 録音停止
                if (not self.rec_sox[index] is None):
                    self.rec_sox[index].send_signal(signal.SIGINT)
                    time.sleep(2.00)
                    #self.rec_sox[index].wait()
                    self.rec_sox[index].terminate()
                    self.rec_sox[index] = None

                #time.sleep(2.00)
                #self.rec_ffmpeg[index].send_signal(signal.SIGINT)

            else:

                # 記録停止
                if (not self.rec_ffmpeg[index] is None):
                    self.rec_ffmpeg[index].stdin.write(b'q\n')
                    try:
                        self.rec_ffmpeg[index].stdin.flush()
                    except:
                        pass

                # 録音停止
                if (not self.rec_sox[index] is None):
                    self.rec_sox[index].send_signal(signal.CTRL_C_EVENT)
                    time.sleep(2.00)
                    #self.rec_sox[index].wait()
                    self.rec_sox[index].terminate()
                    self.rec_sox[index] = None

                #time.sleep(2.00)
                #self.rec_ffmpeg[index].send_signal(signal.CTRL_C_EVENT)

            time.sleep(3.00)
            #logb, errb = self.rec_ffmpeg[index].communicate()
            #self.rec_ffmpeg[index].wait()
            self.rec_ffmpeg[index].terminate()
            self.rec_ffmpeg[index] = None

            # ログ
            rec_filev = self.rec_filev[index]
            rec_filea = self.rec_filea[index]
            rec_namev = rec_filev.replace(qPath_work, '')
            rec_namea = rec_filea.replace(qPath_work, '')
            if (os.path.exists(rec_filev)):
                    qFunc.logOutput(self.proc_id + ':' + rec_namev + ' rec stop (ch=' + str(index) + ')', display=True,)
            else:
                    qFunc.logOutput(self.proc_id + ':' + rec_namev + ' rec err  (ch=' + str(index) + ')', display=True,)
                    rec_filev = ''
                    rec_namev = ''
                    rec_filea = ''
                    rec_namea = ''
            if (rec_namea != ''):
                if (os.path.exists(rec_filea)):
                    qFunc.logOutput(self.proc_id + ':' + rec_namea + ' rec stop (ch=' + str(index) + ')', display=True,)
                else:
                    rec_filea = ''
                    rec_namea = ''

        # いちばん古い録画 -> index
        index = 0
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (not self.rec_ffmpeg[i] is None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # 録画中がなければリセット
        if (index == 0):
            #qFunc.kill('ffmpeg', )

            # メッセージ
            speechs = []
            speechs.append({ 'text':u'記録を終了しました。', 'wait':0, })
            qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_rec, False)

        # 後処理
        if (rec_filev != ''):
            #movie_proc(
            #    self.proc_id, self.batch_index,
            #    rec_filev, rec_namev, rec_filea, rec_namea,
            #    )

            # threading
            self.batch_thread[self.batch_index] = threading.Thread(target=movie_proc, args=(
                self.proc_id, self.batch_index,
                rec_filev, rec_namev, rec_filea, rec_namea,
                ))
            self.batch_thread[self.batch_index].setDaemon(True)
            self.batch_thread[self.batch_index].start()

            self.batch_index = (self.batch_index + 1) % self.batch_max



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

    # 初期設定
    qFunc.remove(qCtrl_control_desktop)
    qFunc.statusReset_desktop(False)

    # パラメータ
    runMode = 'debug'
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()

    # 開始
    recorder_thread = proc_recorder('recorder', '0', runMode, )
    recorder_thread.start()



    # テスト実行
    if (len(sys.argv) < 2):

        recorder_thread.put(['control', u'記録開始'])
        time.sleep(45)

        recorder_thread.put(['control', u'デスクトップの記録1'])
        time.sleep(45)

        recorder_thread.put(['control', u'デスクトップの記録2'])
        time.sleep(45)

        recorder_thread.put(['control', u'記録終了'])
        time.sleep(45)



    # 単体実行
    if (len(sys.argv) >= 2):

        # 記録開始
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

            # メッセージ
            res_data  = recorder_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            #if (res_name != ''):
            #    print(res_name, res_value, )

            time.sleep(0.50)



    # 終了
    recorder_thread.stop()
    del recorder_thread



