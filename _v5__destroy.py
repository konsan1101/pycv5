#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import  time



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_chatting   = 'temp/control_chatting.txt'
qCtrl_control_knowledge  = 'temp/control_knowledge.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()



qFunc.txtsWrite(qCtrl_control_kernel , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.txtsWrite(qCtrl_control_speech , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('adintool-gui')
qFunc.kill('adintool')
qFunc.kill('julius')
qFunc.kill('sox')

qFunc.txtsWrite(qCtrl_control_vision , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

qFunc.txtsWrite(qCtrl_control_desktop , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('ffmpeg')

qFunc.txtsWrite(qCtrl_control_bgm     , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('VLC') # Danger!

qFunc.txtsWrite(qCtrl_control_browser , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('firefox')

qFunc.txtsWrite(qCtrl_control_player  , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('ffplay')

qFunc.txtsWrite(qCtrl_control_chatting  , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.txtsWrite(qCtrl_control_knowledge  , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )



time.sleep(5.00)
qFunc.kill('_v5__main__kernel')
qFunc.kill('_v5__main_speech')
qFunc.kill('_v5__main_vision')
qFunc.kill('_v5__main_desktop')
qFunc.kill('_v5__sub_bgm')
qFunc.kill('_v5__sub_browser')
qFunc.kill('_v5__sub_player')
qFunc.kill('_v5__sub_chatting')
qFunc.kill('_v5__sub_knowledge')

qFunc.kill('_v5_proc_recorder')
qFunc.kill('_v5_proc_uploader')



time.sleep(5.00)
qFunc.kill('python')


