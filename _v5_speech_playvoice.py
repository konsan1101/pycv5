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



playvoice_start=0
playvoice_beat =0
playvoice_busy =False
playvoice_last =0
playvoice_seq  =0
def proc_playvoice(cn_r, cn_s, ):
    global playvoice_start
    global playvoice_beat
    global playvoice_busy
    global playvoice_last

    global playvoice_seq

    qFunc.logOutput('play_voice:init')

    runMode  = cn_r.get()
    micDev   = cn_r.get()
    micType  = cn_r.get()
    micGuide = cn_r.get()
    cn_r.task_done()

    qFunc.logOutput('play_voice:runMode =' + str(runMode ))
    qFunc.logOutput('play_voice:micDev  =' + str(micDev  ))
    qFunc.logOutput('play_voice:micType =' + str(micType ))
    qFunc.logOutput('play_voice:micGuide=' + str(micGuide))

    qFunc.logOutput('play_voice:start')
    playvoice_start=time.time()

    while (True):
        playvoice_beat = time.time()

        if (cn_r.qsize() > 0):
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if (mode_get is None):
                qFunc.logOutput('playvoice_:None=break')
                break

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 1):
                qFunc.logOutput('playvoice_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if (mode_get == 'PASS'):
                #playvoice_last = time.time()
                cn_s.put(['PASS', ''])

            else:

                playvoice_busy = True
                onece = True

                result = 'OK'

                path=qPath_s_play
                files = glob.glob(path + '*')
                if (len(files) > 0):

                    try:
                        for f in files:
                            file=f.replace('\\', '/')
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

                                playvoice_seq += 1
                                if (playvoice_seq >= 10000):
                                    playvoice_seq = 1
                                seq4 = '{:04}'.format(playvoice_seq)
                                seq2 = seq4[-2:]

                                wrkfile = qPath_work + 'playvoice.' + seq2 + '.mp3'
                                if (os.path.exists(wrkfile)):
                                    try:
                                        os.remove(wrkfile)
                                    except:
                                        pass

                                sox=subprocess.Popen(['sox', '-q', file, wrkfile, ], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                sox.wait()
                                sox.terminate()
                                sox = None

                                if (micDev.isdigit()):
                                    os.remove(file)

                                if (os.path.exists(wrkfile)):

                                    if (onece == True):
                                        onece = False
                                        qFunc.busySet(qBusy_s_play, True)

                                        #qFunc.busyCheck(qBusy_s_ctrl, 3)
                                        #qFunc.busyCheck(qBusy_s_STT , 3)
                                        #qFunc.busyCheck(qBusy_s_TTS , 3)
                                        #qFunc.busyCheck(qBusy_s_play, 3)
                                        if (micType == 'bluetooth') or (micGuide == 'on' or micGuide == 'sound'):
                                            qFunc.busyCheck(qBusy_s_inp, 3)

                                    if (runMode == 'debug') or (not micDev.isdigit()):
                                        qFunc.logOutput('play_voice:' + fileId + u' → ' + wrkfile[:-4])

                                    playvoice_last = time.time()

                                    sox=subprocess.Popen(['sox', '-q', wrkfile, '-d', '--norm', ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                                    #if (not micDev.isdigit()):
                                    if (runMode=='debug' or runMode=='handsfree'):
                                        sox.wait()
                                        sox.terminate()
                                        sox = None

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

        playvoice_busy = False
        qFunc.busySet(qBusy_s_play, False)

        if (cn_r.qsize() == 0):
            time.sleep(0.25)
        else:
            time.sleep(0.05)

    qFunc.logOutput('play_voice:terminate')

    while (cn_r.qsize() > 0):
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qFunc.logOutput('play_voice:end')



def main_init(micDev, ):

    qFunc.makeDirs('temp/_log/',   False)
    qFunc.makeDirs('temp/_cache/', False)

    if (micDev.isdigit()):
        qFunc.makeDirs(qPath_s_ctrl, False)
        qFunc.makeDirs(qPath_s_inp,  False)
        qFunc.makeDirs(qPath_s_wav,  False)
        qFunc.makeDirs(qPath_s_jul,  False)
        qFunc.makeDirs(qPath_s_STT,  False)
        qFunc.makeDirs(qPath_s_TTS,  False)
        qFunc.makeDirs(qPath_s_TRA,  False)
        qFunc.makeDirs(qPath_s_play, True )
        qFunc.makeDirs(qPath_rec,  False)
        qFunc.makeDirs(qPath_work, False)
    else:
        qFunc.makeDirs(qPath_s_ctrl, False)
        qFunc.makeDirs(qPath_s_inp,  False)
        qFunc.makeDirs(qPath_s_wav,  False)
        qFunc.makeDirs(qPath_s_jul,  False)
        qFunc.makeDirs(qPath_s_STT,  False)
        qFunc.makeDirs(qPath_s_TTS,  False)
        qFunc.makeDirs(qPath_s_TRA,  False)
        qFunc.makeDirs(qPath_s_play, False)
        qFunc.makeDirs(qPath_rec,  False)
        qFunc.makeDirs(qPath_work, False)

    qFunc.busySet(qBusy_s_ctrl,  False )
    qFunc.busySet(qBusy_s_inp,   False )
    qFunc.busySet(qBusy_s_wav,   False )
    qFunc.busySet(qBusy_s_STT,   False )
    qFunc.busySet(qBusy_s_TTS,   False )
    qFunc.busySet(qBusy_s_TRA,   False )
    qFunc.busySet(qBusy_s_play,  False )



main_start=0
main_beat =0
main_busy =False
main_last =0
if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('')
    qFunc.logOutput('play_main_:init')
    qFunc.logOutput('play_main_:exsample.py runMode, mic..., ')
    #runMode  handsfree, translator, speech, ...,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound

    runMode  = 'debug'
    micDev   = '0'
    micType  = 'usb'
    micGuide = 'on'
    micLevel = '777'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        micType  = str(sys.argv[3]).lower()
    if (len(sys.argv) >= 5):
        micGuide = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        p = str(sys.argv[5]).lower()
        if (p.isdigit() and p != '0'):
            micLevel = p

    qFunc.logOutput('')
    qFunc.logOutput('play_main_:runMode  =' + str(runMode  ))
    qFunc.logOutput('play_main_:micDev   =' + str(micDev   ))
    qFunc.logOutput('play_main_:micType  =' + str(micType  ))
    qFunc.logOutput('play_main_:micGuide =' + str(micGuide ))
    qFunc.logOutput('play_main_:micLevel =' + str(micLevel ))

    main_init(micDev, )

    qFunc.logOutput('')
    qFunc.logOutput('play_main_:start')
    main_start     = time.time()
    main_beat      = 0

    playvoice_s    = queue.Queue()
    playvoice_r    = queue.Queue()
    playvoice_proc = None
    playvoice_beat = 0
    playvoice_pass = 0

    while (True):
        main_beat = time.time()

        # check voice2wav_last

        if (not micDev.isdigit()):
            if (playvoice_last == 0):
                playvoice_last = time.time()
            sec = (time.time() - playvoice_last)
            if (sec > 90):
                break

        # Thread timeout check

        if (playvoice_beat != 0):
          if (micDev.isdigit()):
            sec = (time.time() - playvoice_beat)
            if (sec > 60):
                qFunc.logOutput('play_main_:playvoice_proc 60s')
                qFunc.logOutput('play_main_:playvoice_proc break')
                playvoice_s.put([None, None])
                time.sleep(3.00)
                playvoice_proc = None
                playvoice_beat = 0
                playvoice_pass = 0

                #kill = subprocess.Popen(['_speech_a3_kill_sox.bat', ], \
                #       stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                #kill.wait()
                #kill.terminate()
                #kill = None

        # Thread start

        if (playvoice_proc is None):
            while (playvoice_s.qsize() > 0):
                dummy = playvoice_s.get()
            while (playvoice_r.qsize() > 0):
                dummy = playvoice_r.get()
            playvoice_proc = threading.Thread(target=proc_playvoice, args=(playvoice_s,playvoice_r,))
            playvoice_proc.setDaemon(True)
            playvoice_s.put(runMode )
            playvoice_s.put(micDev  )
            playvoice_s.put(micType )
            playvoice_s.put(micGuide)
            playvoice_proc.start()
            time.sleep(1.00)

            playvoice_s.put(['START', ''])

        # processing

        if (playvoice_r.qsize() == 0 and playvoice_s.qsize() == 0):
            playvoice_s.put(['PROC', ''])
            playvoice_pass += 1
        else:
            playvoice_pass = 0
        if (playvoice_pass > 50):
            playvoice_s.put(['PASS', ''])
            playvoice_pass = 0

        break_flag = False
        while (playvoice_r.qsize() > 0):
            playvoice_get = playvoice_r.get()
            playvoice_res = playvoice_get[0]
            playvoice_dat = playvoice_get[1]
            playvoice_r.task_done()
            if (playvoice_res == 'END'):
                break_flag = True
            if (playvoice_res == 'ERROR'):
                break_flag = True
        #if (break_flag == True):
        #    break



        time.sleep(0.05)



    qFunc.logOutput('')
    qFunc.logOutput('play_main_:terminate')

    try:
        playvoice_s.put( [None, None] )
        time.sleep(3.00)
    except:
        pass

    try:
        playvoice_proc.join()
    except:
        pass

    qFunc.busySet(qBusy_s_play, False)

    qFunc.logOutput('play_main_:bye!')



