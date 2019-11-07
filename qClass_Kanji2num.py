#!/usr/bin/env python
# -*- coding: utf-8 -*-

class qKanji2num_class:

    def __init__(self, ):
        self.kans = '〇一二三四五六七八九'
        self.tais1 = '千百十'
        self.tais2 = '京兆億万'
        self.suuji = {'〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', \
                      '百', '千', '万', '億', '兆', \
                      '０', '１', '２', '３', '４', '５', '６', '７', '８', '９', \
                      '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    # 関数(1)_漢数字（例：二三五六〇一）を単純変換する関数
    def kan2num(self, text):
        for i, tmp in enumerate(self.kans):
            text = text.replace(tmp, str(i)) # replaceメソッドで置換
        return text

    # 関数(2)_4桁までの漢数字（例：六千五百八）を数値変換する関数
    def kans2numf(self, text):
        ans = 0 # 初期値（計算結果を加算していく）
        poss = 0 # スタート位置
        for i, tmp in enumerate(self.tais1):
            pos = text.find(tmp) # 大数（千百十）の位置を順次特定
            if pos == -1: # 対象となる大数（千百十）が無い場合
                block = 0
                pos = poss - 1
            elif  pos == poss: # '二千百'のように'千'と'百'の間に数字がない場合
                block = 1
            else:
                block = int(self.kan2num(text[poss:pos])) # 'possとposの間の漢数字を数値に変換
            ans += block * (10 ** (len(self.tais1) - i))
            poss = pos + 1 # possをposの次の位置に設定
        if poss != len(text): # 一の位の数字がある場合
            ans += int(self.kan2num(text[poss:len(text)]))
        return ans

    # 関数(3)_20桁までの漢数字（例：六兆五千百億十五万八千三十二）を数値変換する関数
    def kans2num(self, text):
        ans = 0
        poss = 0
        for i, tmp in enumerate(self.tais2):
            pos = text.find(tmp)
            if pos == -1:
                block = 0
                pos = poss - 1
            elif  pos == poss:
                block = 1
            else:
                block = self.kans2numf(text[poss:pos])
            ans += block * (10 ** (4 * (len(self.tais2) - i)))
            poss = pos + 1
        if poss != len(text):
            ans += self.kans2numf(text[poss:len(text)])
        return ans

    # 関数(4)_文字列中の漢数字を算用数字に変換する関数（カンマ表示に簡易対応）
    def strkan2num(self, text):
        ans = ''
        tmp = ''
        for chr in text:
            if chr in self.suuji or (tmp != '' and chr == ','): # 文字が数字又はカンマの場合
                tmp += chr # 数字が続く限りtmpに格納
            else: # 文字が数字でない場合
                if tmp != '': # tmpに数字が格納されている場合
                    ans += str(self.kans2num(tmp.replace(',', ''))) #算用数字に変換して連結
                    tmp = ''
                ans += chr
        if tmp != '': # 文字列の最後が数字で終わる場合の処理
            ans += str(self.kans2num(tmp.replace(',', '')))
        return ans



if __name__ == '__main__':

    #kn = qClass_Kanji2num.qKanji2num_class()
    kn = qKanji2num_class()

    print(kn.strkan2num('平成二十三年十一月二十三日に5,000円使った'))
    print(kn.strkan2num('２０１８年１０-１２月期における日本の名目ＧＤＰは五百四十八兆七千七百二十億円、実質ＧＤＰは５３４兆３,３７０億円です'))

    print(kn.strkan2num('十八才'))
    print(kn.strkan2num('二十五才'))
    print(kn.strkan2num('F二'))


