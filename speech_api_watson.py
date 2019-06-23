#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

import requests
import json



# watson 音声認識、翻訳機能、音声合成
#import watson_developer_cloud as watson
import ibm_watson as watson
import speech_api_watson_key  as watson_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut  = 10
        self.stt      = None
        self.tra      = None
        self.tts      = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, user, pswd, ):
        # Watson 音声認識
        if (api == 'stt'):
            try:
                self.stt = watson.SpeechToTextV1(
                           url = 'https://stream.watsonplatform.net/speech-to-text/api',
                           username = user,
                           password = pswd, )
                return True
            except:
                pass

        # Watson 翻訳機能
        if (api == 'tra'):
            try:
                self.tra = watson.LanguageTranslatorV3(
                           version = '2018-05-01',
                           url = 'https://gateway.watsonplatform.net/language-translator/api',
                           username = user,
                           password = pswd, )
                return True
            except:
                pass

        # Watson 音声合成
        if (api == 'tts'):
            try:
                self.tts = watson.TextToSpeechV1(
                           url='https://stream.watsonplatform.net/text-to-speech/api',
                           username = user,
                           password = pswd, )
                return True
            except:
                pass

        return False

    def recognize(self, inpWave, inpLang='ja-JP', ):
        res_text = ''
        res_api  = ''
        if (self.stt is None):
            print('WATSON: Not Authenticate Error !')

        else:
            lang  = ''
            model = ''
            if (inpLang == 'auto'):
                lang  = 'ja-JP'
                model = 'ja-JP_BroadbandModel'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                lang  = 'ja-JP'
                model = 'ja-JP_BroadbandModel'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                lang  = 'en-US'
                model = 'en-US_BroadbandModel'
            elif (inpLang == 'ar'):
                lang  = 'ar-AR'
                model = 'ar-AR_BroadbandModel'
            elif (inpLang == 'es'):
                lang  = 'es-ES'
                model = 'es-ES_BroadbandModel'
            elif (inpLang == 'de'):
                lang  = 'de-DE'
                model = 'de-DE_BroadbandModel'
            elif (inpLang == 'fr'):
                lang  = 'fr-FR'
                model = 'fr-FR_BroadbandModel'
            elif (inpLang == 'it'):
                lang  = 'it-IT'
                model = 'it-IT_BroadbandModel'
            elif (inpLang == 'pt'):
                lang  = 'pt-BR'
                model = 'pt-BR_BroadbandModel'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                lang  = 'zh-CN'
                model = 'zh-CN_BroadbandModel'

            if (model != ''):
                try:
                    rb = open(inpWave, 'rb')
                    audio = rb.read()
                    rb.close
                    rb = None

                    res = self.stt.recognize(
                                   audio=audio,
                                   content_type='audio/wav',
                                   model=model,
                                   timestamps=True,
                                   word_confidence=True,
                                   ).get_result()
                    #print(res)
                    res_text = res['results'][0]['alternatives'][0]['transcript']
                    if (res_text != '') and (inpLang == 'ja' or inpLang == 'ja-JP'):
                        res_split = res_text.split()
                        res_text = ''
                        for sentence in res_split:
                            if (sentence[:2] != 'D_'):
                                res_text += sentence
                            else:
                                res_text += '(' + sentence[2:] +')'
                    if (res_text != ''):
                        res_api = 'watson'
                except:
                    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == u'。') \
                   or (res_text[-1:] == u'、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (inpLang == 'ja' or inpLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return res_text, res_api

    def translate(self, inpText=u'こんにちは', inpLang='ja-JP', outLang='en-US', ):
        if (self.tra is None):
            print('WATSON: Not Authenticate Error !')

        else:
            inp = ''
            out = ''

            if (inpLang == 'auto'):
                inp = 'ja-JP'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                inp = 'ja-JP'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                inp = 'en-US'
            elif (inpLang == 'ar'):
                inp = 'ar-AR'
            elif (inpLang == 'es'):
                inp = 'es-ES'
            elif (inpLang == 'de'):
                inp = 'de-DE'
            elif (inpLang == 'fr'):
                inp = 'fr-FR'
            elif (inpLang == 'it'):
                inp = 'it-IT'
            elif (inpLang == 'pt'):
                inp = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                inp = 'zh-CN'

            if   (outLang == 'ja' or outLang == 'ja-JP'):
                out = 'ja-JP'
            elif (outLang == 'en' or outLang == 'en-US'):
                out = 'en-US'
            elif (outLang == 'ar'):
                out = 'ar-AR'
            elif (outLang == 'es'):
                out = 'es-ES'
            elif (outLang == 'de'):
                out = 'de-DE'
            elif (outLang == 'fr'):
                out = 'fr-FR'
            elif (outLang == 'it'):
                out = 'it-IT'
            elif (outLang == 'pt'):
                out = 'pt-BR'
            elif (outLang == 'zh' or outLang == 'zh-CN'):
                out = 'zh-CN'

            if (inp != '') and (out != '') and (inpText != '') and (inpText != '!'):
                try:

                    res = self.tra.translate(
                                   text=inpText,
                                   source=inp,
                                   target=out,
                                   ).get_result()
                    #print(res)
                    res_text = res['translations'][0]['translation']
                    if (res_text != ''):
                        res_api = 'watson'

                except:
                    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == u'。') \
                   or (res_text[-1:] == u'、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (outLang == 'ja' or outLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return res_text, res_api

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.mp3', ):
        if (self.tts is None):
            print('WATSON: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except:
                    pass

            lang  = ''
            voice = ''

            if   (outLang == 'ja' or outLang=='ja-JP'):
                lang  = 'ja-JP'
                voice = 'ja-JP_EmiVoice'
            elif (outLang == 'en' or outLang == 'en-US'):
                lang  = 'en-US'
                voice = 'en-US_AllisonVoice'
            elif (outLang == 'es'):
                lang  = 'es-ES'
                voice = 'es-ES_SofiaVoice'
            elif (outLang == 'de'):
                lang  = 'de-DE'
                voice = 'de-DE_BirgitVoice'
            elif (outLang == 'fr'):
                lang  = 'fr-FR'
                voice = 'fr-FR_ReneeVoice'
            elif (outLang == 'it'):
                lang  = 'it-IT'
                voice = 'it-IT_FrancescaVoice'
            elif (outLang == 'pt'):
                lang  = 'pt-BR'
                voice = 'pt-BR_IsabelaVoice'

            if (voice != '') and (outText != '') and (outText != '!'):
                try:

                    mp3audio = self.tts.synthesize(
                                        text=outText,
                                        accept='audio/mp3',
                                        voice=voice,
                                        ).get_result().content
                    wb = open(outFile, 'wb')
                    wb.write(mp3audio)
                    wb.close()
                    wb = None

                    return outText, 'watson'
                except:
                    pass

        return '', ''



if __name__ == '__main__':

        #watsonAPI = watson_api.SpeechAPI()
        watsonAPI = SpeechAPI()

        res1 = watsonAPI.authenticate('stt',
                         watson_key.getkey('stt','username'),
                         watson_key.getkey('stt','password'), )
        res2 = watsonAPI.authenticate('tra',
                         watson_key.getkey('tra','username'),
                         watson_key.getkey('tra','password'), )
        res3 = watsonAPI.authenticate('tts',
                         watson_key.getkey('tts','username'),
                         watson_key.getkey('tts','password'), )
        print('authenticate:', res1, res2, res3)
        if (res1 == True) and (res2 == True) and (res3 == True):

            text = 'Hallo'
            file = 'temp_voice.mp3'

            res, api = watsonAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'])
            sox.wait()
            sox.terminate()
            sox = None

            file2 = 'temp_voice.wav'
            sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', file2, ])
            sox.wait()
            sox.terminate()
            sox = None

            res, api = watsonAPI.recognize(inpWave=file2, inpLang='en', )
            print('recognize:', res, '(' + api + ')' )

            res, api = watsonAPI.translate(inpText=res, inpLang='en', outLang='ja', )
            print('translate:', res, '(' + api + ')' )



