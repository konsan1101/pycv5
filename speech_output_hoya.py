#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess



# hoya 音声合成
import speech_api_hoya     as hoya_api
import speech_api_hoya_key as hoya_key



if __name__ == '__main__':

    outLang = 'ja'
    outFile = 'temp/temp_speech.txt'
    tmpFile = 'temp/temp_voice.wav'

    if (len(sys.argv) >= 2):
        outLang = sys.argv[1]
    if (len(sys.argv) >= 3):
        outFile = sys.argv[2]
    if (len(sys.argv) >= 4):
        tmpFile = sys.argv[3]



    print('')
    print('speech_output_hoya.py')
    print(' 1)outLang = ' + str(outLang))
    print(' 2)outFile = ' + str(outFile))
    print(' 3)tmpFile = ' + str(tmpFile))



    if (os.path.exists(tmpFile)):
        os.remove(tmpFile)

    outText = ''
    if (os.path.exists(outFile)):

        rt = codecs.open(outFile, 'r', 'shift_jis')
        for t in rt:
            outText = (outText + ' ' + str(t)).strip()
        rt.close
        rt = None

    print(' ' + outText)
    if (outText != ''):
        #try:

        hoyaAPI = hoya_api.SpeechAPI()
        res = hoyaAPI.authenticate(hoya_key.getkey(), )
        if (res == True):

            res, api = hoyaAPI.vocalize(outText=outText, outLang=outLang, outFile=tmpFile)
            if (res != ''):

                sox = subprocess.Popen(['sox', tmpFile, '-d', '-q'])
                sox.wait()
                sox.terminate()
                sox = None

        #except:
        #print(' Error!', sys.exc_info()[0])



