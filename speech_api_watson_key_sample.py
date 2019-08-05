#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



def getkey(api, key):

    # Watson 音声認識
    if (api == 'stt'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            #return 'your name'
            return 'your name'
        if (key == 'password'):
            #return 'your key'
            return 'your key'

    # Watson 翻訳機能
    if (api == 'tra'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            #return 'your name'
            return 'your name'
        if (key == 'password'):
            #return 'your key'
            return 'your key'

    # Watson 音声合成
    if (api == 'tts'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            #return 'your name'
            return 'your name'
        if (key == 'password'):
            #return 'your key'
            return 'your key'

    return False



