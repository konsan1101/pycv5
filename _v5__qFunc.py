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

import signal
import shutil

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux

qRUNATTR  = 'python'
if getattr(sys, 'frozen', False):
    qRUNATTR = 'exe'

import socket
qHOSTNAME = socket.gethostname().lower()

if (os.name == 'nt'):
    qUSERNAME = os.environ["USERNAME"]
else:
    qUSERNAME = os.environ["USER"]

import ctypes
import array

import unicodedata
import pyautogui
import pyperclip
import numpy as np
import cv2

from PIL import Image, ImageDraw, ImageFont
import io
if (os.name == 'nt'):
    import win32clipboard



qPath_pictures  = ''
qPath_videos    = ''
if (os.name == 'nt'):
    qPath_pictures  = 'C:/Users/' + qUSERNAME + '/Pictures/RiKi/'
    qPath_videos    = 'C:/Users/' + qUSERNAME + '/Videos/RiKi/'

qPath_cache     = '_cache/'
qPath_sounds    = '_sounds/'
qPath_icons     = '_icons/'
qPath_fonts     = '_fonts/'

qPath_log       = 'temp/_log/'
qPath_work      = 'temp/_work/'
qPath_rec       = 'temp/_recorder/'

qPath_s_ctrl    = 'temp/s5_0control/'
qPath_s_inp     = 'temp/s5_1voice/'
qPath_s_wav     = 'temp/s5_2wav/'
qPath_s_jul     = 'temp/s5_3stt_julius/'
qPath_s_STT     = 'temp/s5_4stt_txt/'
qPath_s_TTS     = 'temp/s5_5tts_txt/'
qPath_s_TRA     = 'temp/s5_6tra_txt/'
qPath_s_play    = 'temp/s5_7play/'
qPath_v_ctrl    = 'temp/v5_0control/'
qPath_v_inp     = 'temp/v5_1vision/'
qPath_v_jpg     = 'temp/v5_2jpg/'
qPath_v_detect  = 'temp/v5_3detect/'
qPath_v_cv      = 'temp/v5_5cv_txt/'
qPath_v_photo   = 'temp/v5_7photo/'
qPath_v_msg     = 'temp/v5_7photo_msg/'
qPath_d_ctrl    = 'temp/d5_0control/'
qPath_d_play    = 'temp/d5_1play/'
qPath_d_prtscn  = 'temp/d5_2screen/'
qPath_d_movie   = 'temp/d5_5movie/'
qPath_d_upload  = 'temp/d5_9upload/'

qBusy_dev_cpu   = qPath_work + 'busy_dev_cpu.txt'
qBusy_dev_com   = qPath_work + 'busy_dev_commnication.txt'
qBusy_dev_mic   = qPath_work + 'busy_dev_microphone.txt'
qBusy_dev_spk   = qPath_work + 'busy_dev_speaker.txt'
qBusy_dev_cam   = qPath_work + 'busy_dev_camera.txt'
qBusy_dev_dsp   = qPath_work + 'busy_dev_display.txt'
qBusy_dev_scn   = qPath_work + 'busy_dev_screen.txt'
qBusy_s_ctrl    = qPath_work + 'busy_s_0control.txt'
qBusy_s_inp     = qPath_work + 'busy_s_1audio.txt'
qBusy_s_wav     = qPath_work + 'busy_s_2wav.txt'
qBusy_s_STT     = qPath_work + 'busy_s_4stt_txt.txt'
qBusy_s_TTS     = qPath_work + 'busy_s_5tts_txt.txt'
qBusy_s_TRA     = qPath_work + 'busy_s_6tra_txt.txt'
qBusy_s_play    = qPath_work + 'busy_s_7play.txt'
qBusy_v_ctrl    = qPath_work + 'busy_v_0control.txt'
qBusy_v_inp     = qPath_work + 'busy_v_1video.txt'
qBusy_v_QR      = qPath_work + 'busy_v_2QR.txt'
qBusy_v_jpg     = qPath_work + 'busy_v_3jpg.txt'
qBusy_v_CV      = qPath_work + 'busy_v_5cv.txt'
qBusy_d_ctrl    = qPath_work + 'busy_d_0control.txt'
qBusy_d_inp     = qPath_work + 'busy_d_1screen.txt'
qBusy_d_QR      = qPath_work + 'busy_d_2QR.txt'
qBusy_d_rec     = qPath_work + 'busy_d_5rec.txt'
qBusy_d_play    = qPath_work + 'busy_d_7play.txt'
qBusy_d_browser = qPath_work + 'busy_d_8web.txt'
qBusy_d_upload  = qPath_work + 'busy_d_9blob.txt'
qRdy__s_force   = qPath_work + 'ready_s_force.txt'
qRdy__s_fproc   = qPath_work + 'ready_s_fproc.txt'
qRdy__s_sendkey = qPath_work + 'ready_s_sendkey.txt'
qRdy__v_reader  = qPath_work + 'ready_v_reder.txt'
qRdy__v_sendkey = qPath_work + 'ready_v_sendkey.txt'
qRdy__d_reader  = qPath_work + 'ready_d_reder.txt'
qRdy__d_sendkey = qPath_work + 'ready_d_sendkey.txt'



