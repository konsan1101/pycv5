#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import codecs
import subprocess

import cv2
import requests
import json



# watson 画像認識、OCR認識
#import watson_developer_cloud as watson
import ibm_watson as watson
import vision_api_watson_key as azure_key



class VisionAPI:

    def __init__(self, ):
        self.timeOut = 10
        self.cv_url  = None
        self.cv_key  = None
        self.ocr_url = None
        self.ocr_key = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, url, key, ):
        # watson 画像認識
        if (api == 'cv'):
            self.cv_url = url
            self.cv_key = key
            if (not self.cv_key is None):
                return True

        # watson OCR認識
        if (api == 'ocr'):
            self.ocr_url = url
            self.ocr_key = key
            if (not self.ocr_key is None):
                return True

        return False



    def convert(self, inpImage, outImage, bw=True, maxWidth=640, maxHeight=480, ):
        try:
            if (os.path.exists(outImage)):
                os.remove(outImage)

            image_img = cv2.imread(inpImage, cv2.IMREAD_UNCHANGED)
            if len(image_img.shape) == 3:
                image_height, image_width, image_channels = image_img.shape[:3]
            else:
                image_height, image_width = image_img.shape[:2]
                image_channels = 1

            proc_img    = image_img.copy()
            proc_width  = image_width
            proc_height = image_height
            if (bw == True):
                if (image_channels != 1):
                    proc_img = cv2.cvtColor(image_img, cv2.COLOR_BGR2GRAY)

                #proc_img = cv2.equalizeHist(proc_img)
                #proc_img = cv2.blur(proc_img, (3,3), 0)
                #_, proc_img = cv2.threshold(proc_img, 140, 255, cv2.THRESH_BINARY)

            if (maxWidth != 0):
                if (proc_width > maxWidth):
                    proc_height = int(proc_height * (maxWidth / proc_width))
                    proc_width  = maxWidth
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxHeight != 0):
                if (proc_height > maxHeight):
                    proc_width  = int(proc_width * (maxHeight / proc_height))
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxWidth != 0) and (maxWidth != 0):
                if (proc_width > maxWidth) or (proc_height > maxHeight):
                    proc_width  = maxWidth
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            cv2.imwrite(outImage, proc_img)
            return True

        except:
            pass

        return False



    def cv(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.cv_key is None):
            print('WATSON: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None

                    visual_recognition = watson.VisualRecognitionV3(
                        version = '2018-03-19', 
                        iam_apikey = self.cv_key,)

                    res = visual_recognition.classify(
                        images_file = rb,
                        threshold = '0.6',
                        owners = ["IBM"],
                        ).get_result()

                    print(res)

                    #if (res.status_code == 200):
                    #    res_json = json.loads(res.text)
                    #    #print(res_json)
                    #    categories  = ''
                    #    captions    = ''
                    #    description = ''
                    #    try:
                    #        for names in res_json.get('categories'):
                    #            nm = str(names.get('name')).replace('_',' ')
                    #            categories += nm.strip() + ','
                    #    except:
                    #        pass

                    #    try:
                    #        for texts in res_json.get('description').get('captions'):
                    #            cp = str(texts.get('text'))
                    #            captions = cp.strip() + ','
                    #    except:
                    #        pass

                    #    try:
                    #        for tag in res_json.get('description').get('tags'):
                    #            description += str(tag).strip() + ','
                    #    except:
                    #        pass

                    res_text = {}
                    #    res_text['categories']  = categories
                    #    res_text['captions']    = captions
                    #    res_text['description'] = description
                except:
                    pass

            return res_text, 'watson'

        return None, ''

    def ocr(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.ocr_key is None):
            print('WATSON: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None

                    res_text = None

                except:
                    pass

            return res_text, 'watson'

        return None, ''



if __name__ == '__main__':

        #watsonAPI = watson_api.VisionAPI()
        watsonAPI = VisionAPI()

        res1 = watsonAPI.authenticate('cv' ,
                    watson_key.getkey('cv' ,'url'),
                    watson_key.getkey('cv' ,'key'), )
        print('authenticate:', res1, )
        if (res1 == True):

            file = '_photos/_photo_cv.jpg'
            temp = 'temp_photo_cv.jpg'

            res = watsonAPI.convert(inpImage=file, outImage=temp, bw=False, )
            if (res == True):
                res, api = watsonAPI.cv(inpImage=temp, inpLang='ja', )
                if (not res is None):
                    print('cv')
                    print('categories:', res['categories'], '(' + api + ')' )
                    print('captions:', res['captions']   , '(' + api + ')' )
                    print('description:', res['description'], '(' + api + ')' )


