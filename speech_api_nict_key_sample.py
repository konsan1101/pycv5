#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



def getkey(api, key):

    # nict 音声認識
    if (api == 'stt'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            #return 'your id'
            return 'your id'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    # nict 翻訳機能
    if (api == 'tra'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            #return 'your id'
            return 'your id'
        if (key == 'key'):
            #return 'your key'
            return 'your key'
v
    # nict 音声合成
    if (api == 'tts'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            #return 'your id'
            return 'your id'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    return False


