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

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_audio      = 'temp/control_audio.txt'
qCtrl_control_video      = 'temp/control_video.txt'

# 出力インターフェース
qCtrl_result_audio       = 'temp/result_audio.txt'
qCtrl_result_speech      = 'temp/result_speech.txt'
qCtrl_recognize          = 'temp/result_recognize.txt'
qCtrl_recognize_sjis     = 'temp/result_recognize_sjis.txt'
qCtrl_translate          = 'temp/result_translate.txt'
qCtrl_translate_sjis     = 'temp/result_translate_sjis.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS            = qFunc.getValue('qOS'           )
qHOSTNAME      = qFunc.getValue('qHOSTNAME'     )
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
qPath_v_msg    = qFunc.getValue('qPath_v_msg'   )
qPath_v_screen = qFunc.getValue('qPath_v_screen')

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
qBusy_v_rec    = qFunc.getValue('qBusy_v_rec'   )

# thread ルーチン群
import _v5_proc_controla
import _v5_proc_adintool
import _v5_proc_voice2wav
import _v5_proc_coreSTT
import _v5_proc_coreTTS
import _v5_proc_playvoice
import _v5_proc_txtreader

# julius 音声認識
import speech_api_julius



# debug
runMode      = 'hud'

qApiInp     = 'free'
qApiTrn     = 'free'
qApiOut     = qApiTrn
if (qOS == 'windows'):
    qApiOut = 'winos'
if (qOS == 'darwin'):
    qApiOut = 'macos'
qLangInp    = 'ja'
#qLangTrn    = 'en,fr,'
qLangTrn    = 'en'
qLangTxt    = qLangInp
qLangOut    = qLangTrn[:2]