class qFunc_class:

    def __init__(self, ):
        self.qScreenWidth  = 0
        self.qScreenHeight = 0

        # フォント
        self.qFont_default = {'file':'_fonts/' + '_vision_font_ipaexg.ttf','offset':8}
        self.qFont_status  = {'file':'_fonts/' + '_vision_font_ipag.ttf',  'offset':8}
        self.qFont_zh = {'file':'C:/Windows/Fonts/msyh.ttc',   'offset':5 }
        self.qFont_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}
        self.qFont16_default  = ImageFont.truetype(self.qFont_default['file'], 16, encoding='unic')
        self.qFont16_defaulty =                    self.qFont_default['offset']


        # ガイド表示
        self.qGuide_panel  = '5'
        self.qGuide_left   = 0
        self.qGuide_top    = 0
        self.qGuide_width  = 320
        self.qGuide_height = 240
        self.qGuide_img    = None
        self.qGuide_title  = 'qGuide'

    def __del__(self, ):
        pass
                
    def init(self, ):
        self.makeDirs('temp/_log/',   False)
        self.makeDirs(qPath_cache,    False)

        self.makeDirs(qPath_log,      False)
        self.makeDirs(qPath_work,     False)
        self.makeDirs(qPath_rec,      False)

        self.makeDirs(qPath_s_ctrl,   False)
        self.makeDirs(qPath_s_inp,    False)
        self.makeDirs(qPath_s_wav,    False)
        self.makeDirs(qPath_s_jul,    False)
        self.makeDirs(qPath_s_STT,    False)
        self.makeDirs(qPath_s_TTS,    False)
        self.makeDirs(qPath_s_TRA,    False)
        self.makeDirs(qPath_s_play,   False)
        self.makeDirs(qPath_v_ctrl,   False)
        self.makeDirs(qPath_v_inp,    False)
        self.makeDirs(qPath_v_jpg,    False)
        self.makeDirs(qPath_v_detect, False)
        self.makeDirs(qPath_v_cv,     False)
        self.makeDirs(qPath_v_photo,  False)
        self.makeDirs(qPath_v_msg,    False)
        self.makeDirs(qPath_d_ctrl,   False)
        self.makeDirs(qPath_d_play,   False)
        self.makeDirs(qPath_d_prtscn, False)
        self.makeDirs(qPath_d_movie,  False)
        self.makeDirs(qPath_d_upload, False)

        if (qPath_pictures != ''):
            self.makeDirs(qPath_pictures, False)
        if (qPath_videos != ''):
            self.makeDirs(qPath_videos,   False)

        return True

    def getValue(self, field):
        if (field == 'qPLATFORM'       ): return qPLATFORM
        if (field == 'qRUNATTR'        ): return qRUNATTR
        if (field == 'qHOSTNAME'       ): return qHOSTNAME
        if (field == 'qUSERNAME'       ): return qUSERNAME
        if (field == 'qPath_pictures'  ): return qPath_pictures
        if (field == 'qPath_videos'    ): return qPath_videos
        if (field == 'qPath_cache'     ): return qPath_cache
        if (field == 'qPath_sounds'    ): return qPath_sounds
        if (field == 'qPath_icons'     ): return qPath_icons
        if (field == 'qPath_fonts'     ): return qPath_fonts

        if (field == 'qPath_log'       ): return qPath_log
        if (field == 'qPath_work'      ): return qPath_work
        if (field == 'qPath_rec'       ): return qPath_rec

        if (field == 'qPath_s_ctrl'    ): return qPath_s_ctrl
        if (field == 'qPath_s_inp'     ): return qPath_s_inp
        if (field == 'qPath_s_wav'     ): return qPath_s_wav
        if (field == 'qPath_s_jul'     ): return qPath_s_jul
        if (field == 'qPath_s_STT'     ): return qPath_s_STT
        if (field == 'qPath_s_TTS'     ): return qPath_s_TTS
        if (field == 'qPath_s_TRA'     ): return qPath_s_TRA
        if (field == 'qPath_s_play'    ): return qPath_s_play
        if (field == 'qPath_v_ctrl'    ): return qPath_v_ctrl
        if (field == 'qPath_v_inp'     ): return qPath_v_inp
        if (field == 'qPath_v_jpg'     ): return qPath_v_jpg
        if (field == 'qPath_v_detect'  ): return qPath_v_detect
        if (field == 'qPath_v_cv'      ): return qPath_v_cv
        if (field == 'qPath_v_photo'   ): return qPath_v_photo
        if (field == 'qPath_v_msg'     ): return qPath_v_msg
        if (field == 'qPath_d_ctrl'    ): return qPath_d_ctrl
        if (field == 'qPath_d_play'    ): return qPath_d_play
        if (field == 'qPath_d_prtscn'  ): return qPath_d_prtscn
        if (field == 'qPath_d_movie'   ): return qPath_d_movie
        if (field == 'qPath_d_upload'  ): return qPath_d_upload

        if (field == 'qBusy_dev_cpu'   ): return qBusy_dev_cpu
        if (field == 'qBusy_dev_com'   ): return qBusy_dev_com
        if (field == 'qBusy_dev_mic'   ): return qBusy_dev_mic
        if (field == 'qBusy_dev_spk'   ): return qBusy_dev_spk
        if (field == 'qBusy_dev_cam'   ): return qBusy_dev_cam
        if (field == 'qBusy_dev_dsp'   ): return qBusy_dev_dsp
        if (field == 'qBusy_dev_scn'   ): return qBusy_dev_scn
        if (field == 'qBusy_s_ctrl'    ): return qBusy_s_ctrl
        if (field == 'qBusy_s_inp'     ): return qBusy_s_inp
        if (field == 'qBusy_s_wav'     ): return qBusy_s_wav
        if (field == 'qBusy_s_STT'     ): return qBusy_s_STT
        if (field == 'qBusy_s_TTS'     ): return qBusy_s_TTS
        if (field == 'qBusy_s_TRA'     ): return qBusy_s_TRA
        if (field == 'qBusy_s_play'    ): return qBusy_s_play
        if (field == 'qBusy_v_ctrl'    ): return qBusy_v_ctrl
        if (field == 'qBusy_v_inp'     ): return qBusy_v_inp
        if (field == 'qBusy_v_QR'      ): return qBusy_v_QR
        if (field == 'qBusy_v_jpg'     ): return qBusy_v_jpg
        if (field == 'qBusy_v_CV'      ): return qBusy_v_CV
        if (field == 'qBusy_d_ctrl'    ): return qBusy_d_ctrl
        if (field == 'qBusy_d_inp'     ): return qBusy_d_inp
        if (field == 'qBusy_d_QR'      ): return qBusy_d_QR
        if (field == 'qBusy_d_rec'     ): return qBusy_d_rec
        if (field == 'qBusy_d_play'    ): return qBusy_d_play
        if (field == 'qBusy_d_browser' ): return qBusy_d_browser
        if (field == 'qBusy_d_upload'  ): return qBusy_d_upload
        if (field == 'qRdy__s_force'   ): return qRdy__s_force
        if (field == 'qRdy__s_fproc'   ): return qRdy__s_fproc
        if (field == 'qRdy__s_sendkey' ): return qRdy__s_sendkey
        if (field == 'qRdy__v_reader'  ): return qRdy__v_reader
        if (field == 'qRdy__v_sendkey' ): return qRdy__v_sendkey
        if (field == 'qRdy__d_reader'  ): return qRdy__d_reader
        if (field == 'qRdy__d_sendkey' ): return qRdy__d_sendkey

        print('check program !' + field)
        return None

    def makeDirs(self, ppath, remove=False, ):
        try:
            if (len(ppath) > 0):
                path=ppath.replace('\\', '/')
                if (path[-1:] != '/'):
                    path += '/'
                if (not os.path.isdir(path[:-1])):
                    os.makedirs(path[:-1])
                else:
                    if (remove != False):
                        files = glob.glob(path + '*')
                        for f in files:
                            if (remove == True):
                                try:
                                    self.remove(f)
                                except Exception as e:
                                    pass
                            if (str(remove).isdigit()):
                                try:
                                    nowTime   = datetime.datetime.now()
                                    fileStamp = os.path.getmtime(f)
                                    fileTime  = datetime.datetime.fromtimestamp(fileStamp)
                                    td = nowTime - fileTime
                                    if (td.days >= int(remove)):
                                        self.remove(f)
                                except Exception as e:
                                    pass

        except Exception as e:
            pass
        return True

    def kill(self, name, ):
        if (os.name == 'nt'):
            try:
                kill = subprocess.Popen(['taskkill', '/im', name + '.exe', '/f', ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-f', name, ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        return False

    def remove(self, filename, maxWait=1, ):
        if (not os.path.exists(filename)):
            return True

        if (maxWait == 0):
            try:
                os.remove(filename) 
                return True
            except Exception as e:
                return False
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) <= maxWait):
                try:
                    os.remove(filename)
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)

            if (not os.path.exists(filename)):
                return True
            else:
                return False

    def copy(self, fromFile, toFile, ):
        try:
            shutil.copy2(fromFile, toFile)
            return True
        except Exception as e:
            return False

    def txtsWrite(self, filename, txts=[''], encoding='utf-8', exclusive=False, mode='w', ):
        if (exclusive == False):
            try:
                w = codecs.open(filename, mode, encoding)
                for txt in txts:
                    if (encoding != 'shift_jis'):
                        w.write(txt + '\n')
                    else:
                        w.write(txt + '\r\n')
                w.close()
                w = None
                return True
            except Exception as e:
                w = None
                return False
        else:
            res = self.remove(filename, )
            if (res == False):
                return False
            else:
                f2 = filename[:-4] + '.tmp.txt'
                res = self.remove(f2, )
                if (res == False):
                    return False
                else:
                    try:
                        w = codecs.open(f2, mode, encoding)
                        for txt in txts:
                            if (encoding != 'shift_jis'):
                                w.write(txt + '\n')
                            else:
                                w.write(txt + '\r\n')
                        w.close()
                        w = None
                        os.rename(f2, filename)
                        return True
                    except Exception as e:
                        w = None
                        return False

    def txtsRead(self, filename, encoding='utf-8', exclusive=False, ):
        if (not os.path.exists(filename)):
            return False, ''

        encoding2 = encoding
        if (encoding2 == 'utf-8'):
            encoding2 =  'utf-8-sig'

        if (exclusive == False):
            try:
                txts = []
                txt  = ''
                r = codecs.open(filename, 'r', encoding2)
                for t in r:
                    t = t.replace('\n', '')
                    t = t.replace('\r', '')
                    txt  = (txt + ' ' + str(t)).strip()
                    txts.append(t)
                r.close
                r = None
                return txts, txt
            except Exception as e:
                r = None
                return False, ''
        else:
            f2 = filename[:-4] + '.wrk.txt'
            res = self.remove(f2, )
            if (res == False):
                return False
            else:
                try:
                    os.rename(filename, f2)
                    txts = []
                    txt  = ''
                    r = codecs.open(f2, 'r', encoding2)
                    for t in r:
                        t = t.replace('\n', '')
                        t = t.replace('\r', '')
                        txt = (txt + ' ' + str(t)).strip()
                        txts.append(t)
                    r.close
                    r = None
                    self.remove(f2, )
                    return txts, txt
                except Exception as e:
                    r = None
                    return False, ''

    def txtFilePath(self, txt='',):
        if (txt == ''):
            return False
        chk = txt.replace('\\','/')
        if (os.path.isfile(chk)) \
        or (os.path.isdir(chk)):
            return chk
        return False

    def txt2filetxt(self, txt='', ):
        ftxt = txt.replace(' ','_')
        ftxt = ftxt.replace(u'　','_')
        ftxt = ftxt.replace(u'、','_')
        ftxt = ftxt.replace(u'。','_')
        ftxt = ftxt.replace('"','_')
        ftxt = ftxt.replace('$','_')
        ftxt = ftxt.replace('%','_')
        ftxt = ftxt.replace('&','_')
        ftxt = ftxt.replace("'",'_')
        ftxt = ftxt.replace('\\','_')
        ftxt = ftxt.replace('|','_')
        ftxt = ftxt.replace('*','_')
        ftxt = ftxt.replace('/','_')
        ftxt = ftxt.replace('?','_')
        ftxt = ftxt.replace(':',',')
        ftxt = ftxt.replace('<','_')
        ftxt = ftxt.replace('>','_')
        return ftxt



    def findWindow(self, winTitle='Display', ):
        if (os.name != 'nt'):
            return False
        parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
        if (parent_handle == 0):
            return False
        else:
            return parent_handle

    def moveWindowSize(self, winTitle='Display', posX=0, posY=0, dspMode='full+', ):
        if (os.name != 'nt'):
            return False
        parent_handle = self.findWindow(winTitle)
        if (parent_handle == False):
            return False
        else:
            dspWidth, dspHeight = self.getResolution(dspMode)
            HWND_TOP = 0
            SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(parent_handle, HWND_TOP, posX, posY, dspWidth, dspHeight, SWP_SHOWWINDOW)
            return True

    def setForegroundWindow(self, winTitle='Display', ):
        if (os.name != 'nt'):
            return False
        parent_handle = self.findWindow(winTitle)
        if (parent_handle == False):
            return False
        else:
            ctypes.windll.user32.SetForegroundWindow(parent_handle)
            return True



    def img2clip(self, file):
        if (os.name == 'nt'):
            #try:
                img = Image.open(file)
                output = io.BytesIO()
                img.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                return True
            #except Exception as e:
            #    pass
        return False



    def in_japanese(self, txt=''):
        t = txt.replace('\r', '')
        t = t.replace('\n', '')
        try:
            for s in t:
                name = unicodedata.name(s) 
                if ('CJK UNIFIED' in name) \
                or ('HIRAGANA' in name) \
                or ('KATAKANA' in name):
                    return True
        except Exception as e:
            pass
        return False

    def checkWakeUpWord(self, txt='', ):
        if (txt == u'力') or (txt == u'りき') or (txt == u'リッキー') \
        or (txt == u'三木') or (txt == u'ミキ') or (txt == u'ミッキー') \
        or (txt == u'ウィキ') \
        or (txt.lower() == 'riki') \
        or (txt.lower() == 'miki') or (txt.lower() == 'mickey') \
        or (txt.lower() == 'wiki') \
        or (txt == u'フォース') or (txt.lower() == 'force') \
        or (txt[:6] == u'コンピュータ') or (txt.lower() == 'computer'):
            return True
        else:
            return False

    def sendKey(self, txt='', cr=True, lf=False ):
        out_txt = txt
        if (cr==True) or (lf==True):
            out_txt = out_txt.replace('\r', '')
            out_txt = out_txt.replace('\n', '')

        if (self.checkWakeUpWord(out_txt) == True):
            return False

        pyperclip.copy(out_txt)
        pyautogui.hotkey('ctrl', 'v')

        if (cr==True) or (lf==True):
            pyautogui.typewrite(['enter',])

        return True

    def notePad(self, txt='', cr=True, lf=False, ):
        winTitle  = u'無題 - メモ帳'
        if (os.name != 'nt'):
            return False

        parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
        if (parent_handle == 0):
            return False
        else:
            out_txt = txt
            if (cr==True) or (lf==True):
                out_txt = out_txt.replace('\r', '')
                out_txt = out_txt.replace('\n', '')
            if (cr==True):
                out_txt += '\r'
            if (lf==True):
                out_txt += '\n'

            if (True):
            #try:
                child_handles = array.array('i')
                ENUM_CHILD_WINDOWS = ctypes.WINFUNCTYPE( \
                                    ctypes.c_int, \
                                    ctypes.c_int, \
                                    ctypes.py_object)
                ctypes.windll.user32.EnumChildWindows( \
                                    parent_handle, \
                                    ENUM_CHILD_WINDOWS(self.enum_child_windows_proc), \
                                    ctypes.py_object(child_handles) )
                WM_CHAR = 0x0102
                for i in range(len(out_txt)):
                    ctypes.windll.user32.SendMessageW(child_handles[0], WM_CHAR, (ord(out_txt[i])), 0)
                return True
            #except Exception as e:
            #    return False

    def enum_child_windows_proc(self, handle, list):
        list.append(handle)
        return 1

    def guideSound(self, filename=None, sync=True):
        if (self.statusCheck(qBusy_dev_spk) == True):
            #self.logOutput('spk_busy!_:' + filename, )
            return False

        playfile = filename
        if (filename == '_up'):
            playfile = qPath_sounds + '_sound_up.mp3'
        if (filename == '_ready'):
            playfile = qPath_sounds + '_sound_ready.mp3'
        if (filename == '_accept'):
            playfile = qPath_sounds + '_sound_accept.mp3'
        if (filename == '_ok'):
            playfile = qPath_sounds + '_sound_ok.mp3'
        if (filename == '_ng'):
            playfile = qPath_sounds + '_sound_ng.mp3'
        if (filename == '_down'):
            playfile = qPath_sounds + '_sound_down.mp3'
        if (filename == '_shutter'):
            playfile = qPath_sounds + '_sound_shutter.mp3'

        if (os.path.exists(playfile)):

            sox=subprocess.Popen(['sox', '-q', playfile, '-d', ], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            if (sync == True):
                sox.wait()
                sox.terminate()
                sox = None

            return True

        return False

    def cv2pil(self, cv2_image=None):
        wrk_image = cv2_image.copy()
        if (wrk_image.ndim == 2):  # モノクロ
            pass
        elif (wrk_image.shape[2] == 3):  # カラー
            wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGR2RGB)
        elif (wrk_image.shape[2] == 4):  # 透過
            wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGRA2RGBA)
        pil_image = Image.fromarray(wrk_image)
        return pil_image

    def pil2cv(self, pil_image=None):
        cv2_image = np.array(pil_image, dtype=np.uint8)
        if (cv2_image.ndim == 2):  # モノクロ
            pass
        elif (cv2_image.shape[2] == 3):  # カラー
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
        elif (cv2_image.shape[2] == 4):  # 透過
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGBA2BGRA)
        return cv2_image

    def getPanelPos(self, id='0-', ):
        #left, top, width, height = getPanelPos(panel,)

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
        elif (id == '5+'):
            return int(w/4), int(h/4), int(w/2), int(h/2)
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

    def guideDisplay(self, display=True, panel='', filename='', txt='', ):
        if (panel != ''):
            self.qGuide_panel = panel
        if (filename != ''):
            imgfile = filename
            if (filename == '_kernel_start_'):
                imgfile = qPath_icons + 'RiKi_start.png'
            if (filename == '_kernel_stop_'):
                imgfile = qPath_icons + 'RiKi_stop.png'
            if (filename == '_kernel_guide_'):
                imgfile = qPath_icons + 'RiKi_guide.png'
            if (filename == '_speech_start_'):
                imgfile = qPath_icons + 'speech_start.png'
            if (filename == '_speech_stop_'):
                imgfile = qPath_icons + 'speech_stop.png'
            if (filename == '_speech_guide_'):
                imgfile = qPath_icons + 'speech_guide.png'
            if (filename == '_vision_start_'):
                imgfile = qPath_icons + 'cam_start.png'
            if (filename == '_vision_stop_'):
                imgfile = qPath_icons + 'cam_stop.png'
            if (filename == '_vision_guide_'):
                imgfile = qPath_icons + 'cam_guide.png'
            if (filename == '_desktop_start_'):
                imgfile = qPath_icons + 'rec_start.png'
            if (filename == '_desktop_stop_'):
                imgfile = qPath_icons + 'rec_stop.png'
            if (filename == '_desktop_guide_'):
                imgfile = qPath_icons + 'rec_guide.png'
            self.qGuide_img = None
            try:
                self.qGuide_img = cv2.imread(imgfile)
            except Exception as e:
                pass

            # 表示位置
            if  (self.qGuide_panel != 'detect_face') \
            and (self.qGuide_panel != 'detect_speech'):
                self.qGuide_title = 'Guide_' + self.qGuide_panel
                self.qGuide_left, self.qGuide_top, self.qGuide_width, self.qGuide_height = self.getPanelPos(self.qGuide_panel,)
                if (filename.find('guide') >= 0):
                    self.qGuide_height = int(self.qGuide_height/4)
                    if (self.qGuide_panel == '7') \
                    or (self.qGuide_panel == '8') \
                    or (self.qGuide_panel == '9'):
                        self.qGuide_top += (self.qGuide_height * 3)
                if (os.name == 'nt'):
                    if (self.qGuide_panel == '7') \
                    or (self.qGuide_panel == '8') \
                    or (self.qGuide_panel == '9'):
                        self.qGuide_top -= 50
            else:
                w, h = pyautogui.size()
                chksec9 = int(time.time()) % 10
                chksec2 = (int(time.time()) % 2)
                self.qGuide_left = int(w * (chksec9 * 0.1))
                self.qGuide_top  = int(h * (chksec2 * 0.1))

                # 顔画像リサイズ
                if (not self.qGuide_img is None):
                    image_height, image_width = self.qGuide_img.shape[:2]
                    self.qGuide_width  = int(w / 10)
                    self.qGuide_height = int(self.qGuide_width * image_height / image_width)
                    self.qGuide_img = cv2.resize(self.qGuide_img, (self.qGuide_width, self.qGuide_height))

            if  (self.qGuide_panel == 'detect_face'):
                self.qGuide_title = 'Face_' + str(chksec9)
                self.qGuide_top  += int(h * 0.1)

            if  (self.qGuide_panel == 'detect_speech'):
                self.qGuide_title = 'Speech_' + str(chksec9)
                self.qGuide_top  += int(h * 0.3)

        # ベース画像
        img = None
        if (not self.qGuide_img is None):
            if  (self.qGuide_panel != 'detect_face') \
            and (self.qGuide_panel != 'detect_speech'):
                img = cv2.resize(self.qGuide_img, (self.qGuide_width,self.qGuide_height))
            else:
                img = self.qGuide_img.copy()

        if (display == True) and (not img is None):
            #try:
                if (txt != ''):
                    #cv2.putText(img, txt, (5,self.qGuide_height-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                    pil_image = self.cv2pil(img)
                    text_draw = ImageDraw.Draw(pil_image)
                    text_draw.text((10, self.qGuide_height-26), txt, font=self.qFont16_default, fill=(255,0,255))
                    img = self.pil2cv(pil_image)

                if (os.name == 'nt'):
                    cv2.namedWindow(self.qGuide_title, 1)
                    cv2.moveWindow( self.qGuide_title, self.qGuide_left, self.qGuide_top-30)
                    cv2.imshow(     self.qGuide_title, img )
                    cv2.moveWindow( self.qGuide_title, self.qGuide_left, self.qGuide_top-30)
                    cv2.waitKey(1)
                #else:
                #    rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                #    plt.imshow(rgb)
                #    plt.show()
                return True
            #except Exception as e:
            #    return False

        if (display == False):
            try:
                if (os.name == 'nt'):
                    cv2.destroyWindow(self.qGuide_title)
                    #cv2.destroyAllWindow()
                    cv2.waitKey(1)
                #else:
                #    plt.close('all')
                return True
            except Exception as e:
                return False

    def getResolution(self, reso='full', ):
        if (reso == 'full')  \
        or (reso == 'full+') \
        or (reso == 'full-'):
            if (self.qScreenWidth == 0):
                try:
                    self.qScreenWidth, self.qScreenHeight = pyautogui.size()
                except Exception as e:
                    self.qScreenHeight =  720
                    self.qScreenWidth  = 1280

        if   (reso == 'full'): 
            return self.qScreenWidth, self.qScreenHeight
        if   (reso == 'full+'):
            return self.qScreenWidth + 90, self.qScreenHeight + 50
        if   (reso == 'full-'):
            return int(self.qScreenWidth*0.8), int(self.qScreenHeight*0.8)
        elif (reso == 'half'):
            return int(self.qScreenWidth/2), int(self.qScreenHeight/2)

        elif (reso=='4k'):
                return 4096,2160
        elif (reso=='2k'):
                return 2048,1080
        elif (reso=='hdtv') or (reso=='1920x1080'):
                return 1920,1080
        elif (reso=='uxga'):
                return 1600,1200
        elif (reso=='720p') or (reso=='1280x720'):
                return 1280,720
        elif (reso=='xga') or (reso=='1024x768'):
                return 1024,768
        elif (reso=='svga') or (reso=='800x600'):
                return 800,600
        elif (reso=='dvd'):
                return 720,480
        elif (reso=='vga') or (reso=='640x480'):
                return 640,480
        elif (reso=='qvga') or (reso=='320x240'):
                return 320,240
        elif (reso=='160x120'):
                return 160,120
        print('getResolution error ' + reso + ', -> 640,480')
        return 640,480

    def statusSet(self, file, Flag=True, txt='_on_'):
        if (Flag == True):
            chktime = time.time()
            while (not os.path.exists(file)) and ((time.time() - chktime) < 1):
                try:
                    w = open(file, 'w')
                    w.write(txt)
                    w.close()
                    w = None
                    return True
                except Exception as e:
                    w = None
                time.sleep(0.10)
        else:
            chktime = time.time()
            while (os.path.exists(file)) and ((time.time() - chktime) < 1):
                try:
                    self.remove(file, )
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)
        return False

    def statusReset_speech(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_mic,   Flag)
        self.statusSet(qBusy_dev_spk,   Flag)
        self.statusSet(qBusy_s_ctrl,    Flag)
        self.statusSet(qBusy_s_inp,     Flag)
        self.statusSet(qBusy_s_wav,     Flag)
        self.statusSet(qBusy_s_STT,     Flag)
        self.statusSet(qBusy_s_TTS,     Flag)
        self.statusSet(qBusy_s_TRA,     Flag)
        self.statusSet(qBusy_s_play,    Flag)
        self.statusSet(qRdy__s_force,   Flag)
        self.statusSet(qRdy__s_fproc,   Flag)
        self.statusSet(qRdy__s_sendkey, Flag)
        return True

    def statusReset_vision(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_cam,   Flag)
        self.statusSet(qBusy_dev_dsp,   Flag)
        self.statusSet(qBusy_v_ctrl,    Flag)
        self.statusSet(qBusy_v_inp,     Flag)
        self.statusSet(qBusy_v_QR,      Flag)
        self.statusSet(qBusy_v_jpg,     Flag)
        self.statusSet(qBusy_v_CV,      Flag)
        self.statusSet(qRdy__v_reader,  Flag)
        self.statusSet(qRdy__v_sendkey, Flag)
        return True

    def statusReset_desktop(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_scn,   Flag)
        self.statusSet(qBusy_d_ctrl,    Flag)
        self.statusSet(qBusy_d_inp,     Flag)
        self.statusSet(qBusy_d_QR,      Flag)
        self.statusSet(qBusy_d_rec,     Flag)
        self.statusSet(qBusy_d_play,    Flag)
        self.statusSet(qBusy_d_browser, Flag)
        self.statusSet(qBusy_d_upload,  Flag)
        self.statusSet(qRdy__d_reader,  Flag)
        self.statusSet(qRdy__d_sendkey, Flag)
        return True

    def statusCheck(self, file, ):
        if (os.path.exists(file)):
            return True
        else:
            return False

    def statusWait_false(self, file, falseWait=1, ):
        if (falseWait != 0):
            chktime = time.time()
            while (os.path.exists(file)) and ((time.time() - chktime) < falseWait):
                time.sleep(0.10)
        return self.statusCheck(file)

    def statusWait_true(self, file, trueWait=1, ):
        if (trueWait != 0):
            chktime = time.time()
            while (not os.path.exists(file)) and ((time.time() - chktime) < trueWait):
                time.sleep(0.10)
        return self.statusCheck(file)

    def statusWait_speech(self, idolSec=2, maxWait=15, ):
        busy_flag = True
        chktime1 = time.time()
        while (busy_flag == True) and ((time.time() - chktime1) < maxWait):
            busy_flag = False
            chktime2 = time.time()
            while ((time.time() - chktime2) < idolSec):
                if (self.statusCheck(qBusy_s_wav ) == True) \
                or (self.statusCheck(qBusy_s_STT ) == True) \
                or (self.statusCheck(qBusy_s_TTS ) == True) \
                or (self.statusCheck(qBusy_s_TRA ) == True) \
                or (self.statusCheck(qBusy_s_play) == True):
                    busy_flag = True
                    time.sleep(0.10)
                    break

    def tts(self, id, text, idolSec=2, maxWait=15, ):
        self.statusWait_speech(idolSec, maxWait, )

        if (text != ''):
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
            filename = qPath_s_TTS + stamp + '.' + str(id) + '.txt'

            return self.txtsWrite(filename, txts=[text], encoding='utf-8', exclusive=False, mode='w', )

        return False

    def speech(self, id='speech', speechs=[], lang='auto', idolSec=2, maxWait=15, ):
        self.statusWait_speech(idolSec, maxWait, )

        outLang = lang
        if (outLang == 'auto'):
            if   (qPLATFORM == 'windows'):
                #outLang = 'ja,winos,'
                outLang = 'ja,hoya,'
            elif (qPLATFORM == 'darwin'):
                outLang = 'ja,macos,'
            else:
                outLang = 'ja,free,'

        seq = 0
        for speech in speechs:
            text = outLang + str(speech['text'])
            seq+= 1
            id2  = id + '.' + '{:02}'.format(seq)
            self.tts(id2, text, 0, 0, )
            try:
                time.sleep(speech['wait'])
            except Exception as e:
                pass

        return True

