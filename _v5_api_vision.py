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

import multiprocessing



# 出力インターフェース
qCtrl_result_vision      = 'temp/result_vision.txt'
qCtrl_result_cv          = 'temp/result_cv.txt'
qCtrl_result_cv_sjis     = 'temp/result_cv_sjis.txt'
qCtrl_result_ocr         = 'temp/result_ocr.txt'
qCtrl_result_ocr_sjis    = 'temp/result_ocr_sjis.txt'
qCtrl_result_ocrTrn      = 'temp/result_ocr_translate.txt'
qCtrl_result_ocrTrn_sjis = 'temp/result_ocr_translate_sjis.txt'



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

google = False

qApiCV     = 'azure'
qApiOCR    = qApiCV
qApiTrn    = qApiCV
qLangCV    = 'ja'
qLangOCR   = qLangCV
qLangTrn   = 'en'



# google 画像認識、OCR認識
if (google == True):
    import vision_api_google     as google_api
    import vision_api_google_key as google_key

# google 機械翻訳
if (google == True):
    import speech_api_google     as a_google_api
    import speech_api_google_key as a_google_key

# azure 画像認識、OCR認識
import vision_api_azure     as azure_api
import vision_api_azure_key as azure_key

# azure 翻訳機能
import speech_api_azure     as a_azure_api
import speech_api_azure_key as a_azure_key



