#!/usr/bin/env python
# -*- coding: utf-8 -*-

# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qFunc.kill('adintool-gui')
qFunc.kill('adintool')
qFunc.kill('julius')

qFunc.kill('sox')
qFunc.kill('VLC') # Danger!
qFunc.kill('ffmpeg')

qFunc.kill('python')


