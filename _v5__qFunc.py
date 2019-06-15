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

import platform
qOS = platform.system().lower() #windows,darwin,linux

import ctypes
import array

import cv2



qPath_log      = 'temp/_log/'
qPath_work     = 'temp/_work/'
qPath_rec      = 'temp/_recorder/'

qPath_a_ctrl   = 'temp/a5_0control/'
qPath_a_inp    = 'temp/a5_1voice/'
qPath_a_wav    = 'temp/a5_2wav/'
qPath_a_jul    = 'temp/a5_3stt_julius/'
qPath_a_STT    = 'temp/a5_4stt_txt/'
qPath_a_TTS    = 'temp/a5_5tts_txt/'
qPath_a_TRA    = 'temp/a5_6tra_txt/'
qPath_a_play   = 'temp/a5_7play/'
qPath_v_ctrl   = 'temp/v5_0control/'
qPath_v_inp    = 'temp/v5_1vision/'
qPath_v_jpg    = 'temp/v5_2jpg/'
qPath_v_detect = 'temp/v5_3detect/'
qPath_v_cv     = 'temp/v5_5cv_txt/'
qPath_v_photo  = 'temp/v5_7photo/'

qBusy_dev_cpu  = qPath_work + 'busy_dev_cpu.txt'
qBusy_dev_com  = qPath_work + 'busy_dev_commnication.txt'
qBusy_dev_mic  = qPath_work + 'busy_dev_microphone.txt'
qBusy_dev_spk  = qPath_work + 'busy_dev_speaker.txt'
qBusy_dev_cam  = qPath_work + 'busy_dev_camera.txt'
qBusy_dev_dsp  = qPath_work + 'busy_dev_display.txt'
qBusy_a_ctrl   = qPath_work + 'busy_0control.txt'
qBusy_a_inp    = qPath_work + 'busy_1audio.txt'
qBusy_a_wav    = qPath_work + 'busy_2wav.txt'
qBusy_a_STT    = qPath_work + 'busy_4stt_txt.txt'
qBusy_a_TTS    = qPath_work + 'busy_5tts_txt.txt'
qBusy_a_TRA    = qPath_work + 'busy_6tra_txt.txt'
qBusy_a_play   = qPath_work + 'busy_7play.txt'
qBusy_v_ctrl   = qPath_work + 'busy_v_0control.txt'
qBusy_v_inp    = qPath_work + 'busy_v_1video.txt'
qBusy_v_jpg    = qPath_work + 'busy_v_2jpg.txt'
qBusy_v_CV     = qPath_work + 'busy_v_5cv.txt'



