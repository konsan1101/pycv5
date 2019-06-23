#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api, key):

    # azure 画像認識
    if (api == 'cv'):
        print('vision_api_azure_key.py')
        print('set your key!')
        if (key == 'url'):
            return 'https://japaneast.api.cognitive.microsoft.com/vision/v1.0/analyze'
        if (key == 'key'):
            return 'your key'

    # azure OCR認識
    if (api == 'ocr'):
        print('vision_api_azure_key.py')
        print('set your key!')
        if (key == 'url'):
            return 'https://japaneast.api.cognitive.microsoft.com/vision/v1.0/ocr'
        if (key == 'key'):
            return 'your key'

    return False


