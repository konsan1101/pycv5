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

import cv2

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_desktop

qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'

# 出力インターフェース
qCtrl_result_capture      = 'temp/result_capture.jpg'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS             = qFunc.getValue('qOS'            )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
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



# thread ルーチン群
import _v5_proc_controld
import _v5_proc_capture
import _v5_proc_cvreader
import _v5_proc_recorder
import _v5_proc_uploader



# debug
runMode     = 'debug'



class main_desktop:

    def __init__(self, name='thread', id='0', runMode='debug', ):
        self.runMode   = runMode

        self.capStretch = '0'
        self.capRotate  = '0'
        self.capZoom    = '1'
        self.codeRead   = 'qr'

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

    def abort(self, waitMax=20, ):
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

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        # 外部ＰＧリセット
        qFunc.kill('ffmpeg')
        qFunc.kill('ffplay')

        # 起動条件
        controld_thread  = None
        controld_switch  = 'on'
        capture_thread   = None
        capture_switch   = 'on'
        cvreader_thread  = None
        cvreader_switch  = 'on'
        recorder_thread  = None
        recorder_switch  = 'on'
        uploader_thread  = None
        uploader_switch  = 'off'

        if (self.runMode == 'debug'):
            capture_switch   = 'on'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            uploader_switch  = 'on'
        elif (self.runMode == 'hud'):
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'on'
            uploader_switch  = 'off'
        elif (self.runMode == 'handsfree'):
            capture_switch   = 'off'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            uploader_switch  = 'off'
        elif (self.runMode == 'camera'):
            capture_switch   = 'off'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            uploader_switch  = 'on'
        elif (self.runMode == 'background'):
            capture_switch   = 'on'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            uploader_switch  = 'on'

        # 待機ループ
        self.proc_step = '5'

        main_img        = None

        cvreader_last_put  = time.time()
        cvreader_last_code = ''

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_'):
                    break

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

            # スレッド設定

            speechs = []

            if (controld_thread is None) and (controld_switch == 'on'):
                controld_thread = _v5_proc_controld.proc_controld(
                                    name='controld', id='0',
                                    runMode=self.runMode,
                                    )
                controld_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「デスクトップ制御」の機能が有効になりました。', 'wait':0, })

            if (not controld_thread is None) and (controld_switch != 'on'):
                controld_thread.abort()
                del controld_thread
                controld_thread = None

            if (capture_thread is None) and (capture_switch == 'on'):
                capture_thread = _v5_proc_capture.proc_capture(
                                    name='capture', id='0',
                                    runMode=self.runMode,
                                    capStretch=self.capStretch, capRotate=self.capRotate, capZoom=self.capZoom, capFps='5',
                                    )
                capture_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「デスクトップ入力」の機能が有効になりました。', 'wait':0, })

            if (not capture_thread is None) and (capture_switch != 'on'):
                capture_thread.abort()
                del capture_thread
                capture_thread = None

            if (cvreader_thread is None) and (cvreader_switch == 'on'):
                cvreader_thread = _v5_proc_cvreader.proc_cvreader(
                                    name='reader', id='d',
                                    runMode=self.runMode, 
                                    reader=self.codeRead,
                                    )
                cvreader_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「画面ＱＲコード認識」の機能が有効になりました。', 'wait':0, })

            if (not cvreader_thread is None) and (cvreader_switch != 'on'):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (recorder_thread is None) and (recorder_switch == 'on'):
                recorder_thread  = _v5_proc_recorder.proc_recorder(
                                    name='recorder', id='0',
                                    runMode=self.runMode,
                                    )
                recorder_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「デスクトップ記録」の機能が有効になりました。', 'wait':0, })

            if (not recorder_thread is None) and (recorder_switch != 'on'):
                recorder_thread.abort()
                del recorder_thread
                recorder_thread = None

            if (uploader_thread is None) and (uploader_switch == 'on'):
                uploader_thread  = _v5_proc_uploader.proc_uploader(
                                    name='uploader', id='0',
                                    runMode=self.runMode,
                                    )
                uploader_thread.begin()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ブロブ連携」の機能が有効になりました。', 'wait':0, })

            if (not uploader_thread is None) and (uploader_switch != 'on'):
                uploader_thread.abort()
                del uploader_thread
                uploader_thread = None

            if (len(speechs) != 0):
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if   (self.runMode == 'debug') \
                or   (self.runMode == 'handsfree'):
                    speechs = []
                    speechs.append({ 'text':u'「デスクトップ制御」の準備が完了しました。', 'wait':0, })
                    qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # レコーダー制御
            if (inp_name.lower() == 'recorder'):
                if (not recorder_thread is None):
                    recorder_thread.put(['control', inp_value])

            # 制御処理
            control = ''

            if (not controld_thread is None):
                while (controld_thread.proc_r.qsize() != 0):
                    res_data  = controld_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                    # 制御
                    if (res_name.lower() == 'control'):
                        control = res_value
                        # 結果出力
                        if (cn_s.qsize() < 99):
                            cn_s.put([res_name, res_value])
                        break

                    # レコーダー制御
                    if (res_name.lower() == 'recorder'):
                        if (not recorder_thread is None):
                            recorder_thread.put(['control', res_value])

            # 画像入力（デスクトップ）
            if (not capture_thread is None):
                while (capture_thread.proc_r.qsize() != 0):
                    res_data  = capture_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '_fps_'):
                        pass
                    if (res_name == '_reso_'):
                        pass
                    if (res_name == '[img]'):
                        main_img = res_value.copy()

                        # 画像識別（ＱＲ）
                        if ((time.time() - cvreader_last_put) >= 1):
                            if (not cvreader_thread is None):
                                if (cvreader_thread.proc_s.qsize() == 0):
                                    cvreader_thread.put(['[img]', main_img ])
                                    cvreader_last_put = time.time()

                        break

                # 画像合成（ＱＲ　識別結果）
                if (not cvreader_thread is None):
                    while (cvreader_thread.proc_r.qsize() != 0):
                        res_data  = cvreader_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[img]'):
                            pass
                        if (res_name == '[txts]'):

                            # コントロール出力
                            if (res_value[0][:1] == '_'):
                                nowTime = datetime.datetime.now()
                                stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                                controld_file = qPath_d_ctrl + stamp + '.txt'
                                qFunc.txtsWrite(controld_file, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )

                            # 画面表示
                            #qFunc.txtsWrite(qCtrl_control_browser, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )
                            #qFunc.txtsWrite(qCtrl_control_player, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )

                # 記録機能
                if (not recorder_thread is None):
                    res_data  = recorder_thread.get()

            # キャプチャ
            if (control == '_capture_'):
                if (not main_img is None):

                    # シャッター音
                    qFunc.guide('_shutter', sync=False)

                    # キャプチャ保存
                    nowTime = datetime.datetime.now()
                    stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                    self.save_capture(stamp, main_img)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif (qFunc.statusCheck(qBusy_dev_scn) == True) \
            and  (qFunc.statusCheck(qRdy__d_reader)  == False) \
            and  (qFunc.statusCheck(qRdy__d_sendkey) == False):
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

            # スレッド停止
            if (not controld_thread is None):
                controld_thread.abort()
                del controld_thread
                controld_thread = None

            if (not capture_thread is None):
                capture_thread.abort()
                del capture_thread
                capture_thread = None

            if (not cvreader_thread is None):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (not recorder_thread is None):
                recorder_thread.abort()
                del recorder_thread
                recorder_thread = None

            if (not uploader_thread is None):
                uploader_thread.abort()
                del uploader_thread
                uploader_thread = None

            # 外部ＰＧリセット
            qFunc.kill('ffmpeg')
            qFunc.kill('ffplay')

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



    def save_capture(self, stamp, main_img):

        # キャプチャ保存
        main_file = ''
        main_file = qPath_rec + stamp + '.capture.jpg'
        cv2.imwrite(main_file, main_img)
        #try:
        #    if (not main_img is None):
        #        main_file = qPath_rec + stamp + '.capture.jpg'
        #        cv2.imwrite(main_file, main_img)
        #except:
        #    main_file = ''

        # コピー保存
        filename_s1 = qPath_d_prtscn + stamp + '.capture.jpg'
        filename_s2 = qPath_d_upload + stamp + '.capture.jpg'
        filename_s3 = qCtrl_result_capture
        filename_s4 = qPath_pictures + stamp + '.capture.jpg'
        if (main_file != ''):
            qFunc.copy(main_file,   filename_s1)
            qFunc.copy(main_file,   filename_s2)
            qFunc.copy(main_file,   filename_s3)
            if (qPath_pictures != ''):
                qFunc.copy(main_file,   filename_s4)



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'desktop'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qFunc.init()

    # ログ設定

    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput(main_id + ':init')
    qFunc.logOutput(main_id + ':exsample.py runMode, mic..., ')

    #runMode  debug, hud, handsfree, translator, speech, number, camera, background,

    # パラメータ

    if (True):

        #runMode     = 'debug'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        qFunc.logOutput(main_id + ':runMode  =' + str(runMode  ))

    # 初期設定

    qFunc.remove(qCtrl_control_desktop  )

    qFunc.makeDirs(qPath_d_ctrl,   True )
    qFunc.makeDirs(qPath_d_play,   True )
    qFunc.makeDirs(qPath_d_prtscn, True )
    qFunc.makeDirs(qPath_d_movie,  True )
    qFunc.makeDirs(qPath_d_upload, True )

    qFunc.statusReset_desktop(False)

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

        main_desktop = main_desktop(main_id, '0', runMode=runMode, )

        main_desktop.begin()

    # 待機ループ

    while (True):

        # 終了確認

        control = ''
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            qFunc.logOutput(main_id + ':' + str(txt))
            if (txt == '_end_'):
                break
            else:
                qFunc.remove(qCtrl_control_self)
                control = txt

        # レコーダー制御
        if (control.lower() == '_rec_start_') \
        or (control.lower() == '_rec_stop_') \
        or (control.lower() == '_rec_restart_') \
        or (control.find(u'記録') >= 0) \
        or (control.find(u'録画') >= 0):
            main_desktop.put(['recorder', control])
            control = ''

        while (main_desktop.proc_r.qsize() != 0) and (control == ''):
            res_data  = main_desktop.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == 'control'):
                control  = res_value
                break

        # アイドリング
        slow = False
        if (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif (qFunc.statusCheck(qBusy_dev_scn) == True) \
        and  (qFunc.statusCheck(qRdy__d_reader)  == False) \
        and  (qFunc.statusCheck(qRdy__d_sendkey) == False):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.25)

    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        # 外部ＰＧリセット
        qFunc.kill('ffmpeg')
        qFunc.kill('ffplay')

        main_desktop.abort()
        del main_desktop

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)