class main_audio:

    def __init__(self, name='thread', id='0', runMode='debug',
                    micDev='0', micType='bluetooth', micGuide='on', micLevel='777',
                    qApiInp='free', qApiTrn='free', qApiOut='free',
                    qLangInp='ja', qLangTrn='en,fr,', qLangTxt='ja', qLangOut='en',
                    ):
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
        while (not self.proc_beat is None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.10)

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
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        fileRdy = qPath_work + self.proc_id + '.rdy'
        fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.remove(fileRdy)
        qFunc.remove(fileBsy)

        # 外部ＰＧリセット
        qFunc.kill('adintool-gui')
        qFunc.kill('adintool')
        qFunc.kill('julius')

        # 起動条件
        controla_thread  = None
        controla_switch  = 'on'
        adintool_thread  = None
        adintool_switch  = 'on'
        voice2wav_thread = None
        voice2wav_switch = 'on'
        coreSTT_thread   = None
        coreSTT_switch   = 'on'
        coreTTS_thread   = None
        coreTTS_switch   = 'on'
        playvoice_thread = None
        playvoice_switch = 'on'
        julius_thread    = None
        julius_switch    = 'on'
        sttreader_thread = None
        sttreader_switch = 'on'
        trareader_thread = None
        trareader_switch = 'on'

        if (self.runMode == 'debug'):
            julius_switch    = 'on'
            sttreader_switch = 'on'
            trareader_switch = 'on'
        if (self.runMode == 'handsfree'):
            julius_switch    = 'on'
            sttreader_switch = 'off'
            trareader_switch = 'off'
        if (self.runMode == 'translator'):
            julius_switch    = 'on'
            sttreader_switch = 'off'
            trareader_switch = 'on'
        if (self.runMode == 'speech') or (self.runMode == 'number'):
            julius_switch    = 'on'
            sttreader_switch = 'on'
            trareader_switch = 'off'
        if (self.runMode == 'hud'):
            julius_switch    = 'on'
            sttreader_switch = 'off'
            trareader_switch = 'off'
        if (self.runMode == 'camera'):
            julius_switch    = 'on'
            sttreader_switch = 'off'
            trareader_switch = 'off'

        if (not self.micDev.isdigit()):
            julius_switch    = 'off'
            sttreader_switch = 'off'
            trareader_switch = 'off'

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            txts, txt = qFunc.txtsRead(qCtrl_control_audio)
            if (txt == '_close_'):
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

            if (controla_thread is None) and (controla_switch == 'on'):
                controla_thread = _v5_proc_controla.proc_controla(
                                    name='controla', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                controla_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「音声制御」の機能が有効になりました。', 'wait':0, })

            if (not controla_thread is None) and (controla_switch != 'on'):
                controla_thread.stop()
                del controla_thread
                controla_thread = None

            if (adintool_thread is None) and (adintool_switch == 'on'):
                adintool_thread  = _v5_proc_adintool.proc_adintool(
                                    name='adintool', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                adintool_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「マイク入力」の機能が有効になりました。', 'wait':0, })

            if (not adintool_thread is None) and (adintool_switch != 'on'):
                adintool_thread.stop()                
                del adintool_thread
                adintool_thread = None

            if (voice2wav_thread is None) and (voice2wav_switch == 'on'):
                voice2wav_thread = _v5_proc_voice2wav.proc_voice2wav(
                                    name='voice2wave', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                voice2wav_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「音響補正」の機能が有効になりました。', 'wait':0, })

            if (not voice2wav_thread is None) and (voice2wav_switch != 'on'):
                voice2wav_thread.stop()                
                del voice2wav_thread
                voice2wav_thread = None

            if (coreSTT_thread is None) and (coreSTT_switch == 'on'):
                coreSTT_thread   = _v5_proc_coreSTT.proc_coreSTT(
                                    name='coreSTT', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel, 
                                    qApiInp=self.qApiInp, qApiTrn=self.qApiTrn, qApiOut=self.qApiOut,
                                    qLangInp=self.qLangInp, qLangTrn=self.qLangTrn, qLangTxt=self.qLangTxt, qLangOut=self.qLangOut,
                                    )
                coreSTT_thread.start()

                speechs = []
                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＡＩ音声認識」の機能が有効になりました。', 'wait':0, })
                    speechs.append({ 'text':u'「ＡＩ機械翻訳」の機能が有効になりました。', 'wait':0, })

            if (not coreSTT_thread is None) and (coreSTT_switch != 'on'):
                coreSTT_thread.stop()                
                del coreSTT_thread
                coreSTT_thread = None

            if (coreTTS_thread is None) and (coreTTS_switch == 'on'):
                coreTTS_thread   = _v5_proc_coreTTS.proc_coreTTS(
                                    name='coreTTS', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel, 
                                    qApiInp=self.qApiInp, qApiTrn=self.qApiTrn, qApiOut=self.qApiOut,
                                    qLangInp=self.qLangInp, qLangTrn=self.qLangTrn, qLangTxt=self.qLangTxt, qLangOut=self.qLangOut,
                                    )
                coreTTS_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＡＩ音声合成」の機能が有効になりました。', 'wait':0, })

            if (not coreTTS_thread is None) and (coreTTS_switch != 'on'):
                coreTTS_thread.stop()                
                del coreTTS_thread
                coreTTS_thread = None

            if (playvoice_thread is None) and (playvoice_switch == 'on'):
                playvoice_thread = _v5_proc_playvoice.proc_playvoice(
                                    name='playvoice', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                playvoice_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「スピーカー出力」の機能が有効になりました。', 'wait':0, })

            if (not playvoice_thread is None) and (playvoice_switch != 'on'):
                playvoice_thread.stop()                
                del playvoice_thread
                playvoice_thread = None

            if (julius_thread is None) and (julius_switch == 'on'):
                julius_thread    = speech_api_julius.proc_julius(
                                    name='julius', id='0', 
                                    runMode=self.runMode,
                                    )
                julius_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「ＪＵＬＩＵＳローカル音声認識」の機能が有効になりました。', 'wait':0, })

            if (not julius_thread is None) and (julius_switch != 'on'):
                julius_thread.stop()                
                del julius_thread
                julius_thread = None

            if (sttreader_thread is None) and (sttreader_switch == 'on'):
                sttreader_thread = _v5_proc_txtreader.proc_txtreader(
                                    name='sttreader', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, path='qPath_a_STT',
                                    )
                sttreader_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「音声認識結果のテキスト連携」の機能が有効になりました。', 'wait':0, })

            if (not sttreader_thread is None) and (sttreader_switch != 'on'):
                sttreader_thread.stop()                
                del sttreader_thread
                sttreader_thread = None

            if (trareader_thread is None) and (trareader_switch == 'on'):                                        
                trareader_thread = _v5_proc_txtreader.proc_txtreader(
                                    name='trareader', id='0', 
                                    runMode=runMode,
                                    micDev=self.micDev, path='qPath_a_TRA',
                                    )
                trareader_thread.start()

                if (self.runMode == 'debug') \
                or (self.runMode == 'handsfree'):
                    speechs.append({ 'text':u'「機械翻訳結果のテキスト連携」の機能が有効になりました。', 'wait':0, })

            if (not trareader_thread is None) and (trareader_switch != 'on'):
                trareader_thread.stop()                
                del trareader_thread
                trareader_thread = None

            if (len(speechs) != 0):
                qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if   (self.runMode == 'debug') \
                or   (self.runMode == 'handsfree') \
                or   (self.runMode == 'hud') \
                or   (self.runMode == 'camera'):
                    speechs = []
                    speechs.append({ 'text':u'「ハンズフリー機能」の準備が完了しました。', 'wait':0, })
                    qFunc.speech(id=self.proc_id, speechs=speechs, lang='', )

            # レディー設定
            if (not os.path.exists(fileRdy)):
                qFunc.txtsWrite(fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])

            # 処理
            if (True):

                # 音声ファイル処理（バッチ）時の自動終了
                if (not self.micDev.isdigit()):
                    if  ((time.time() - coreSTT_thread.proc_last) > 120) \
                    and ((time.time() - coreTTS_thread.proc_last) > 120):
                        qFunc.txtsWrite(qCtrl_control_audio, txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
                        break

                # 制御処理
                control = ''

                if (not controla_thread is None):
                    while (controla_thread.proc_r.qsize() != 0):
                        res_data  = controla_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == 'control'):
                            control = res_value
                            # 結果出力
                            if (cn_s.qsize() < 99):
                                cn_s.put([res_name, res_value])
                            break

                # マイク切り替え時、自動復旧処理
                if (control == ''):
                    if (self.micDev.isdigit()):
                        if  ((time.time() - voice2wav_thread.proc_last) > 30):
                            control = 'reset_mic'

                if (control == 'reset_mic'):
                    if (adintool_switch == 'on'):
                        adintool_thread.stop()
                    if (voice2wav_switch == 'on'):
                        voice2wav_thread.stop()
                    if (julius_switch == 'on'):
                        julius_thread.stop()
                    if (adintool_switch == 'on'):
                        adintool_thread.start()
                    if (voice2wav_switch == 'on'):
                        voice2wav_thread.start()
                    if (julius_switch == 'on'):
                        julius_thread.start()

                # 音声入力（マイク入力）
                if (not adintool_thread is None):
                    res_data  = adintool_thread.get()

                # 音声処理（前処理）
                if (not voice2wav_thread is None):
                    res_data  = voice2wav_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                # julius 音声認識（ローカル処理）
                if (not julius_thread is None):
                    if (res_name == 'filename'):
                        julius_thread.put(['filename', res_value])

                # ＡＩ音声認識（クラウド処理）
                if (not coreSTT_thread is None):
                    res_data  = coreSTT_thread.get()

                # ＡＩ音声合成（クラウド処理）
                if (not coreTTS_thread is None):
                    res_data  = coreTTS_thread.get()

                # 音声出力（スピーカー出力）
                if (not playvoice_thread is None):
                    res_data  = playvoice_thread.get()

                # julius 音声認識 外部インターフェース用
                if (not julius_thread is None):
                    res_data  = julius_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '[txts]'):

                        # 終了操作
                        if (res_value[0] == u'システムの終了') or (res_value[0] == u'カメラの終了'):
                            qFunc.txtsWrite(qCtrl_control_main,  txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
                            #qFunc.txtsWrite(qCtrl_control_audio, txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
                            break

                # 音声認識 外部インターフェース用
                if (not sttreader_thread is None):
                    res_data  = sttreader_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '[txts]'):
                        qFunc.notePad(txt=res_value[0])

                # 機械翻訳 外部インターフェース用
                if (not trareader_thread is None):
                    res_data  = trareader_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '[txts]'):
                        qFunc.notePad(txt=res_value[0])

            # ビジー解除
            qFunc.remove(fileBsy)

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_mic, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.50)
            else:
                time.sleep(0.25)

        # 終了処理
        if (True):

            # レディー解除
            qFunc.remove(fileRdy)

            # スレッド停止
            if (not controla_thread is None):
                controla_thread.stop()
                del controla_thread
                controla_thread = None

            if (not adintool_thread is None):
                adintool_thread.stop()                
                del adintool_thread
                adintool_thread = None

            if (not voice2wav_thread is None):
                voice2wav_thread.stop()                
                del voice2wav_thread
                voice2wav_thread = None

            if (not coreSTT_thread is None):
                coreSTT_thread.stop()                
                del coreSTT_thread
                coreSTT_thread = None

            if (not coreTTS_thread is None):
                coreTTS_thread.stop()                
                del coreTTS_thread
                coreTTS_thread = None

            if (not playvoice_thread is None):
                playvoice_thread.stop()                
                del playvoice_thread
                playvoice_thread = None

            if (not julius_thread is None):
                julius_thread.stop()                
                del julius_thread
                julius_thread = None

            if (not sttreader_thread is None):
                sttreader_thread.stop()                
                del sttreader_thread
                sttreader_thread = None

            if (not trareader_thread is None):
                trareader_thread.stop()                
                del trareader_thread
                trareader_thread = None

            # 外部ＰＧリセット
            qFunc.kill('adintool-gui')
            qFunc.kill('adintool')
            qFunc.kill('julius')

            # ビジー解除
            qFunc.remove(fileBsy)

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



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'main_audio'
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

    #runMode  debug, handsfree, translator, speech, number, hud, camera,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound
    #api      free, google, watson, azure, nict, winos, macos, docomo,
    #lang     ja, en, fr, kr...

    # パラメータ

    if (True):

        #runMode     = 'handsfree'
        micDev      = '0'
        micType     = 'bluetooth'
        micGuide    = 'on'
        micLevel    = '777'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        if (runMode == 'debug'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        if (runMode == 'handsfree'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        if (runMode == 'translator'):
            micType   = 'bluetooth'
            micGuide  = 'display'
        if (runMode == 'speech') or (runMode == 'number'):
            micType   = 'usb'
            micGuide  = 'display'
        if (runMode == 'hud'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        if (runMode == 'camera'):
            micType   = 'bluetooth'
            micGuide  = 'off'

        if (len(sys.argv) >= 3):
            micDev   = str(sys.argv[2]).lower()
            if (not micDev.isdigit()):
                micGuide = 'off' 
        if (len(sys.argv) >= 4):
            micType  = str(sys.argv[3]).lower()
        if (len(sys.argv) >= 5):
            micGuide = str(sys.argv[4]).lower()
        if (len(sys.argv) >= 6):
            p = str(sys.argv[5]).lower()
            if (p.isdigit() and p != '0'):
                micLevel = p

        if (len(sys.argv) >= 7):
            qApiInp  = str(sys.argv[6]).lower()
            if (qApiInp == 'google') or (qApiInp == 'watson') \
            or (qApiInp == 'azure')  or (qApiInp == 'nict'):
                qApiTrn  = qApiInp
                qApiOut  = qApiInp
            else:
                qApiTrn  = 'free'
                qApiOut  = 'free'
            if (qApiInp == 'nict'):
                #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
                qLangTrn = 'en,fr,es,id,zh,ko,'
                qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 8):
            qApiTrn  = str(sys.argv[7]).lower()
        if (len(sys.argv) >= 9):
            qApiOut  = str(sys.argv[8]).lower()
        if (len(sys.argv) >= 10):
            qLangInp = str(sys.argv[9]).lower()
            qLangTxt = qLangInp
        if (len(sys.argv) >= 11):
            qLangTrn = str(sys.argv[10]).lower()
            qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 12):
            qLangTxt = str(sys.argv[11]).lower()
        if (len(sys.argv) >= 13):
            qLangOut = str(sys.argv[12]).lower()

        qFunc.logOutput(main_id + ':runMode  =' + str(runMode  ))
        qFunc.logOutput(main_id + ':micDev   =' + str(micDev   ))
        qFunc.logOutput(main_id + ':micType  =' + str(micType  ))
        qFunc.logOutput(main_id + ':micGuide =' + str(micGuide ))
        qFunc.logOutput(main_id + ':micLevel =' + str(micLevel ))

        qFunc.logOutput(main_id + ':qApiInp  =' + str(qApiInp  ))
        qFunc.logOutput(main_id + ':qApiTrn  =' + str(qApiTrn  ))
        qFunc.logOutput(main_id + ':qApiOut  =' + str(qApiOut  ))
        qFunc.logOutput(main_id + ':qLangInp =' + str(qLangInp ))
        qFunc.logOutput(main_id + ':qLangTrn =' + str(qLangTrn ))
        qFunc.logOutput(main_id + ':qLangTxt =' + str(qLangTxt ))
        qFunc.logOutput(main_id + ':qLangOut =' + str(qLangOut ))

    # 初期設定

    qFunc.remove(qCtrl_control_audio     )

    qFunc.remove(qCtrl_result_audio       )
    qFunc.remove(qCtrl_result_speech      )
    qFunc.remove(qCtrl_recognize          )
    qFunc.remove(qCtrl_recognize_sjis     )
    qFunc.remove(qCtrl_translate          )
    qFunc.remove(qCtrl_translate_sjis     )

    qFunc.makeDirs(qPath_a_ctrl, True )
    if (micDev.isdigit()):
        qFunc.makeDirs(qPath_a_inp,  True )
    qFunc.makeDirs(qPath_a_wav,  True )
    qFunc.makeDirs(qPath_a_jul,  True )
    qFunc.makeDirs(qPath_a_STT,  True )
    qFunc.makeDirs(qPath_a_TRA,  True )
    if (micDev.isdigit()):
        qFunc.makeDirs(qPath_a_TTS,  True )
        qFunc.makeDirs(qPath_a_play, True )

    qFunc.busyReset_a(False)

    qFunc.busySet(qBusy_dev_cpu, False)
    qFunc.busySet(qBusy_dev_com, False)
    qFunc.busySet(qBusy_dev_mic, False)
    qFunc.busySet(qBusy_dev_spk, False)

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

        main_audio = main_audio('main_audio', '0', runMode=runMode,
                                micDev=micDev, micType=micType, micGuide=micGuide, micLevel=micLevel,
                                qApiInp=qApiInp, qApiTrn=qApiTrn, qApiOut=qApiOut,
                                qLangInp=qLangInp, qLangTrn=qLangTrn, qLangTxt=qLangTxt, qLangOut=qLangOut, )

        main_audio.start()

    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_audio)
        if (txt == '_close_'):
            break

        control = ''

        while (main_audio.proc_r.qsize() != 0) and (control == ''):
            res_data  = main_audio.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name == 'control'):
                control  = res_value
                break

        # 終了操作
        if (control == 'shutdown'):
            break



    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        # メインプロセス終了
        qFunc.txtsWrite(qCtrl_control_main      ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )

        time.sleep(10.00)

        # 外部ＰＧリセット
        qFunc.kill('adintool-gui')
        qFunc.kill('adintool')
        qFunc.kill('julius')

        main_audio.stop()
        time.sleep(20.00)
        del main_audio

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)


