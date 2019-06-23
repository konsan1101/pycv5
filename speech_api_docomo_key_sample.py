#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api,):

    # docomo 音声認識(amivoice)
    if (api == 'stt'):
        print('speech_api_docomo_key.py')
        print('set your key!')
        return 'your key'

    # docomo 雑談対話
    if (api == 'chatting'):
        print('speech_api_docomo_key.py')
        print('set your key!')
        return 'your key'

    # docomo 知識検索
    if (api == 'knowledge'):
        print('speech_api_docomo_key.py')
        print('set your key!')
        return 'your key'

    return False


