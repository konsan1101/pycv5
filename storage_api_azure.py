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

from azure.storage.blob import BlockBlobService, PublicAccess



# azure blob
import storage_api_azure_key as azure_key



class StorageAPI:

    def __init__(self, ):
        self.timeOut   = 10
        self.blob_account = None
        self.blob_key     = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, account, key, ):
        # azure blob
        if (api == 'blob'):
            self.blob_account = account
            self.blob_key     = key
            return True

        return False



    def put(self, inpFile, container='default', outFile='temp.tmp', ):
        if (self.blob_account is None):
            print('AZURE: Not Authenticate Error !')

        else:

            # Service connect
            block_blob_service = BlockBlobService(
                account_name = self.blob_account, 
                account_key  = self.blob_key,
                )

            # Create a container
            block_blob_service.create_container(container)

        return True



if __name__ == '__main__':

        #azureAPI = azure_api.StorageAPI()
        azureAPI = StorageAPI()

        res1 = azureAPI.authenticate('blob', 
                    azure_key.getkey('blob', 'account', ),
                    azure_key.getkey('blob', 'key', ),
                    )

        print('authenticate:', res1, )

        if (res1 == True):

            inpFile = '_photos/_photo_cv.jpg'
            res = azureAPI.put(inpFile, container='default', outFile='_photo_cv.jpg', )
            print('put:', res, )


