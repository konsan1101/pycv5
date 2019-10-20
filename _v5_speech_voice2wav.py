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

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



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
qRdy__s_sendkey = qFunc.getValue('qRdy__s_sendkey')
qRdy__v_reader  = qFunc.getValue('qRdy__v_reader' )
qRdy__v_sendkey = qFunc.getValue('qRdy__v_sendkey')
qRdy__d_reader  = qFunc.getValue('qRdy__d_reader' )
qRdy__d_sendkey = qFunc.getValue('qRdy__d_sendkey')

# julius 音声認識
import speech_api_julius



audio_start  = 0
audio_beat   = 0
audio_busy   = False
audio_last   = 0
audio_bakSEQ = 0
audio_bakLast= ''
audio_bakWav = ''

adinsvr_run  = False
adinsvr_sbp  = None
adinexe_run  = False
adinexe_sbp  = None
adingui_run  = False
adingui_sbp  = None
bakSox_run   = False
bakSox_sbp   = None

def proc_audio(cn_r, cn_s, ):
    global audio_start
    global audio_beat
    global audio_busy
    global audio_last
    global audio_bakSEQ
    global audio_bakLast
    global audio_bakWav

    global adinsvr_run
    global adinsvr_sbp
    global adinexe_run
    global adinexe_sbp
    global adingui_run
    global adingui_sbp
    global bakSox_run
    global bakSox_sbp

    global v2w_wave_seq

    qFunc.logOutput('audio_inp_:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    micLevel = cn_r.get()
    cn_r.task_done()

    #qFunc.logOutput('audio_inp_:runMode =' + str(runMode ))
    #qFunc.logOutput('audio_inp_:micDev  =' + str(micDev  ))
    #qFunc.logOutput('audio_inp_:micType =' + str(micType ))
    #qFunc.logOutput('audio_inp_:micGuide=' + str(micGuide))
    #qFunc.logOutput('audio_inp_:micLevel=' + str(micLevel))

    qFunc.logOutput('audio_inp_:start')
    audio_start=time.time()

    audio_rewind   = '555'
    audio_headmg   = '333'
    audio_tailmg   = '444'
    vadLevel        = '1'
    if (micLevel == '1'):
        vadLevel    = '3'



    if (micDev.isdigit()):
        if (bakSox_run == True):
            bakSox_run = False
            if (not bakSox_sbp is None):
                try:
                    stdout, stderr = bakSox_sbp.communicate()
                except:
                    pass
                bakSox_sbp.wait(2)
                bakSox_sbp.terminate()
                bakSox_sbp = None

        if (audio_bakLast != '' and audio_bakWav != ''):
            if (os.path.exists(audio_bakWav)):
                qFunc.logOutput('audio_inp_:recovery ' + audio_bakLast)

                #qFunc.copy(audio_bakWav, audio_bakLast)
                sox = subprocess.Popen(['sox', '-q', audio_bakWav, audio_bakLast, ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

                try:
                    time.sleep(0.20)
                    os.remove(audio_bakWav)
                except:
                    pass

        audio_bakLast = ''
        audio_bakWav  = ''

        audio_bakSEQ  = 9999 #dummy



    while (True):
        audio_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qFunc.logOutput('audio_inp_:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qFunc.logOutput('audio_inp_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                audio_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                audio_busy = True
                audio_last = time.time()

                if (micDev.isdigit()) and (adinsvr_run == False):
                    adinsvr_run = True
                    #now=datetime.datetime.now()
                    #filename=qPath_s_inp + now.strftime('%H%M%S') +'.julius'
                    #adinsvr_sbp = subprocess.Popen(['adintool', '-in', 'adinnet', '-out', 'file', '-filename', filename, '-startid', '5001',] , \
                    #              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    #              #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                    #time.sleep(0.50)
                    if (micGuide != 'off'):
                        qFunc.guide('_up')

                sw = 'off'
                if (micDev.isdigit()):
                    if (micType == 'usb'):
                        sw = 'on'
                    else:
                        if  (qFunc.statusWait_false(qBusy_s_ctrl, 1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_STT,  1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_TTS,  1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_play, 1) == False):
                            sw = 'on'

                if (sw == 'on'):
                    qFunc.statusSet(qBusy_s_inp, True)

                    if (v2w_wave_seq != audio_bakSEQ):
                        audio_bakSEQ = v2w_wave_seq

                    if (adinexe_run == False):
                        adinexe_run = True

                        if (bakSox_run == True):
                            bakSox_run = False
                            if (not bakSox_sbp is None):
                                bakSox_sbp.terminate()
                                bakSox_sbp = None
                            audio_bakLast = ''
                            audio_bakWav  = ''

                        if (micGuide == 'on' or micGuide == 'sound'):
                            qFunc.guide('_ready')

                        if (bakSox_run == False):
                            bakSox_run = True
                            now=datetime.datetime.now()
                            audio_bakLast = qPath_s_inp + now.strftime('%H%M%S') +'.julius.5000.wav'
                            audio_bakWav = qPath_work + 'audio_backup.wav'
                            bakSox_sbp = subprocess.Popen(['sox', '-q', '-d', '-r', '16000', '-b', '16', '-c', '1', \
                                            audio_bakWav, 'trim', '0', '30', ], \
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #qFunc.logOutput('audio_inp_:backup ' + audio_bakLast)

                        #adinexe_sbp = subprocess.Popen(['adintool', '-in', 'mic', \
                        #    '-rewind', audio_rewind, '-headmargin', audio_headmg, '-tailmargin', audio_tailmg, \
                        #    '-fvad', vadLevel, '-lv', micLevel, \
                        #    '-out', 'adinnet', '-server', 'localhost', '-port', '5530',] , \
                        #    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        #    #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
                        now=datetime.datetime.now()
                        filename=qPath_s_inp + now.strftime('%H%M%S') +'.julius'
                        adinexe_sbp = subprocess.Popen(['adintool', '-in', 'mic', \
                            '-rewind', audio_rewind, '-headmargin', audio_headmg, '-tailmargin', audio_tailmg, \
                            '-fvad', vadLevel, '-lv', micLevel, \
                            '-out', 'file', '-filename', filename, '-startid', '5001', ] , \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )

                    if (os.name == 'nt'):
                      if (adingui_run == False) and (micGuide == 'on' or micGuide == 'display'):
                        adingui_run = True
                        adingui_sbp = subprocess.Popen(['adintool-gui', '-in', 'mic', \
                            '-rewind', audio_rewind, '-headmargin', audio_headmg, '-tailmargin', audio_tailmg, \
                            '-lv', micLevel,] , \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            #stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )

                sw = 'on'
                if (micType == 'bluetooth'):
                    if (qFunc.statusCheck(qBusy_s_ctrl) == True) \
                    or (qFunc.statusCheck(qBusy_s_STT ) == True) \
                    or (qFunc.statusCheck(qBusy_s_TTS ) == True) \
                    or (qFunc.statusCheck(qBusy_s_play) == True):
                        sw = 'off'
                if (adinexe_run == True):
                    files = glob.glob(qPath_s_inp + '*')
                    if (len(files) > 0):
                        chktime = time.time()
                        while (len(files) > 0) and ((time.time() - chktime) < 5):
                            time.sleep(0.20)
                            files = glob.glob(qPath_s_inp + '*')
                        if (len(files) == 0):
                            sw = 'accept'

                if (sw == 'off') or (sw == 'accept'):
                    if (bakSox_run == True):
                        bakSox_run = False
                        if (not bakSox_sbp is None):
                            bakSox_sbp.terminate()
                            bakSox_sbp = None
                        audio_bakLast = ''
                        audio_bakWav  = ''

                    if (adingui_run == True):
                        adingui_run = False
                        if (not adingui_sbp is None):
                            adingui_sbp.terminate()
                            adingui_sbp = None

                    if (adinexe_run == True):
                        adinexe_run = False
                        if (not adinexe_sbp is None):
                            adinexe_sbp.terminate()
                            adinexe_sbp = None

                    qFunc.statusSet(qBusy_s_inp, False)

                    if (sw == 'accept'):
                        if (micGuide == 'on' or micGuide == 'sound'):
                            qFunc.guide('_accept')
                            time.sleep(1.00)

                cn_s.put(['OK', ''])

        audio_busy = False

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qFunc.logOutput('audio_inp_:terminate')

    qFunc.statusSet(qBusy_s_inp, False)

    if (adingui_run == True):
        adingui_run = False
        if (not adingui_sbp is None):
            adingui_sbp.terminate()
            adingui_sbp = None
    if (adinexe_run == True):
        adinexe_run = False
        if (not adinexe_sbp is None):
            adinexe_sbp.terminate()
            adinexe_sbp = None
    if (adinsvr_run == True):
        adinsvr_run = False
        if (not adinsvr_sbp is None):
            adinsvr_sbp.terminate()
            adinsvr_sbp = None

    qFunc.kill('adintool-gui')
    qFunc.kill('adintool')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qFunc.logOutput('audio_inp_:end')



def v2w_wave_sub(micDev, seq4, fileId, file, f2, f2size, bytebase, minSize, maxSize, ):
    global julius_API
    global julius_MAX
    global julius_INI
    global julius_SEQ

    if (True):

        if (f2size >= int(minSize) and f2size <= int(maxSize+2000)):

                now=datetime.datetime.now()
                stamp=now.strftime('%Y%m%d.%H%M%S')

                if (micDev.isdigit()):
                     sec=int((f2size-44)/2/16000)
                else:
                     sec=int(bytebase/2/16000)
                hh=int(sec/3600)
                mm=int((sec-hh*3600)/60)
                ss=int(sec-hh*3600-mm*60)
                tm='{:02}{:02}{:02}'.format(hh,mm,ss)

                f3=qPath_s_wav + stamp + '.' + fileId + '(000).' + tm + '.wav'
                qFunc.copy(f2, f3)

                fwav=f3.replace(qPath_s_wav, '')
                fwav=qPath_s_jul + fwav
                qFunc.copy(f2, fwav)

                if (True):
                        julius_SEQ += 1
                        if (julius_SEQ > (julius_MAX * 20)):
                            julius_SEQ = 1
                        j = ((julius_SEQ -1) % julius_MAX) + 1
                        julius_API[j].put(['filename', fwav])
                        resdata = julius_API[j].checkGet()
                        #print(resdata[0], resdata[1], )

                        julius_API[j].stop()
                        del julius_API[j]

                        julius_INI += 1
                        if (julius_INI > (julius_MAX * 20)):
                            julius_INI = 1
                        j = ((julius_INI - 1) % julius_MAX) + 1
                        jx = '{:02}'.format(j)
                        julius_API[j] = speech_api_julius.proc_julius('julius', jx, )
                        julius_API[j].start()

                if (micDev.isdigit()):
                        try:
                            frec=f3.replace(qPath_s_wav, '')
                            frec=qPath_rec + frec[:-4] + '.mp3'
                            sox = subprocess.Popen(['sox', '-q', f2, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None
                        except:
                            pass

        if (f2size > int(maxSize+2000)):
            nn=1
            while (nn != 0):

                sepsec=int(maxSize/16000/2 - 1)

                now=datetime.datetime.now()
                stamp=now.strftime('%Y%m%d.%H%M%S')

                f4 = f2[:-4] + '.trim.wav'
                sox = subprocess.Popen(['sox', '-q', f2, '-r', '16000', '-b', '16', '-c', '1', f4, 'trim', str((nn-1)*sepsec), str(sepsec+1), ], \
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

                f4size = 0
                try:
                    rb = open(f4, 'rb')
                    f4size = sys.getsizeof(rb.read())
                    rb.close
                    rb = None
                except:
                    pass

                if (f4size < int(minSize)):
                    nn = 0
                    os.remove(f4)
                else:

                    if (micDev.isdigit()):
                        sec=int((f4size-44)/2/16000)
                    else:
                        sec=int(bytebase/2/16000) + (nn-1)*15
                    hh=int(sec/3600)
                    mm=int((sec-hh*3600)/60)
                    ss=int(sec-hh*3600-mm*60)
                    tm='{:02}{:02}{:02}'.format(hh,mm,ss)

                    f5=qPath_s_wav + stamp + '.' + fileId + '(' + '{:03}'.format(nn) + ').' + tm + '.wav'
                    qFunc.copy(f4, f5)

                    fwav=f5.replace(qPath_s_wav, '')
                    fwav=qPath_s_jul + fwav
                    qFunc.copy(f4, fwav)

                    if (True):
                        julius_SEQ += 1
                        if (julius_SEQ > (julius_MAX * 20)):
                            julius_SEQ = 1
                        j = ((julius_SEQ -1) % julius_MAX) + 1
                        julius_API[j].put(['filename', fwav])
                        resdata = julius_API[j].checkGet()
                        #print(resdata[0], resdata[1], )

                        julius_API[j].stop()
                        del julius_API[j]

                        julius_INI += 1
                        if (julius_INI > (julius_MAX * 20)):
                            julius_INI = 1
                        j = ((julius_INI - 1) % julius_MAX) + 1
                        jx = '{:02}'.format(j)
                        julius_API[j] = speech_api_julius.proc_julius('julius', jx, )
                        julius_API[j].start()

                    if (micDev.isdigit()):
                        try:
                            frec=f3.replace(qPath_s_wav, '')
                            frec=qPath_rec + frec[:-4] + '.mp3'
                            sox = subprocess.Popen(['sox', '-q', f4, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None
                        except:
                            pass

                    nn += 1



v2w_wave_start=0
v2w_wave_beat =0
v2w_wave_busy =False
v2w_wave_last =0
v2w_wave_seq  =0

julius_API = {}
julius_MAX = 3
julius_INI = 0
julius_SEQ = 0

def proc_v2w_wave(cn_r, cn_s, ):
    global v2w_wave_start
    global v2w_wave_beat
    global v2w_wave_busy
    global v2w_wave_last
    global v2w_wave_seq

    global julius_API
    global julius_MAX
    global julius_INI
    global julius_SEQ

    qFunc.logOutput('v2w_wave__:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    minSize  = cn_r.get()
    maxSize  = cn_r.get()
    cn_r.task_done()

    qFunc.logOutput('v2w_wave__:runMode =' + str(runMode ))
    qFunc.logOutput('v2w_wave__:micDev  =' + str(micDev  ))
    qFunc.logOutput('v2w_wave__:micType =' + str(micType ))
    qFunc.logOutput('v2w_wave__:micGuide=' + str(micGuide))
    qFunc.logOutput('v2w_wave__:minSize =' + str(minSize ))
    qFunc.logOutput('v2w_wave__:maxSize =' + str(maxSize ))

    qFunc.logOutput('v2w_wave__:start')
    v2w_wave_start = time.time()

    if (True):
        #julius_API = {}
        #julius_MAX = 3
        #julius_INI = 0
        #julius_SEQ = 0
        for j in range(1, julius_MAX):
            julius_INI += 1
            if (julius_INI > (julius_MAX * 20)):
                julius_INI = 1
            j = ((julius_INI - 1) % julius_MAX) + 1
            jx = '{:02}'.format(j)
            julius_API[j] = speech_api_julius.proc_julius('julius', jx, )
            julius_API[j].start()



    while (True):
        v2w_wave_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qFunc.logOutput('v2w_wave__:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qFunc.logOutput('v2w_wave__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #v2w_wave_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                v2w_wave_busy = True

                result = 'OK'

                path=qPath_s_inp
                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:

                        bytebase=0
                        for f in files:
                            file=f.replace('\\', '/')
                            if (os.name != 'nt'):
                                time.sleep(2.00)
                            if (file[-4:].lower() == '.wav' and file[-8:].lower() != '.tmp.wav'):
                                a = open(file, 'a')
                                a.close()
                                a = None
                            if (file[-4:].lower() == '.wav' and file[-8:].lower() != '.tmp.wav'):
                                f1=file
                                f2=file[:-4] + '.tmp.wav'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass
                            if (file[-4:].lower() == '.mp3' and file[-8:].lower() != '.tmp.mp3'):
                                f1=file
                                f2=file[:-4] + '.tmp.mp3'
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                            if (file[-8:].lower() == '.tmp.wav' or file[-8:].lower() == '.tmp.mp3'):
                                f1=file
                                f2=file[:-8] + file[-4:]
                                try:
                                    os.rename(f1, f2)
                                    file=f2
                                except:
                                    pass

                                fileId = file.replace(path, '')
                                fileId = fileId[:-4]

                                v2w_wave_seq += 1
                                if (v2w_wave_seq >= 10000):
                                    v2w_wave_seq = 1
                                seq4 = '{:04}'.format(v2w_wave_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPath_work + 'v2w_wave.' + seq2 + '.wav'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', wrkfile, ], \
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                sox.wait()
                                sox.terminate()
                                sox = None

                                if (micDev.isdigit()):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (runMode == 'debug') or (not micDev.isdigit()):
                                        qFunc.logOutput('v2w_wave__:' + fileId + u' → ' + wrkfile[:-4])

                                    wrksize = 0
                                    try:
                                        rb = open(wrkfile, 'rb')
                                        wrksize = sys.getsizeof(rb.read())
                                        rb.close
                                        rb = None
                                    except:
                                        pass

                                    v2w_wave_last = time.time()

                                    v2w_wave_sub(micDev, seq4, fileId, file, wrkfile, wrksize, bytebase, minSize, maxSize, )

                                    if (not micDev.isdigit()):
                                        bytebase += wrksize - 44

                    except:
                        pass
                        result = 'NG'

                if (not micDev.isdigit()):
                    if (result == 'OK'):
                        cn_s.put(['END', ''])
                        time.sleep( 5.00)
                        break
                    else:
                        cn_s.put(['ERROR', ''])
                        time.sleep( 5.00)
                        break
                else:
                    cn_s.put([result, ''])

        v2w_wave_busy = False

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qFunc.logOutput('v2w_wave__:terminate')

    qFunc.kill('julius')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qFunc.logOutput('v2w_wave__:end')



def main_init(micDev, ):

    qFunc.makeDirs('temp/_log/',   False)
    qFunc.makeDirs('temp/_cache/', False)

    if (micDev.isdigit()):
        qFunc.makeDirs(qPath_s_ctrl, False)
        qFunc.makeDirs(qPath_s_inp,  True )
        qFunc.makeDirs(qPath_s_wav,  True )
        qFunc.makeDirs(qPath_s_jul,  True )
        qFunc.makeDirs(qPath_s_STT,  False)
        qFunc.makeDirs(qPath_s_TTS,  False)
        qFunc.makeDirs(qPath_s_TRA,  False)
        qFunc.makeDirs(qPath_s_play, False)
        qFunc.makeDirs(qPath_rec,  False)
        qFunc.makeDirs(qPath_work, False)
    else:
        qFunc.makeDirs(qPath_s_ctrl, False)
        qFunc.makeDirs(qPath_s_inp,  False)
        qFunc.makeDirs(qPath_s_wav,  True )
        qFunc.makeDirs(qPath_s_jul,  True )
        qFunc.makeDirs(qPath_s_STT,  False)
        qFunc.makeDirs(qPath_s_TTS,  False)
        qFunc.makeDirs(qPath_s_TRA,  False)
        qFunc.makeDirs(qPath_s_play, False)
        qFunc.makeDirs(qPath_rec,  False)
        qFunc.makeDirs(qPath_work, False)

    qFunc.statusSet(qBusy_s_ctrl,  False )
    qFunc.statusSet(qBusy_s_inp,   False )
    qFunc.statusSet(qBusy_s_wav,   False )
    qFunc.statusSet(qBusy_s_STT,   False )
    qFunc.statusSet(qBusy_s_TTS,   False )
    qFunc.statusSet(qBusy_s_TRA,   False )
    qFunc.statusSet(qBusy_s_play,  False )



main_start=0
main_beat =0
main_busy =False
main_last =0
main_seq  =0
if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    #global main_beat
    #global audio_beat
    #global adinxxx_run
    #global adinxxx_sbp
    #global v2w_wave_beat

    qFunc.logOutput('')
    qFunc.logOutput('v2w_main__:init')
    qFunc.logOutput('v2w_main__:exsample.py runMode, mic..., ')
    #runMode  handsfree, translator, speech, ...,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound

    runMode  = 'debug'
    micDev   = '0'
    micType  = 'bluetooth'
    micGuide = 'on'
    micLevel = '777'

    minSize  =  10000
    maxSize  = 384000

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
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

    qFunc.logOutput('')
    qFunc.logOutput('v2w_main__:runMode  =' + str(runMode  ))
    qFunc.logOutput('v2w_main__:micDev   =' + str(micDev   ))
    qFunc.logOutput('v2w_main__:micType  =' + str(micType  ))
    qFunc.logOutput('v2w_main__:micGuide =' + str(micGuide ))
    qFunc.logOutput('v2w_main__:micLevel =' + str(micLevel ))

    main_init(micDev, )

    qFunc.kill('adintool-gui')
    qFunc.kill('adintool')
    qFunc.kill('julius')

    qFunc.logOutput('')
    qFunc.logOutput('v2w_main__:start')
    main_start     = time.time()
    main_beat      = 0

    audio_s        = queue.Queue()
    audio_r        = queue.Queue()
    audio_proc     = None
    audio_beat     = 0
    audio_pass     = 0

    v2w_wave_s     = queue.Queue()
    v2w_wave_r     = queue.Queue()
    v2w_wave_proc  = None
    v2w_wave_beat  = 0
    v2w_wave_pass  = 0

    while (True):
        main_beat = time.time()

        # check v2w_wave_last

        if (not micDev.isdigit()):
            if (v2w_wave_last == 0):
                v2w_wave_last = time.time()
            sec = (time.time() - v2w_wave_last)
            if (sec > 90):
                break

        if (micDev.isdigit()):
            if (qFunc.statusCheck(qBusy_s_ctrl) == True) \
            or (qFunc.statusCheck(qBusy_s_STT ) == True) \
            or (qFunc.statusCheck(qBusy_s_TTS ) == True) \
            or (qFunc.statusCheck(qBusy_s_play) == True):
                v2w_wave_last = 0
            if (v2w_wave_last == 0):
                v2w_wave_last = time.time()
            sec = (time.time() - v2w_wave_last)
            if (sec > 99): #30->9999->99
                qFunc.logOutput('v2w_main__:audio_proc 99s reboot !')
                audio_beat   = main_start
                v2w_wave_last = 0

        # Thread timeout check

        if (audio_beat != 0):
          if (micDev.isdigit()):
            sec = (time.time() - audio_beat)
            if (sec > 60):
                qFunc.logOutput('v2w_main__:audio_proc 60s')
                qFunc.logOutput('v2w_main__:audio_proc break')
                audio_s.put([None, None])
                time.sleep(3.00)
                audio_proc = None
                audio_beat = 0
                audio_pass = 0

                if (adingui_run == True):
                    adingui_run = False
                    if (not adingui_sbp is None):
                        adingui_sbp.terminate()
                        adingui_sbp = None
                if (adinexe_run == True):
                    adinexe_run = False
                    if (not adinexe_sbp is None):
                        adinexe_sbp.terminate()
                        adinexe_sbp = None
                if (adinsvr_run == True):
                    adinsvr_run = False
                    if (not adinsvr_sbp is None):
                        adinsvr_sbp.terminate()
                        adinsvr_sbp = None

                qFunc.kill('adintool-gui')
                qFunc.kill('adintool')

                if (micGuide != 'off'):
                    qFunc.guide('_down')

        if (v2w_wave_beat != 0):
          if (micDev.isdigit()):
            sec = (time.time() - v2w_wave_beat)
            if (sec > 60):
                qFunc.logOutput('v2w_main__:v2w_wave_proc 60s')
                qFunc.logOutput('v2w_main__:v2w_wave_proc break')
                v2w_wave_s.put([None, None])
                time.sleep(3.00)
                v2w_wave_proc = None
                v2w_wave_beat = 0
                v2w_wave_pass = 0

        # Thread start

        if (audio_proc is None):
            while (audio_s.qsize() > 0):
                dummy = audio_s.get()
            while (audio_r.qsize() > 0):
                dummy = audio_r.get()
            audio_proc = threading.Thread(target=proc_audio, args=(audio_s,audio_r,))
            audio_proc.setDaemon(True)
            audio_s.put(runMode )
            audio_s.put(micDev  )
            audio_s.put(micType )
            audio_s.put(micGuide)
            audio_s.put(micLevel)
            audio_proc.start()
            time.sleep(1.00)

            audio_s.put(['START', ''])

        if (v2w_wave_proc is None):
            while (v2w_wave_s.qsize() > 0):
                dummy = v2w_wave_s.get()
            while (v2w_wave_r.qsize() > 0):
                dummy = v2w_wave_r.get()
            v2w_wave_proc = threading.Thread(target=proc_v2w_wave, args=(v2w_wave_s,v2w_wave_r,))
            v2w_wave_proc.setDaemon(True)
            v2w_wave_s.put(runMode )
            v2w_wave_s.put(micDev  )
            v2w_wave_s.put(micType )
            v2w_wave_s.put(micGuide)
            v2w_wave_s.put(minSize )
            v2w_wave_s.put(maxSize )
            v2w_wave_proc.start()
            time.sleep(1.00)

            v2w_wave_s.put(['START', ''])

        # processing

        if (audio_r.qsize() == 0 and audio_s.qsize() == 0):
            audio_s.put(['PROC', ''])
            audio_pass += 1
        else:
            audio_pass = 0
        if (audio_pass > 50):
            audio_s.put(['PASS', ''])
            audio_pass = 0

        while (audio_r.qsize() > 0):
            audio_get = audio_r.get()
            audio_res = audio_get[0]
            audio_dat = audio_get[1]
            audio_r.task_done()

        if (v2w_wave_r.qsize() == 0 and v2w_wave_s.qsize() == 0):
            v2w_wave_s.put(['PROC', ''])
            v2w_wave_pass += 1
        else:
            v2w_wave_pass = 0
        if (v2w_wave_pass > 50):
            v2w_wave_s.put(['PASS', ''])
            v2w_wave_pass = 0

        break_flag = False
        while (v2w_wave_r.qsize() > 0):
            v2w_wave_get = v2w_wave_r.get()
            v2w_wave_res = v2w_wave_get[0]
            v2w_wave_dat = v2w_wave_get[1]
            v2w_wave_r.task_done()
            if (v2w_wave_res == 'END'):
                break_flag = True
            if (v2w_wave_res == 'ERROR'):
                break_flag = True
        if (break_flag == True):
            break



        time.sleep(0.05)



    qFunc.logOutput('')
    qFunc.logOutput('v2w_main__:terminate')

    try:
        audio_s.put(  [None, None] )
        v2w_wave_s.put( [None, None] )
        time.sleep(3.00)
    except:
        pass

    if (adingui_run == True):
        adingui_run = False
        if (not adingui_sbp is None):
            adingui_sbp.terminate()
            adingui_sbp = None
    if (adinexe_run == True):
        adinexe_run = False
        if (not adinexe_sbp is None):
            adinexe_sbp.terminate()
            adinexe_sbp = None
    if (adinsvr_run == True):
        adinsvr_run = False
        if (not adinsvr_sbp is None):
            adinsvr_sbp.terminate()
            adinsvr_sbp = None

    qFunc.kill('adintool-gui')
    qFunc.kill('adintool')

    if (bakSox_run == True):
        bakSox_run = False
        if (not bakSox_sbp is None):
            bakSox_sbp.terminate()
            bakSox_sbp = None

    try:
        audio_proc.join()
        v2w_wave_proc.join()
    except:
        pass

    qFunc.statusSet(qBusy_s_inp, False)

    qFunc.logOutput('v2w_main__:bye!')