class qBusy_status_txts_class(object):
    def __init__(self):
        self.check     = ''

        self.dev_cpu   = False
        self.dev_com   = False
        self.dev_mic   = False
        self.dev_spk   = False
        self.dev_cam   = False
        self.dev_dsp   = False
        self.dev_scn   = False
        self.s_ctrl    = False
        self.s_inp     = False
        self.s_wav     = False
        self.s_STT     = False
        self.s_TTS     = False
        self.s_TRA     = False
        self.s_play    = False
        self.s_force   = False
        self.s_sendkey = False
        self.v_ctrl    = False
        self.v_inp     = False
        self.v_QR      = False
        self.v_jpg     = False
        self.v_CV      = False
        self.v_reader  = False
        self.v_sendkey = False
        self.d_ctrl    = False
        self.d_inp     = False
        self.d_QR      = False
        self.d_rec     = False
        self.d_play    = False
        self.d_browser = False
        self.d_upload  = False
        self.d_reader  = False
        self.d_sendkey = False

    def statusCheck(self, file, ):
        if (os.path.exists(file)):
            return True
        else:
            return False

    def getAll(self):
        change = False

        if (self.check !='all'):
            change = True
        self.check = 'all'

        # ステータス取得
        check = self.statusCheck(qBusy_dev_cpu)
        if (check != self.dev_cpu):
            change = True
        self.dev_cpu = check
        check = self.statusCheck(qBusy_dev_com)
        if (check != self.dev_com):
            change = True
        self.dev_com = check
        check = self.statusCheck(qBusy_dev_mic)
        if (check != self.dev_mic):
            change = True
        self.dev_mic = check
        check = self.statusCheck(qBusy_dev_spk)
        if (check != self.dev_spk):
            change = True
        self.dev_spk = check
        check = self.statusCheck(qBusy_dev_cam)
        if (check != self.dev_cam):
            change = True
        self.dev_cam = check
        check = self.statusCheck(qBusy_dev_dsp)
        if (check != self.dev_dsp):
            change = True
        self.dev_dsp = check
        check = self.statusCheck(qBusy_dev_scn)
        if (check != self.dev_scn):
            change = True
        self.dev_scn = check

        check = self.statusCheck(qBusy_s_ctrl)
        if (check != self.s_ctrl):
            change = True
        self.s_ctrl = check
        check = self.statusCheck(qBusy_s_inp )
        if (check != self.s_inp):
            change = True
        self.s_inp = check
        check = self.statusCheck(qBusy_s_wav )
        if (check != self.s_wav):
            change = True
        self.s_wav = check
        check = self.statusCheck(qBusy_s_STT )
        if (check != self.s_STT):
            change = True
        self.s_STT = check
        check = self.statusCheck(qBusy_s_TTS )
        if (check != self.s_TTS):
            change = True
        self.s_TTS = check
        check = self.statusCheck(qBusy_s_TRA )
        if (check != self.s_TRA):
            change = True
        self.s_TRA = check
        check = self.statusCheck(qBusy_s_play)
        if (check != self.s_play):
            change = True
        self.s_play = check
        check = self.statusCheck(qRdy__s_force)
        if (check != self.s_force):
            change = True
        self.s_force = check
        check = self.statusCheck(qRdy__s_sendkey)
        if (check != self.s_sendkey):
            change = True
        self.s_sendkey = check

        check = self.statusCheck(qBusy_v_ctrl)
        if (check != self.v_ctrl):
            change = True
        self.v_ctrl = check
        check = self.statusCheck(qBusy_v_inp )
        if (check != self.v_inp):
            change = True
        self.v_inp = check
        check = self.statusCheck(qBusy_v_QR  )
        if (check != self.v_QR):
            change = True
        self.v_QR = check
        check = self.statusCheck(qBusy_v_jpg )
        if (check != self.v_jpg):
            change = True
        self.v_jpg = check
        check = self.statusCheck(qBusy_v_CV  )
        if (check != self.v_CV):
            change = True
        self.v_CV = check
        check = self.statusCheck(qRdy__v_reader)
        if (check != self.v_reader):
            change = True
        self.v_reader = check
        check = self.statusCheck(qRdy__v_sendkey)
        if (check != self.v_sendkey):
            change = True
        self.v_sendkey = check

        check = self.statusCheck(qBusy_d_ctrl)
        if (check != self.d_ctrl):
            change = True
        self.d_ctrl = check
        check = self.statusCheck(qBusy_d_inp )
        if (check != self.d_inp):
            change = True
        self.d_inp = check
        check = self.statusCheck(qBusy_d_QR  )
        if (check != self.d_QR):
            change = True
        self.d_QR = check
        check = self.statusCheck(qBusy_d_rec )
        if (check != self.d_rec):
            change = True
        self.d_rec = check
        check = self.statusCheck(qBusy_d_play)
        if (check != self.d_play):
            change = True
        self.d_play = check
        check = self.statusCheck(qBusy_d_browser)
        if (check != self.d_browser):
            change = True
        self.d_browser = check
        check = self.statusCheck(qBusy_d_upload )
        if (check != self.d_upload):
            change = True
        self.d_upload = check
        check = self.statusCheck(qRdy__d_reader)
        if (check != self.d_reader):
            change = True
        self.d_reader = check
        check = self.statusCheck(qRdy__d_sendkey)
        if (check != self.d_sendkey):
            change = True
        self.d_sendkey = check

        if (change != True):
            return False

        # 文字列生成
        txts=[]
        txts.append('[Device control]')
        if (self.dev_cpu == True):
            txts.append(' CPU    : slow!___')
        else:
            txts.append(' CPU    : ________')
        if (self.dev_com == True):
            txts.append(' Comm   : disable!')
        else:
            txts.append(' Comm   : ________')
        if (self.dev_mic == True):
            txts.append(' Mic    : disable!')
        else:
            txts.append(' Mic    : ________')
        if (self.dev_spk == True):
            txts.append(' Speaker: disable!')
        else:
            txts.append(' Speaker: ________')
        if (self.dev_cam == True):
            txts.append(' camera : disable!')
        else:
            txts.append(' camera : ________')
        if (self.dev_dsp == True):
            txts.append(' Display: disable!')
        else:
            txts.append(' Display: ________')
        if (self.dev_scn == True):
            txts.append(' Screen : disable!')
        else:
            txts.append(' Screen : ________')

        txts.append('')
        txts.append('[Speech status]')
        if (self.s_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.s_inp == True):
            txts.append(' Input  : ready___')
        else:
            txts.append(' Input  : ________')
        if (self.s_wav == True):
            txts.append(' Wave   : busy!___')
        else:
            txts.append(' Wave   : ________')
        if (self.s_STT == True):
            txts.append(' STT    : busy!___')
        else:
            txts.append(' STT    : ________')
        if (self.s_TTS == True):
            txts.append(' TTS    : busy!___')
        else:
            txts.append(' TTS    : ________')
        if (self.s_TRA == True):
            txts.append(' TRA    : busy!___')
        else:
            txts.append(' TRA    : ________')
        if (self.s_play == True):
            txts.append(' Play   : busy!___')
        else:
            txts.append(' Play   : ________')
        if (self.s_force == True):
            txts.append(' RIKI   : active__')
        else:
            txts.append(' RIKI   : ________')
        if (self.s_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        txts.append('[Vision status]')
        if (self.v_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.v_inp == True):
            txts.append(' Input  : active__')
        else:
            txts.append(' Input  : ________')
        if (self.v_QR == True):
            txts.append(' QR scan: active__')
        else:
            txts.append(' QR scan: ________')
        if (self.v_jpg == True):
            txts.append(' jpeg   : busy!___')
        else:
            txts.append(' jpeg   : ________')
        if (self.v_CV == True):
            txts.append(' CV     : busy!___')
        else:
            txts.append(' CV     : ________')
        if (self.v_reader == True):
            txts.append(' Reader : active__')
        else:
            txts.append(' Reader : ________')
        if (self.v_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        txts.append('[Desktop status]')
        if (self.d_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.d_inp == True):
            txts.append(' Capture: active__')
        else:
            txts.append(' Capture: ________')
        if (self.d_QR == True):
            txts.append(' QR scan: active__')
        else:
            txts.append(' QR scan: ________')
        if (self.d_rec == True):
            txts.append(' Rec    : rec!____')
        else:
            txts.append(' Rec    : ________')
        if (self.d_play == True):
            txts.append(' Play   : play!___')
        else:
            txts.append(' Play   : ________')
        if (self.d_browser == True):
            txts.append(' Browser: play!___')
        else:
            txts.append(' Browser: ________')
        if (self.d_upload == True):
            txts.append(' Upload : active__')
        else:
            txts.append(' Upload : ________')
        if (self.d_reader == True):
            txts.append(' Reader : active__')
        else:
            txts.append(' Reader : ________')
        if (self.d_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        return txts

    def getRecorder(self):
        change = False

        if (self.check !='recorder'):
            change = True
        self.check = 'recorder'

        # ステータス取得
        check = self.statusCheck(qBusy_s_inp )
        if (check != self.s_inp):
            change = True
        self.s_inp = check
        check = self.statusCheck(qBusy_d_rec )
        if (check != self.d_rec):
            change = True
        self.d_rec = check
 
        if (change != True):
            return False

        # 文字列生成
        txts=[]
        if (self.s_inp == True):
            txts.append(' Speech   : ready__')
        else:
            txts.append(' Speech   : _______')
        if (self.d_rec == True):
            txts.append(' Recorder : rec!___')
        else:
            txts.append(' Recorder : _______')

        return txts



class qFPS_class(object):
    def __init__(self):
        self.start     = cv2.getTickCount()
        self.count     = 0
        self.FPS       = 0
        self.lastcheck = time.time()
    def get(self):
        self.count += 1
        if (self.count >= 15) or ((time.time() - self.lastcheck) > 5):
            nowTick  = cv2.getTickCount()
            diffSec  = (nowTick - self.start) / cv2.getTickFrequency()
            self.FPS = 1 / (diffSec / self.count)
            self.start = cv2.getTickCount()
            self.count = 0
            self.lastcheck = time.time()
        return self.FPS



if (__name__ == '__main__'):

    qFunc = qFunc_class()
    qFunc.init()

    # テスト
    qBusy_status_txts = qBusy_status_txts_class()

    qFunc.kill('sox')

    qFunc.guideDisplay(display=True, panel='1', filename='_kernel_start_', txt='waiting...')
    time.sleep(3.00)
    qFunc.guideDisplay(display=False, )

    qFunc.notePad(txt=u'開始')
    #qFunc.sendKey(txt=u'日本語')
    #qFunc.sendKey(txt=u'abcdefg',lf=False)

    x,y = qFunc.getResolution('full')
    print('getResolution x,y = ', x, y, )

    qFunc.img2clip('cv2dnn\dog.jpg')

    qFunc.statusReset_speech(True)
    qFunc.statusReset_vision(True)
    qFunc.statusReset_desktop(True)

    qFunc.statusReset_speech(False)
    qFunc.statusReset_vision(False)
    qFunc.statusReset_desktop(False)

    txts = qBusy_status_txts.getAll()
    for txt in txts:
        print(txt)

    txts = qBusy_status_txts.getRecorder()
    for txt in txts:
        print(txt)

    qFunc.notePad(txt=u'終了')



