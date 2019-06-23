#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api, key):

    # nict 音声認識
    if (api == 'stt'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            return 'your id'
        if (key == 'key'):
            return 'your key'

    # nict 翻訳機能
    if (api == 'tra'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            return 'your id'
        if (key == 'key'):
            return 'your key'

    # nict 音声合成
    if (api == 'tts'):
        print('speech_api_nict_key.py')
        print('set your key!')
        if (key == 'id'):
            return 'your id'
        if (key == 'key'):
            return 'your key'

    return False


