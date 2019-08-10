#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



# インターフェース
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qFunc.kill('adintool-gui')
qFunc.kill('adintool')
qFunc.kill('julius')

qFunc.kill('sox')

qFunc.txtsWrite(qCtrl_control_desktop , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('ffmpeg')

qFunc.txtsWrite(qCtrl_control_bgm     , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('VLC') # Danger!

qFunc.txtsWrite(qCtrl_control_browser , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('firefox')

qFunc.txtsWrite(qCtrl_control_player  , txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
qFunc.kill('ffplay')

qFunc.kill('python')


