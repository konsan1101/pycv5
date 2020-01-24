#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import codecs
import subprocess



# aws
import boto3

# aws ストレージ
import storage_api_aws_key as aws_key



class StorageAPI:

    def __init__(self, ):
        self.timeOut     = 10
        self.key_id      = None
        self.secret_key  = None
        self.region_name = 'ap-northeast-1'
        self.bucketid    = 'kondou-pycv-'

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, key_id, secret_key, ):
        # aws s3
        if (api == 's3'):
            try:
                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = key_id, 
                    aws_secret_access_key = secret_key,
                    region_name           = self.region_name,
                    )

                self.key_id     = key_id
                self.secret_key = secret_key

                s3 = None
                return True

            except:
                return False

        return False



    def s3_put(self, bucket='default', inpPath='', inpFile='', s3File='', ):
        if (s3File == ''):
            s3File = inpFile
        s3bucket = self.bucketid + bucket

        if (self.key_id is None):
            print('aws: Not Authenticate Error !')

        else:

            try:

                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = self.key_id, 
                    aws_secret_access_key = self.secret_key,
                    region_name           = self.region_name,
                    )

                # Create a bucket
                try:
                    s3.create_bucket(Bucket=s3bucket, 
                                     ACL='private', 
                                     CreateBucketConfiguration={'LocationConstraint': self.region_name}, )
                except:
                    pass

                # Upload file
                full_path_file = inpPath + inpFile
                s3.upload_file(full_path_file, s3bucket, s3File, )

                s3 = None
                return True

            except:
                return False

        return False

    def s3_dir(self, bucket='default', ):
        s3bucket = self.bucketid + bucket

        if (self.key_id is None):
            print('aws: Not Authenticate Error !')

        else:

            try:

                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = self.key_id, 
                    aws_secret_access_key = self.secret_key,
                    region_name           = self.region_name,
                    )

                # List s3s
                s3Files = []
                list_bucket = s3.list_objects(Bucket=s3bucket, )
                for content in list_bucket['Contents']:
                    #s3Files.append(content['Key'])
                    print(content['Key'])

                s3 = None
                return s3Files

            except:
                return False

        return False

    def s3_get(self, bucket='default', s3File='', outPath='', outFile='', ):
        if (outFile == ''):
            outFile = s3File
        s3bucket = self.bucketid + bucket

        if (self.key_id is None):
            print('aws: Not Authenticate Error !')

        else:

            try:

                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = self.key_id, 
                    aws_secret_access_key = self.secret_key,
                    region_name           = self.region_name,
                    )

                # Download file
                full_path_file = outPath + outFile
                s3.download_file(s3bucket, s3File, full_path_file, )

                s3 = None
                return True

            except:
                return False

        return False

    def s3_remove(self, bucket='default', s3File='', ):
        s3bucket = self.bucketid + bucket

        if (self.key_id is None):
            print('aws: Not Authenticate Error !')

        else:

            try:

                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = self.key_id, 
                    aws_secret_access_key = self.secret_key,
                    region_name           = self.region_name,
                    )

                # Delete file
                s3.delete_object(Bucket=s3bucket, Key=s3File, )

                s3 = None
                return True

            except:
                return False

        return False

    def s3_wait_get(self, bucket='default', s3File='', outPath='', outFile='', maxWait=10, ):
        if (outFile == ''):
            outFile = s3File
        s3bucket = self.bucketid + bucket

        if (self.key_id is None):
            print('aws: Not Authenticate Error !')

        else:

            try:

                # Service connect
                s3 = boto3.client('s3',
                    aws_access_key_id     = self.key_id, 
                    aws_secret_access_key = self.secret_key,
                    region_name           = self.region_name,
                    )

                # Wait & Download file
                chktime = time.time()
                res = self.s3_get(bucket=bucket, s3File=s3File, outPath=outPath, outFile=outFile, )
                while (res == False) and ((time.time() - chktime) <= maxWait):
                    time.sleep(1.00)
                    res = self.s3_get(bucket=bucket, s3File=s3File, outPath=outPath, outFile=outFile, )

                # Check
                if (os.path.exists(outPath + outFile)):
                    return True

            except:
                return False

        return False



if __name__ == '__main__':

        #awsAPI = aws_api.StorageAPI()
        awsAPI = StorageAPI()

        res1 = awsAPI.authenticate('s3', 
                    aws_key.getkey('s3', 'key_id',     ),
                    aws_key.getkey('s3', 'secret_key', ),
                    )

        print('authenticate:', res1, )

        if (res1 == True):

            inpPath = '_photos/'
            inpFile = '_photo_cv.jpg'
            res = awsAPI.s3_put(bucket='default', inpPath=inpPath, inpFile=inpFile, s3File='', )
            print('s3_put:', res, )

            res = awsAPI.s3_dir(bucket='default', )
            if (res != False):
                for f in res:
                    print('s3_dir:', f, )

            res = awsAPI.s3_get(bucket='default', s3File=inpFile, outPath='', outFile='temp_s3.jpg', )
            print('s3_get:', res, )

            res = awsAPI.s3_remove(bucket='default', s3File=inpFile, )
            print('s3_remove:', res, )