def qVisionCV(useApi='google', inpLang='ja', inpFile='vision__cv_photo.jpg', tmpFile='temp_cv_photo.jpg', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None
    resLM   = ''

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        if (google == True):
            api = 'google'
        else:
            api = 'azure'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.VisionAPI()
        res = azureAPI.authenticate('cv' ,
                   azure_key.getkey('cv' ,'url'),
                   azure_key.getkey('cv' ,'key'), )
        if (res == True):
            res = azureAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=False, )
            if (res == True):
                res, api = azureAPI.cv(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    if (res['captions'] != ''):
                        resText = res['captions']
                        resLM   = resText
                    else:
                        resText = res['categories']
                    resApi  = api
                    resAry  = []
                    if (res['captions'] != ''):
                        resAry.append('[captions] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['captions'])
                        resAry.append('')
                    if (res['categories'] != ''):
                        resAry.append('[categories] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['categories'])
                        resAry.append('')
                    if (res['description'] != ''):
                        resAry.append('[description] ' + inpLang + ' (' + api + ')')
                        resAry.append(' ' + res['description'])
                        resAry.append('')

        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (google == True):
        if (resText == '') and ((api == 'free') or (api == 'google')):
            googleAPI = google_api.VisionAPI()
            res = googleAPI.authenticate('cv' ,
                    google_key.getkey('cv' ,'url'),
                    google_key.getkey('cv' ,'key'), )
            if (res == True):
                res = googleAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=False, )
                if (res == True):
                    res, api = googleAPI.cv(inpImage=tmpFile, inpLang=inpLang, )
                    if (not res is None):
                        #print(res)
                        if (res['landmark'] != ''):
                            resText = res['landmark']
                            resLM   = resText
                        else:
                            resText = res['label']
                        resApi  = api
                        resAry  = []
                        if (res['landmark'] != ''):
                            resAry.append('[landmark] ' + inpLang + ' (' + api + ')')
                            resAry.append(' ' + res['landmark'])
                            resAry.append('')
                        if (res['label'] != ''):
                            resAry.append('[label] ' + inpLang + ' (' + api + ')')
                            resAry.append(' ' + res['label'])
                            resAry.append('')

    if (resText != ''):
        return resText, resApi, resAry, resLM

    return '', '', None, ''



def qVisionOCR(useApi='google', inpLang='ja', inpFile='vision__ocr_photo.jpg', tmpFile='temp_ocr_photo.jpg', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        if (google == True):
            api = 'google'
        else:
            api = 'azure'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.VisionAPI()
        res = azureAPI.authenticate('ocr' ,
                   azure_key.getkey('ocr' ,'url'),
                   azure_key.getkey('ocr' ,'key'), )
        if (res == True):
            res = azureAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=True, )
            if (res == True):
                res, api = azureAPI.ocr(inpImage=tmpFile, inpLang=inpLang, )
                if (not res is None):
                    #print(res)
                    resText = ''
                    resApi  = api
                    resAry  = []
                    if (len(res) > 0):
                        resAry.append('[OCR] ' + inpLang + ' (' + api + ')')
                        for text in res:
                            resAry.append(' ' + text)
                            resText += ' ' + text
                            resText = str(resText).strip()

    if (google == True):
        if (resText == '') and ((api == 'free') or (api == 'google')):
            googleAPI = google_api.VisionAPI()
            res = googleAPI.authenticate('ocr' ,
                    google_key.getkey('ocr' ,'url'),
                    google_key.getkey('ocr' ,'key'), )
            if (res == True):
                res = googleAPI.convert(inpImage=inpFile, outImage=tmpFile, bw=True, )
                if (res == True):
                    res, api = googleAPI.ocr(inpImage=tmpFile, inpLang=inpLang, )
                    if (not res is None):
                        #print(res)
                        resText = ''
                        resApi  = api
                        resAry  = []
                        if (len(res) > 0):
                            resAry.append('[OCR] ' + inpLang + ' (' + api + ')')
                            for text in res:
                                resAry.append(' ' + text)
                                resText += ' ' + text
                                resText = str(resText).strip()

    if (resText != ''):
        return resText, resApi, resAry

    return '', '', None



def qOCR2Trn(useApi='google', inpLang='ja', inpAry=['Hallo'], trnLang='en', apiRecovery=False,):
    resText = ''
    resApi  = ''
    resAry  = None

    api   = useApi
    if  (api != 'free') and (api != 'google') \
    and (api != 'azure'):
        if (google == True):
            api = 'google'
        else:
            api = 'azure'

    if (resText == '') and (api == 'azure'):
        a_azureAPI = a_azure_api.SpeechAPI()
        key     = a_azure_key.getkey('tra', 'key', )
        authurl = a_azure_key.getkey('tra', 'authurl', )
        procurl = a_azure_key.getkey('tra', 'procurl', )
        res = a_azureAPI.authenticate('tra', key, authurl, procurl, )
        if (res == True):
            resAry = []
            resAry.append('[Translate] ' + trnLang + ' (' + api + ')')
            l = 0
            for text in inpAry:
                l+=1
                if ( l>1 ):
                    outText, api = a_azureAPI.translate(inpText=text, inpLang=inpLang, outLang=trnLang, )
                    if (outText != ''):
                        text   = outText
                        resApi = api
                    resAry.append(text)
                    resText += str(text) + ','

    if (google == True):
        if (resText == '') and ((api == 'free') or (api == 'google')):
            a_googleAPI = a_google_api.SpeechAPI()
            a_res = a_googleAPI.authenticate('tra', a_google_key.getkey('tra'), )
            if (a_res == True):
                resAry = []
                resAry.append('[Translate] ' + trnLang + ' (' + api + ')')
                l = 0
                for text in inpAry:
                    l+=1
                    if ( l>1 ):
                        outText, api = a_googleAPI.translate(inpText=text, inpLang=inpLang, outLang=trnLang, )
                        if (outText != ''):
                            text   = outText
                            resApi = api
                        resAry.append(text)
                        resText += str(text) + ','

    if (resText != ''):
        return resText, resApi, resAry

    return '', '', None



def vision_batch(runMode, camDev,
                qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
                procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn, ):

    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=False, outfile=True, )
    #qFunc.logOutput(qLogFile, )

    qFunc.remove(qCtrl_result_vision      )
    qFunc.remove(qCtrl_result_cv          )
    qFunc.remove(qCtrl_result_cv_sjis     )
    qFunc.remove(qCtrl_result_ocr         )
    qFunc.remove(qCtrl_result_ocr_sjis    )
    qFunc.remove(qCtrl_result_ocrTrn      )
    qFunc.remove(qCtrl_result_ocrTrn_sjis )

    if (inpCV != ''):
        res,api,ary,landmark = qVisionCV(qApiCV, qLangCV, inpCV, tmpCV)
        if (api == qApiCV) or (api == 'free' and qApiCV == 'google'):
                qFunc.logOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (' + api + ')', True)
        else:
            if (api != ''):
                qFunc.logOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (!' + api + ')', True)
            else:
                qFunc.logOutput(' ' + procId + ' Vision CV    [' + res + '] ' + qLangCV + ' (!' + qApiCV + ')', True)

        if (res != ''):
            if (outCV != ''):
                qFunc.txtsWrite(outCV, txts=ary, encoding='utf-8', exclusive=False, mode='w', )

            if (qCtrl_result_cv != ''):
                qFunc.txtsWrite(qCtrl_result_cv, txts=ary, encoding='utf-8', exclusive=True, mode='w', )

            if (qCtrl_result_cv_sjis != ''):
                qFunc.txtsWrite(qCtrl_result_cv_sjis, txts=ary, encoding='shift_jis', exclusive=True, mode='w', )

            if (landmark != ''):
                qFunc.logOutput(' ' + procId + ' Landmark     [' + landmark + '] ' + qLangCV + ' (!' + qApiCV + ')', True)

                recfile = outCV.replace(qPath_v_cv, '')
                recfile = recfile.replace(qPath_rec, '')
                recfile = qPath_s_TTS + recfile

                qFunc.txtsWrite(recfile, txts=[landmark], encoding='utf-8', exclusive=False, mode='w', )



    if (inpOCR != ''):
        res,api,ary = qVisionOCR(qApiOCR, qLangOCR, inpOCR, tmpOCR)
        if (api == qApiOCR) or (api == 'free' and qApiOCR == 'google'):
                qFunc.logOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (' + api + ')', True)
        else:
            if (api != ''):
                qFunc.logOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (!' + api + ')', True)
            else:
                qFunc.logOutput(' ' + procId + ' Vision OCR   [' + res + '] ' + qLangOCR + ' (!' + qApiOCR + ')', True)

        if (res != ''):
            if (outOCR != ''):
                qFunc.txtsWrite(outOCR, txts=ary, encoding='utf-8', exclusive=False, mode='w', )

            if (qCtrl_result_ocr != ''):
                qFunc.txtsWrite(qCtrl_result_ocr, txts=ary, encoding='utf-8', exclusive=True, mode='w', )

            if (qCtrl_result_ocr_sjis != ''):
                qFunc.txtsWrite(qCtrl_result_ocr_sjis, txts=ary, encoding='shift_jis', exclusive=True, mode='w', )

            trnRes,trnApi,trnAry = qOCR2Trn(qApiTrn, qLangOCR, ary, qLangTrn)
            if (api == qApiOCR) or (api == 'free' and qApiOCR == 'google'):
                    qFunc.logOutput(' ' + procId + ' Vision Trns  [' + trnRes + '] ' + qLangTrn + ' (' + api + ')', True)
            else:
                if (api != ''):
                    qFunc.logOutput(' ' + procId + ' Vision Trans [' + trnRes + '] ' + qLangTrn + ' (!' + api + ')', True)
                else:
                    qFunc.logOutput(' ' + procId + ' Vision Trans [' + trnRes + '] ' + qLangTrn + ' (!' + qApiTrn + ')', True)

            if (trnRes != ''):
                if (outTrn != ''):
                    qFunc.txtsWrite(outTrn, txts=trnAry, encoding='utf-8', exclusive=False, mode='w', )

                if (qCtrl_result_ocrTrn != ''):
                    qFunc.txtsWrite(qCtrl_result_ocrTrn, txts=trnAry, encoding='utf-8', exclusive=True, mode='w', )

                if (qCtrl_result_ocrTrn_sjis != ''):
                    qFunc.txtsWrite(qCtrl_result_ocrTrn_sjis, txts=trnAry, encoding='shift_jis', exclusive=True, mode='w', )



class api_vision_class:

    def __init__(self, ):
        self.timeOut     = 15
        self.vision_proc = None
        self.vision_id   = None
        
    def __del__(self, ):
        self.vision_id   = None

    def setTimeOut(self, timeOut=5, ):
        self.timeOut = timeOut

    def execute(self, sync, 
            runMode, camDev,
            qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
            procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn, 
            ):

        if (sync == True):
            vision_batch(
                runMode, camDev,
                qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
                procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn, 
                )

        # threading
        if (sync != True):
            self.vision_proc = threading.Thread(target=vision_batch, args=(
                runMode, camDev,
                qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
                procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn,
                ))
            self.vision_proc.setDaemon(True)
            self.vision_proc.start()

        # multiprocessing.Process
        #if (sync != True):
        #    self.vision_proc = multiprocessing.Process(target=vision_batch, args=(
        #        runMode, camDev,
        #        qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
        #        procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn,
        #        ))
        #    self.vision_proc.start()

        #if (sync == True):
        #    self.vision_proc.join()
        #    self.vision_id = None

        return True



if (__name__ == '__main__'):
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=False, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput('___main___:init')
    qFunc.logOutput('___main___:exsample.py runMode, api..., lang..., etc..., ')
    #runMode  debug, ...
    #api      google, azure,
    #lang     ja, en, fr, kr...

    runMode  = 'debug'
    camDev   = '0'

    procId   = '00'
    fileId   = 'temp_sample'

    inpCV    = '_photos/_photo_cv.jpg'
    tmpCV    = 'temp_cv_photo.jpg'
    outCV    = 'temp_cv_ja.txt'
    inpOCR   = '_photos/_photo_ocr_meter.jpg'
    tmpOCR   = 'temp_ocr_photo.jpg'
    outOCR   = 'temp_ocr_ja.txt'
    outTrn   = 'temp_ocr_en.txt'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        camDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        qApiCV   = str(sys.argv[3]).lower()
        qApiOCR  = qApiCV
        qApiTrn  = qApiCV
    if (len(sys.argv) >= 5):
        qApiOCR  = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        qApiTrn  = str(sys.argv[5]).lower()
    if (len(sys.argv) >= 7):
        qLangCV  = str(sys.argv[6]).lower()
        qLangOCR = qLangCV
    if (len(sys.argv) >= 8):
        qLangOCR = str(sys.argv[7]).lower()
    if (len(sys.argv) >= 9):
        qLangTrn = str(sys.argv[8]).lower()

    if (len(sys.argv) >= 10):
        procId   = sys.argv[9]
    if (len(sys.argv) >= 11):
        fileId   = sys.argv[10]

    if (len(sys.argv) >= 12):
        inpCV = sys.argv[11]
    if (len(sys.argv) >= 13):
        tmpCV = sys.argv[12]
    if (len(sys.argv) >= 14):
        outCV = sys.argv[13]
    if (len(sys.argv) >= 15):
        inpOCR = sys.argv[14]
    if (len(sys.argv) >= 16):
        tmpOCR = sys.argv[15]
    if (len(sys.argv) >= 17):
        outOCR = sys.argv[16]
    if (len(sys.argv) >= 18):
        outTrn = sys.argv[17]

    qFunc.logOutput('')
    qFunc.logOutput('___main___:runMode  =' + str(runMode  ))
    qFunc.logOutput('___main___:camDev   =' + str(camDev   ))
    qFunc.logOutput('___main___:qApiCV   =' + str(qApiCV   ))
    qFunc.logOutput('___main___:qApiOCR  =' + str(qApiOCR  ))
    qFunc.logOutput('___main___:qApiTrn  =' + str(qApiTrn  ))
    qFunc.logOutput('___main___:qLangCV  =' + str(qLangCV  ))
    qFunc.logOutput('___main___:qLangOCR =' + str(qLangOCR ))
    qFunc.logOutput('___main___:qLangTrn =' + str(qLangTrn ))

    qFunc.logOutput('___main___:procId   =' + str(procId   ))
    qFunc.logOutput('___main___:fileId   =' + str(fileId   ))

    qFunc.logOutput('___main___:inpCV    =' + str(inpCV    ))
    qFunc.logOutput('___main___:tmpCV    =' + str(tmpCV    ))
    qFunc.logOutput('___main___:outCV    =' + str(outCV    ))
    qFunc.logOutput('___main___:inpOCR   =' + str(inpOCR   ))
    qFunc.logOutput('___main___:tmpOCR   =' + str(tmpOCR   ))
    qFunc.logOutput('___main___:outOCR   =' + str(outOCR   ))
    qFunc.logOutput('___main___:outTrn   =' + str(outTrn   ))



    qFunc.logOutput('')
    qFunc.logOutput('___main___:start')



    # 画像処理 api
    #import       _v5_api_vision
    #api_vision = _v5_api_vision.api_vision_class()
    api_vision = api_vision_class()

    res = api_vision.execute(True,
            runMode, camDev,
            qApiCV, qApiOCR, qApiTrn, qLangCV, qLangOCR, qLangTrn,
            procId, fileId, inpCV, tmpCV, outCV, inpOCR, tmpOCR, outOCR, outTrn,
            )



    qFunc.logOutput('___main___:terminate')

    qFunc.logOutput('___main___:bye!')


