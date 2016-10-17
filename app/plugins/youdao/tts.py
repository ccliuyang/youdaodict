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

import sys
import traceback
import requests
from pyquery import PyQuery
from urllib.parse import urlencode
import const

VOICE_UK = 1
VOICE_US = 2

def get_voice_type(text):
    voice_type = VOICE_US

    data = { "keyfrom" : "deskdict.linux", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
             "client" : const.client, "id" : "cee84504d9984f1b2", "vendor": "deskdict.linux",
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
    try:
        ret = requests.get("http://dict.youdao.com/search", params=data).text
        ret = ret.encode('utf-8')
        pq = PyQuery(ret, parser="xml")
        if pq.find('usphone').text() == None:
            voice_type = VOICE_UK
    except Exception as e:
        print("[Error] get_voice_type:", e)
        traceback.print_exc(file=sys.stdout)

    return voice_type

def get_voice_simple(text):
    url = "http://dict.youdao.com/dictvoice"
    data = { "keyfrom" : "deskdict.linux", "audio" : text, "client" : const.client, "id" : "cee84504d9984f1b2", "vendor": "deskdict.linux",
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "type" : get_voice_type(text)}
    return ["%s?%s" % (url, urlencode(data))]

def get_phonetic_symbol(text):
    phonetic_type = "US"
    phonetic_symbol = ""
    data = { "keyfrom" : "deskdict.linux", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
             "client" : const.client, "id" : "cee84504d9984f1b2", "vendor": "deskdict.linux",
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
    try:
        ret = requests.get("http://dict.youdao.com/search", params=data).text
        ret = ret.encode('utf-8')
        pq = PyQuery(ret, parser="xml")
        phonetic_symbol = pq.find('usphone').text()
        if phonetic_symbol == '':
            phonetic_symbol = pq.find('ukphone').text()
            phonetic_type = "UK"
    except Exception as e:
        print("[Error] get_phonetic_symbol:", e)
        traceback.print_exc(file=sys.stdout)

    return (phonetic_type, phonetic_symbol)
