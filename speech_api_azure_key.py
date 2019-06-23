#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api,):

    # azure 音声認識
    if (api == 'stt'):
        print('speech_api_azure_key.py')
        print('set your key!')
        return 'speech', 'your key'

    # azure 音声合成
    if (api == 'tts'):
        print('speech_api_azure_key.py')
        print('set your key!')
        return 'speech', 'your key'

    # azure 翻訳機能
    if (api == 'tra'):
        print('speech_api_azure_key.py')
        print('set your key!')
        return 'translator', 'your key'

    return Flase, False


