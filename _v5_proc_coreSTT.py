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
qCtrl_control_speech     = 'temp/control_speech.txt'



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

# 音声処理 api
import       _v5_api_speech
api_speech = _v5_api_speech.api_speech_class()



class proc_coreSTT:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='on', micLevel='777', 
        qApiInp='free', qApiTrn='free', qApiOut='free',
        qLangInp='ja', qLangTrn='en,fr,', qLangTxt='ja', qLangOut='en', ):

        self.path      = qPath_s_wav

        self.runMode   = runMode
        self.micDev    = micDev
        self.micType   = micType
        self.micGuide  = micGuide
        self.micLevel  = micLevel

        self.qApiInp   = qApiInp
        self.qApiTrn   = qApiTrn
        self.qApiOut   = qApiOut
        self.qLangInp  = qLangInp
        self.qLangTrn  = qLangTrn
        self.qLangTxt  = qLangTxt
        self.qLangOut  = qLangOut

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



            # 処理
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

                        if (proc_file[-4:].lower() == '.wav' and proc_file[-8:].lower() != '.wrk.wav'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.wav'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass
                        if (proc_file[-4:].lower() == '.mp3' and proc_file[-8:].lower() != '.wrk.mp3'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.mp3'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.wav' or proc_file[-8:].lower() == '.wrk.mp3'):
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
                            work_file = qPath_work + work_name + '.wav'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            sox = subprocess.Popen(['sox', '-q', proc_file, '-r', '16000', '-b', '16', '-c', '1', work_file, ], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None

                            if (os.path.exists(work_file)):

                                #if (self.micDev.isdigit()):
                                os.remove(proc_file)

                                # ログ
                                if (self.runMode == 'debug') or (not self.micDev.isdigit()):
                                    qFunc.logOutput(self.proc_id + ':' + proc_name + u' → ' + work_name, display=self.logDisp,)

                                # 結果出力
                                if (cn_s.qsize() < 99):
                                    out_name  = 'filename'
                                    out_value = work_file
                                    cn_s.put([out_name, out_value])

                                # ビジー設定
                                if (qFunc.statusCheck(self.fileBsy) == False):
                                    qFunc.statusSet(self.fileBsy, True)
                                    if (str(self.id) == '0'):
                                        qFunc.statusSet(qBusy_s_STT, True)

                                    qFunc.statusWait_false(qBusy_s_ctrl, 3)
                                    if (self.micType == 'bluetooth') \
                                    or (self.micGuide == 'on' or self.micGuide == 'sound'):
                                        qFunc.statusWait_false(qBusy_s_inp, 3)

                                # 処理
                                self.proc_last = time.time()
                                self.sub_proc(seq4, proc_file, work_file, proc_name, )

                                time.sleep(1.00)

                #except:
                #    pass



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_STT, False)

            # アイドリング
            slow = False
            if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif (qFunc.statusCheck(qBusy_dev_mic) == True) \
            and  (qFunc.statusCheck(qRdy__s_force)   == False) \
            and  (qFunc.statusCheck(qRdy__s_sendkey) == False):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.25)
                else:
                    time.sleep(0.05)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_STT, False)

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



    def sub_proc(self, seq4, proc_file, work_file, proc_name, ):

        inpLang = self.qLangTxt
        trnLang = self.qLangTrn
        outLang = self.qLangOut

        if (self.runMode == 'debug') \
        or (self.runMode == 'learning'):
            inpInput = work_file
            inpOutput= qPath_s_STT  + proc_name + '.' + inpLang + '.txt'
            trnInput = inpOutput
            trnOutput= qPath_s_TRA  + proc_name + '.' + inpLang + '.' + trnLang[:2] + '.stt.translate.txt'
            txtInput = inpOutput
            txtOutput= qPath_s_play + proc_name + '.' + outLang + '.feedback.mp3'
            outInput = trnOutput
            outOutput= qPath_s_play + proc_name + '.' + outLang + '.voice.mp3'
            inpPlay  = 'off'
            txtPlay  = 'off'
            outPlay  = 'off'

        elif (self.runMode == 'live') \
        or   (self.runMode == 'translator'):
            inpInput = work_file
            inpOutput= qPath_s_STT  + proc_name + '.' + inpLang + '.txt'
            trnInput = inpOutput
            trnOutput= qPath_s_TRA  + proc_name + '.' + inpLang + '.' + trnLang[:2] + '.stt.translate.txt'
            txtInput = ''
            txtOutput= ''
            outInput = trnOutput
            outOutput= qPath_s_play + proc_name + '.' + outLang + '.voice.mp3'
            inpPlay  = 'off'
            txtPlay  = 'off'
            outPlay  = 'off'
        else: 
            inpInput = work_file
            inpOutput= qPath_s_STT  + proc_name + '.' + inpLang + '.txt'
            trnInput = ''
            trnOutput= ''
            if (not self.micDev.isdigit()):
                trnInput = inpOutput
                trnOutput= qPath_s_TRA  + proc_name + '.' + inpLang + '.' + trnLang[:2] + '.stt.translate.txt'
            txtInput = ''
            txtOutput= ''
            outInput = ''
            outOutput= ''
            inpPlay  = 'off'
            txtPlay  = 'off'
            outPlay  = 'off'

        if (self.qApiOut == 'none'):
            txtOutput= ''
            outOutput= ''



        if (True):
            sync = False
            if (not self.micDev.isdigit()):
                if (seq4[-1:] == '0'):
                    sync = True
            else:
                if ((self.micType == 'bluetooth') \
                and ((self.runMode == 'debug') \
                  or (self.runMode == 'live') \
                  or (self.runMode == 'translator'))):
                    #sync = True
                    pass

            res = api_speech.execute(sync,
                    self.runMode, self.micDev, 
                    self.qApiInp, self.qApiTrn, self.qApiOut, 
                    self.qLangInp, self.qLangTrn, self.qLangTxt, self.qLangOut,
                    'STT'+str(seq4), proc_name, 
                    inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, 
                    inpPlay, txtPlay, outPlay, 
                    )

            #api = subprocess.Popen(['python', '_v5_api_speech.py',
            #        self.runMode, self.micDev, 
            #        self.qApiInp, self.qApiTrn, self.qApiOut, 
            #        self.qLangInp, self.qLangTrn, self.qLangTxt, self.qLangOut,
            #        'STT'+str(seq4), proc_name, 
            #        inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput, 
            #        inpPlay, txtPlay, outPlay, 
            #        ],)
            #if (sync == True):
            #    api.wait()
            #    api.terminate()
            #    api = None

            #if (not self.micDev.isdigit()):
            #    if (sync == True):
            #        time.sleep(10.00)



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    # 初期設定
    qFunc.remove(qCtrl_control_speech)
    qFunc.statusReset_speech(False)

    # パラメータ
    runMode = 'debug'
    api     = 'free'
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        api      = str(sys.argv[2]).lower()

    # 開始
    coreSTT_thread = proc_coreSTT('coreSTT', '0', runMode, qApiInp=api)
    coreSTT_thread.begin()



    # テスト実行
    if (len(sys.argv) < 2):

        qFunc.copy('_sounds/_sound_hallo.wav', qPath_s_wav + '_sound_hallo.wav')

        chktime = time.time()
        while ((time.time() - chktime) < 15):

            res_data  = coreSTT_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                print(res_name, res_value, )

            if (coreSTT_thread.proc_s.qsize() == 0):
                coreSTT_thread.put(['_status_', ''])

            time.sleep(0.05)



    # 単体実行
    if (len(sys.argv) >= 2):

        # 待機ループ
        while (True):

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_speech)
            if (txts != False):
                qFunc.logOutput(str(txt))
                if (txt == '_end_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_speech)
                    control = txt

            # メッセージ
            res_data  = coreSTT_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            #if (res_name != ''):
            #    print(res_name, res_value, )

            time.sleep(0.50)



    # 終了
    coreSTT_thread.abort()
    del coreSTT_thread


