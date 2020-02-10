#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import datetime



import _v5__qLog
qLog = _v5__qLog.qLog_class()



def sub():
    proc_name = 'sub'
    proc_id   = '{0:10s}'.format(proc_name).replace(' ', '_')

    qLog.log('info', proc_id, 'start')
    qLog.log('info', proc_id, 'error test ↓')
    try:
        a=100/0
    except Exception as e:
        qLog.exception(e)        
    qLog.log('info', proc_id, 'end')
    
    return True



if __name__ == '__main__':
    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # ログ
    if (not os.path.isdir('temp')):
        os.makedirs('temp')
    if (not os.path.isdir('temp/_log')):
        os.makedirs('temp/_log')
    filename = 'temp/_log/' + os.path.basename(__file__) + '.log'
    qLog.init(mode='nologger', filename=filename, )
    #qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'run')

    qLog.log('info'    , main_id, '')
    qLog.log('debug'   , main_id, 'debug')
    qLog.log('warning' , main_id, 'warning')
    qLog.log('error'   , main_id, 'error')
    qLog.log('critical', main_id, 'critical')
    qLog.log('info'    , main_id, '')

    x = sub()


