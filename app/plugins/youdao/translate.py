#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2014 Deepin, Inc.
#               2011~2014 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

from pyquery import PyQuery
from PyQt5 import QtCore
import json
import time

from auto_object import AutoQObject
from utils import threaded, open_offline_dict
from tts import get_voice_simple
import const

#@ 使用google翻译
def useTranslateComponent(text):
    import translate

    # import sys
    # import locale
    # from_lang = 'en'
    # to_lang = 'zh'
    # translator = translate.Translator(from_lang,to_lang)
    # translation = translator.translate(text)
    # if sys.version_info.major == 2:
    #     translation =translation.encode(locale.getpreferredencoding())
    # return translation
    import os
    from dae.utils import get_conf
    conf = get_conf()
    toLang = conf['toLang']
    # translation = os.popen(cmd + " '" + text + "'").readlines()[0]
    from mtranslate import translate
    translation = translate(text,toLang)
    return translation

class YoudaoTranslate(QtCore.QObject):

    translateFinished = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)

        TranslateInfo = AutoQObject(
            ("text", str),
            ("phonetic", str),
            ("voices", 'QVariant'),
            ("webtrans", str),
            ("trans", str),
            ("weba", str),
            ("lang", str),
            name="TranslateInfo")
        self.translate_info = TranslateInfo()




    def wrap_web_trans(self, pq):
        tran_lines = [PyQuery(e).text() for e in pq.find('web-translation:first')('trans value')]

        result_lines = [""]
        for tran_line in tran_lines:
            current_line = result_lines[-1]
            if len(current_line) + len(tran_line) > 30:
                result_lines.append(tran_line)
            else:
                result_lines[-1] += tran_line + "; "

        for (index, result_line) in enumerate(result_lines):
            result_lines[index] = "w. " + result_lines[index]

        return '\n'.join(result_lines)

    @threaded
    @QtCore.pyqtSlot(str)
    def get_translate(self, text):
        # with open('/home/ubuntu/Desktop/translate.txt', 'a') as f:
        #         f.write('\ntext :'+ text + '\n' + 'translate: ' + self.translate_info.webtrans)
        #         f.close()
        # text = text.strip()
        # if not text:
        #     return
        #
        data = { "keyfrom" : "deskdict.linux", "q" : text.encode("utf-8"), "doctype" : "xml", "xmlVersion" : 8.2,
                 "client" : const.client, "id" : "cee84504d9984f1b2", "vendor": "deskdict.linux",
                 "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
        self.clear_translate()
        try:
            ret = requests.get("http://dict.youdao.com/search", params=data).text
            ret = ret.encode('utf-8')
            pq = PyQuery(ret, parser="xml")
            test_data = {"q": text, "type": 1, "pos": -1, "client": const.client}
            test_ret = json.loads(requests.get("http://dict.youdao.com/jsonresult", params=test_data).text)

            self.translate_info.text = text
            text = str(text).replace('\n',' ')
            from dae.utils import get_conf
            conf = get_conf()
            self.translate_info.webtrans = "谷歌翻译: \n"

            if (str(conf['useTranslateModule']).upper() == 'TRUE' ):
                self.translate_info.webtrans = self.translate_info.webtrans + useTranslateComponent(text) + "\n"
            # if self.translate_info.webtrans:
            self.translate_info.webtrans =self.translate_info.webtrans + "有道:\n"
            self.translate_info.trans = '\n'.join([PyQuery(l)("i").text() for l in pq('trs l')])
            self.translate_info.phonetic = test_ret.get("ussm", "")
            self.translate_info.webtrans = self.translate_info.webtrans + self.wrap_web_trans(pq)
        except:
            with open_offline_dict() as obj:
                ret = obj.query(text)
                if ret:
                    self.translate_info.text = text
                    self.translate_info.trans = ret[1].replace("\\n", "\n")
                    self.translate_info.phonetic = ret[0][1:-1]
                    self.translate_info.webtrans = "抱歉，从网络获取结果失败，请检测网络重试"
                    self.translate_info.lang = "eng"
        self.translate_info.voices = get_voice_simple(text)

        if not self.translate_info.webtrans:
            self.translate_info.webtrans = "查询失败"
        # time.sleep(1)
        if self.translate_info.webtrans:
            self.translateFinished.emit()


    @QtCore.pyqtSlot()
    def clear_translate(self):
        self.translate_info.text = ""
        self.translate_info.trans = None
        self.translate_info.webtrans = None
        self.translate_info.voice = None
        self.translate_info.phonetic = ""