class qFunc_class:

    def __init__(self, ):
        nowTime = datetime.datetime.now()
        self.qLogFlie = qPath_log + nowTime.strftime('%Y%m%d-%H%M%S') + '.log'
        self.qLogDisp = True
        self.qLogOutf = True
        
    def __del__(self, ):
        pass
                
    def init(self, ):
        self.makeDirs('temp/_log/',   False)
        self.makeDirs('temp/_cache/', False)

        self.makeDirs(qPath_log,      False)
        self.makeDirs(qPath_work,     False)
        self.makeDirs(qPath_rec,      False)

        self.makeDirs(qPath_a_ctrl,   False)
        self.makeDirs(qPath_a_inp,    False)
        self.makeDirs(qPath_a_wav,    False)
        self.makeDirs(qPath_a_jul,    False)
        self.makeDirs(qPath_a_STT,    False)
        self.makeDirs(qPath_a_TTS,    False)
        self.makeDirs(qPath_a_TRA,    False)
        self.makeDirs(qPath_a_play,   False)
        self.makeDirs(qPath_v_ctrl,   False)
        self.makeDirs(qPath_v_inp,    False)
        self.makeDirs(qPath_v_jpg,    False)
        self.makeDirs(qPath_v_detect, False)
        self.makeDirs(qPath_v_cv,     False)
        self.makeDirs(qPath_v_photo,  False)

        return True

    def getValue(self, field):
        if (field == 'qOS'           ): return qOS

        if (field == 'qPath_log'     ): return qPath_log
        if (field == 'qPath_work'    ): return qPath_work
        if (field == 'qPath_rec'     ): return qPath_rec

        if (field == 'qPath_a_ctrl'  ): return qPath_a_ctrl
        if (field == 'qPath_a_inp'   ): return qPath_a_inp
        if (field == 'qPath_a_wav'   ): return qPath_a_wav
        if (field == 'qPath_a_jul'   ): return qPath_a_jul
        if (field == 'qPath_a_STT'   ): return qPath_a_STT
        if (field == 'qPath_a_TTS'   ): return qPath_a_TTS
        if (field == 'qPath_a_TRA'   ): return qPath_a_TRA
        if (field == 'qPath_a_play'  ): return qPath_a_play
        if (field == 'qPath_v_ctrl'  ): return qPath_v_ctrl
        if (field == 'qPath_v_inp'   ): return qPath_v_inp
        if (field == 'qPath_v_jpg'   ): return qPath_v_jpg
        if (field == 'qPath_v_detect'): return qPath_v_detect
        if (field == 'qPath_v_cv'    ): return qPath_v_cv
        if (field == 'qPath_v_photo' ): return qPath_v_photo

        if (field == 'qBusy_dev_cpu' ): return qBusy_dev_cpu
        if (field == 'qBusy_dev_com' ): return qBusy_dev_com
        if (field == 'qBusy_dev_mic' ): return qBusy_dev_mic
        if (field == 'qBusy_dev_spk' ): return qBusy_dev_spk
        if (field == 'qBusy_dev_cam' ): return qBusy_dev_cam
        if (field == 'qBusy_dev_dsp' ): return qBusy_dev_dsp
        if (field == 'qBusy_a_ctrl'  ): return qBusy_a_ctrl
        if (field == 'qBusy_a_inp'   ): return qBusy_a_inp
        if (field == 'qBusy_a_wav'   ): return qBusy_a_wav
        if (field == 'qBusy_a_STT'   ): return qBusy_a_STT
        if (field == 'qBusy_a_TTS'   ): return qBusy_a_TTS
        if (field == 'qBusy_a_TRA'   ): return qBusy_a_TRA
        if (field == 'qBusy_a_play'  ): return qBusy_a_play
        if (field == 'qBusy_v_ctrl'  ): return qBusy_v_ctrl
        if (field == 'qBusy_v_inp'   ): return qBusy_v_inp
        if (field == 'qBusy_v_jpg'   ): return qBusy_v_jpg
        if (field == 'qBusy_v_CV'    ): return qBusy_v_CV

        print('check program !' + field)
        return None

    def logFileSet(self, file, display=True, outfile=True, ):
        self.qLogFlie = file
        self.qLogDisp = display
        self.qLogOutf = outfile
        return True

    def logOutput(self, text='', display='auto', outfile='auto', ):
        if (display != 'auto'):
            disp = display
        else:
            disp = self.qLogDisp
        if (outfile != 'auto'):
            outf = outfile
        else:
            outf = self.qLogOutf
        try:
            if (disp == True) or (disp == 'yes'):
                print(str(text))
            if (outf == True) or (outf == 'yes'):
                w = codecs.open(qLogFlie, 'a', 'utf-8')
                w.write(str(text) + '\n')
                w.close()
                w = None
        except:
            pass
        return True

    def makeDirs(self, ppath, remove=False, ):
        try:
            if (len(ppath) > 0):
                path=ppath.replace('\\', '/')
                if (path[-1:] != '/'):
                    path += '/'
                if (not os.path.isdir(path[:-1])):
                    os.makedirs(path[:-1])
                else:
                    if (remove == True):
                        files = glob.glob(path + '*')
                        for f in files:
                            try:
                                os.remove(f)
                            except:
                                pass
        except:
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
            except:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-f', name, ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except:
                pass
        return False

    def remove(self, filename, maxWait=0, ):
        if (not os.path.exists(filename)):
            return True
        else:
            if (maxWait == 0):
                try:
                    os.remove(filename)            
                    return True
                except:
                    return False
            else:
                chktime = time.time()
                while (os.path.exists(filename)) and ((time.time() - chktime) <= maxWait):
                    try:
                        os.remove(filename)            
                        return True
                    except:
                        pass
                    time.sleep(0.10)

                if (not os.path.exists(filename)):
                    return True
                else:
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
            except:
                w = None
                return False
        else:
            res = self.remove(filename, maxWait=1, )
            if (res == False):
                return False
            else:
                f2 = filename[:-4] + '.tmp.txt'
                res = self.remove(f2, maxWait=1, )
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
                    except:
                        w = None
                        return False

    def txtsRead(self, filename, encoding='utf-8', exclusive=False, ):
        if (exclusive == False):
            try:
                txts = []
                txt  = ''
                r = codecs.open(filename, 'r', encoding)
                for t in r:
                    t = t.replace('\n', '')
                    t = t.replace('\r', '')
                    txt  = (txt + ' ' + str(t)).strip()
                    txts.append(t)
                r.close
                r = None
                return txts, txt
            except:
                r = None
                return False, ''
        else:
            f2 = filename[:-4] + '.wrk.txt'
            res = self.remove(f2, maxWait=1, )
            if (res == False):
                return False
            else:
                try:
                    os.rename(filename, f2)
                    txts = []
                    txt  = ''
                    r = codecs.open(f2, 'r', encoding)
                    for t in r:
                        t = t.replace('\n', '')
                        t = t.replace('\r', '')
                        txt = (txt + ' ' + str(t)).strip()
                        txts.append(t)
                    r.close
                    r = None
                    self.remove(f2, maxWait=1, )
                    return txts, txt
                except:
                    r = None
                    return False, ''

    def notePad(self, txt='', cr=False, lf=True, ):
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
            #except:
            #    return False

    def enum_child_windows_proc(self, handle, list):
        list.append(handle)
        return 1

    def guide(self, filename=None, sync=True):
        if (self.busyCheck(qBusy_dev_spk, 0) == 'busy'):
            #self.logOutput('spk_busy!_:' + filename, )
            return False

        playfile = filename
        if (filename == '_up'):
            playfile = '_sounds/_sound_up.mp3'
        if (filename == '_ready'):
            playfile = '_sounds/_sound_ready.mp3'
        if (filename == '_accept'):
            playfile = '_sounds/_sound_accept.mp3'
        if (filename == '_ok'):
            playfile = '_sounds/_sound_ok.mp3'
        if (filename == '_ng'):
            playfile = '_sounds/_sound_ng.mp3'
        if (filename == '_down'):
            playfile = '_sounds/_sound_down.mp3'
        if (filename == '_shutter'):
            playfile = '_sounds/_sound_shutter.mp3'

        if (os.path.exists(playfile)):

            sox=subprocess.Popen(['sox', '-q', playfile, '-d', ], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            if (sync == True):
                sox.wait()
                sox.terminate()
                sox = None

            return True

        return False

    def getResolution(self, reso='full', ):
        if   (reso=='full'): 
            if (qOS != 'darwin'):
                return 1920,1080  # win,other
            else:
                return 2560,1600  # mac
        if   (reso=='full+'):
            if (qOS != 'darwin'):
                #return 1920+40,1080+40
                return 1280+40,720+40
            else:
                return 2560+40,1600+40
        elif (reso=='half'):
            if (qOS != 'darwin'):
                return 960,540
            else:
                return 1280,800

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

    def busySet(self, file, Flag=True):
        if (Flag == True):
            chktime = time.time()
            while (not os.path.exists(file)) and ((time.time() - chktime) < 1):
                try:
                    w = open(file, 'w')
                    w.write('BUSY')
                    w.close()
                    w = None
                    return True
                except:
                    w = None
                time.sleep(0.10)
        else:
            chktime = time.time()
            while (os.path.exists(file)) and ((time.time() - chktime) < 1):
                try:
                    os.remove(file)
                    return True
                except:
                    pass
                time.sleep(0.10)
        return False

    def busyReset_a(self, Flag=False):
        self.busySet(qBusy_dev_cpu, Flag)
        self.busySet(qBusy_dev_com, Flag)
        self.busySet(qBusy_dev_mic, Flag)
        self.busySet(qBusy_dev_spk, Flag)
        self.busySet(qBusy_a_ctrl,  Flag)
        self.busySet(qBusy_a_inp,   Flag)
        self.busySet(qBusy_a_wav,   Flag)
        self.busySet(qBusy_a_STT,   Flag)
        self.busySet(qBusy_a_TTS,   Flag)
        self.busySet(qBusy_a_TRA,   Flag)
        self.busySet(qBusy_a_play,  Flag)
        return True

    def busyReset_v(self, Flag=False):
        self.busySet(qBusy_dev_cpu, Flag)
        self.busySet(qBusy_dev_com, Flag)
        self.busySet(qBusy_dev_cam, Flag)
        self.busySet(qBusy_dev_dsp, Flag)
        self.busySet(qBusy_v_ctrl,  Flag)
        self.busySet(qBusy_v_inp,   Flag)
        self.busySet(qBusy_v_jpg,   Flag)
        self.busySet(qBusy_v_CV,    Flag)
        return True

    def busyCheck(self, file, maxWait=0, ):
        if (maxWait != 0):
            chktime = time.time()
            while (os.path.exists(file)) and ((time.time() - chktime) < maxWait):
                time.sleep(0.10)
        if (os.path.exists(file)):
            return 'busy'
        else:
            return 'none'

    def busyWait(self, idolSec=2, maxWait=15, ):
        busy_flag = True
        chktime1 = time.time()
        while (busy_flag == True) and ((time.time() - chktime1) < maxWait):
            busy_flag = False
            chktime2 = time.time()
            while ((time.time() - chktime2) < idolSec):
                if (self.busyCheck(qBusy_a_wav , 0) == 'busy') \
                or (self.busyCheck(qBusy_a_STT , 0) == 'busy') \
                or (self.busyCheck(qBusy_a_TTS , 0) == 'busy') \
                or (self.busyCheck(qBusy_a_TRA , 0) == 'busy') \
                or (self.busyCheck(qBusy_a_play, 0) == 'busy'):
                    busy_flag = True
                    time.sleep(0.10)
                    break

    def tts(self, id, text, idolSec=2, maxWait=15, ):
        self.busyWait(idolSec, maxWait, )

        if (text != ''):
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d-%H%M%S')
            filename = qPath_a_TTS + stamp + '.' + str(id) + '.txt'

            return self.txtsWrite(filename, txts=[text], encoding='utf-8', exclusive=False, mode='w', )

        return False

    def speech(self, id='speech', speechs=[], lang='auto', idolSec=2, maxWait=15, ):
        self.busyWait(idolSec, maxWait, )

        outLang = lang
        if (outLang == 'auto'):
            if   (qOS == 'windows'):
                #outLang = 'ja,winos,'
                outLang = 'ja,hoya,'
            elif (qOS == 'darwin'):
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
            except:
                pass

        return True

class qBusy_status_txts_class(object):
    def __init__(self):
        self.dev_cpu = 'none'
        self.dev_mic = 'none'
        self.dev_spk = 'none'
        self.dev_cam = 'none'
        self.dev_dsp = 'none'
        self.a_ctrl  = 'none'
        self.a_inp   = 'none'
        self.a_wav   = 'none'
        self.a_STT   = 'none'
        self.a_TTS   = 'none'
        self.a_TRA   = 'none'
        self.a_play  = 'none'
        self.v_ctrl  = 'none'
        self.v_inp   = 'none'
        self.v_jpg   = 'none'
        self.v_CV    = 'none'

    def busyCheck(self, file, maxWait=0, ):
        if (maxWait != 0):
            chktime = time.time()
            while (os.path.exists(file)) and ((time.time() - chktime) < maxWait):
                time.sleep(0.10)
        if (os.path.exists(file)):
            return 'busy'
        else:
            return 'none'

    def get(self):
        change = False

        # ステータス取得
        check = self.busyCheck(qBusy_dev_cpu, 0)
        if (check != self.dev_cpu):
            self.dev_cpu = check
            change = True
        check = self.busyCheck(qBusy_dev_mic, 0)
        if (check != self.dev_mic):
            self.dev_mic = check
            change = True
        check = self.busyCheck(qBusy_dev_spk, 0)
        if (check != self.dev_spk):
            self.dev_spk = check
            change = True
        check = self.busyCheck(qBusy_dev_cam, 0)
        if (check != self.dev_cam):
            self.dev_cam = check
            change = True
        check = self.busyCheck(qBusy_dev_dsp, 0)
        if (check != self.dev_dsp):
            self.dev_dsp = check
            change = True

        check = self.busyCheck(qBusy_a_ctrl, 0)
        if (check != self.a_ctrl):
            self.a_ctrl = check
            change = True
        check = self.busyCheck(qBusy_a_inp, 0)
        if (check != self.a_inp):
            self.a_inp = check
            change = True
        check = self.busyCheck(qBusy_a_wav, 0)
        if (check != self.a_wav):
            self.a_wav = check
            change = True
        check = self.busyCheck(qBusy_a_STT, 0)
        if (check != self.a_STT):
            self.a_STT = check
            change = True
        check = self.busyCheck(qBusy_a_TTS, 0)
        if (check != self.a_TTS):
            self.a_TTS = check
            change = True
        check = self.busyCheck(qBusy_a_TRA, 0)
        if (check != self.a_TRA):
            self.a_TRA = check
            change = True
        check = self.busyCheck(qBusy_a_play, 0)
        if (check != self.a_play):
            self.a_play = check
            change = True

        check = self.busyCheck(qBusy_v_ctrl, 0)
        if (check != self.v_ctrl):
            self.v_ctrl = check
            change = True
        check = self.busyCheck(qBusy_v_inp, 0)
        if (check != self.v_inp):
            self.v_inp = check
            change = True
        check = self.busyCheck(qBusy_v_jpg, 0)
        if (check != self.v_jpg):
            self.v_jpg = check
            change = True
        check = self.busyCheck(qBusy_v_CV, 0)
        if (check != self.v_CV):
            self.v_CV = check
            change = True
 
        if (change != True):
            return False

        # 文字列生成
        txts=[]
        txts.append('[Device control]')
        if (self.dev_cpu == 'busy'):
            txts.append(' CPU    : slow!__')
        else:
            txts.append(' CPU    : _______')
        if (self.dev_mic == 'busy'):
            txts.append(' Mic    : disable')
        else:
            txts.append(' Mic    : _______')
        if (self.dev_spk == 'busy'):
            txts.append(' Speaker: disable')
        else:
            txts.append(' Speaker: _______')
        if (self.dev_cam == 'busy'):
            txts.append(' Camera : disable')
        else:
            txts.append(' Camera : _______')
        if (self.dev_dsp == 'busy'):
            txts.append(' Display: disable')
        else:
            txts.append(' Display: _______')

        txts.append('')
        txts.append('[Speech status]')
        if (self.a_ctrl == 'busy'):
            txts.append(' Ctrl   : busy!__')
        else:
            txts.append(' Ctrl   : _______')
        if (self.a_inp == 'busy'):
            txts.append(' Input  : ready__')
        else:
            txts.append(' Input  : _______')
        if (self.a_wav == 'busy'):
            txts.append(' Wave   : busy!__')
        else:
            txts.append(' Wave   : _______')
        if (self.a_STT == 'busy'):
            txts.append(' STT    : busy!__')
        else:
            txts.append(' STT    : _______')
        if (self.a_TTS == 'busy'):
            txts.append(' TTS    : busy!__')
        else:
            txts.append(' TTS    : _______')
        if (self.a_TRA == 'busy'):
            txts.append(' TRA    : busy!__')
        else:
            txts.append(' TRA    : _______')

        if (self.a_TRA == 'busy'):
            txts.append(' Play   : busy!__')
        else:
            txts.append(' Play   : _______')

        txts.append('')
        txts.append('[Vision status]')
        if (self.v_ctrl == 'busy'):
            txts.append(' Ctrl   : busy!__')
        else:
            txts.append(' Ctrl   : _______')
        if (self.v_inp == 'busy'):
            txts.append(' Input  : ready__')
        else:
            txts.append(' Input  : _______')
        if (self.v_jpg == 'busy'):
            txts.append(' jpeg   : busy!__')
        else:
            txts.append(' jpeg   : _______')
        if (self.v_CV == 'busy'):
            txts.append(' CV     : busy!__')
        else:
            txts.append(' CV     : _______')

        txts.append('')
        return txts



class qFPS_class(object):
    def __init__(self):
        self.start = cv2.getTickCount()
        self.count = 0
        self.FPS   = 0
    def get(self):
        self.count += 1
        if (self.count >= 30):
            nowTick  = cv2.getTickCount()
            diffSec  = (nowTick - self.start) / cv2.getTickFrequency()
            self.FPS = 1 / (diffSec / self.count)
            self.start = cv2.getTickCount()
            self.count = 0
        return self.FPS



if (__name__ == '__main__'):

    #import  _v5__qFunc
    #qFunc = _v5__qFunc.qFunc_class()
    qFunc = qFunc_class()
    qFunc.init()

    nowTime = datetime.datetime.now()
    logfile = qPath_log + nowTime.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=logfile, display=True, outfile=True, )
    qFunc.logOutput(logfile, )

    qFunc.kill('sox')

    qFunc.notePad(txt=u'開始')

    qFunc.busyReset_a(True)
    qFunc.busyReset_v(True)

    qFunc.busyReset_a(False)
    qFunc.busyReset_v(False)

    qFunc.logOutput('')
    qFunc.logOutput( qBusy_dev_cpu + ':' + qFunc.busyCheck(qBusy_dev_cpu, 1), )
    qFunc.logOutput( qBusy_dev_com + ':' + qFunc.busyCheck(qBusy_dev_com, 1), )
    qFunc.logOutput( qBusy_dev_mic + ':' + qFunc.busyCheck(qBusy_dev_mic, 1), )
    qFunc.logOutput( qBusy_dev_spk + ':' + qFunc.busyCheck(qBusy_dev_spk, 1), )
    qFunc.logOutput( qBusy_dev_cam + ':' + qFunc.busyCheck(qBusy_dev_cam, 1), )
    qFunc.logOutput( qBusy_dev_dsp + ':' + qFunc.busyCheck(qBusy_dev_dsp, 1), )
    qFunc.logOutput( qBusy_a_ctrl + ' :' + qFunc.busyCheck(qBusy_a_ctrl,  1), )
    qFunc.logOutput( qBusy_a_inp + '  :' + qFunc.busyCheck(qBusy_a_inp,   1), )
    qFunc.logOutput( qBusy_a_wav + '  :' + qFunc.busyCheck(qBusy_a_wav,   1), )
    qFunc.logOutput( qBusy_a_STT + '  :' + qFunc.busyCheck(qBusy_a_STT,   1), )
    qFunc.logOutput( qBusy_a_TTS + '  :' + qFunc.busyCheck(qBusy_a_TTS,   1), )
    qFunc.logOutput( qBusy_a_TRA + '  :' + qFunc.busyCheck(qBusy_a_TRA,   1), )
    qFunc.logOutput( qBusy_a_play + ' :' + qFunc.busyCheck(qBusy_a_play,  1), )
    qFunc.logOutput( qBusy_v_ctrl + ' :' + qFunc.busyCheck(qBusy_v_ctrl,  1), )
    qFunc.logOutput( qBusy_v_inp + '  :' + qFunc.busyCheck(qBusy_v_inp,   1), )
    qFunc.logOutput( qBusy_v_jpg + '  :' + qFunc.busyCheck(qBusy_v_jpg,   1), )
    qFunc.logOutput( qBusy_v_CV + '   :' + qFunc.busyCheck(qBusy_v_CV,   1), )

    qFunc.notePad(txt=u'終了')


