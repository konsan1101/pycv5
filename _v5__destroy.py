#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qFunc.kill('adintool-gui')
qFunc.kill('adintool')
qFunc.kill('julius')

qFunc.kill('sox')
qFunc.kill('VLC') # Danger!

qFunc.kill('ffmpeg')
qFunc.kill('ffplay')

qFunc.kill('python')


