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

from __future__ import print_function

import os
import sys
import traceback
import copy
from PyQt5 import QtCore

import requests
import utils
import const

from xmltodict import parse as xml_parse
from utils import open_offline_dict

def get_main_query(text):
    text = text.strip()
    with open_offline_dict() as obj:
        ret = obj.query(text)
        if ret:
            trans = ret[1].split("\\n")
            phonetic = ret[0][1:-1]
            dict_type = ret[2]
            return {"text": text, "trans": trans, "sm": phonetic, "dict_type": dict_type}
        else:
            return None

def get_suggest(text, num=10):
    text = text.strip()
    data = { "type" : "DESKDICT", "num" : num, "ver" : 2.0, "le": "eng", "q" : text, "client": const.client }
    results = []
    try:
        ret = requests.get("http://dict.youdao.com/suggest", params=data).text
        doc =  xml_parse(ret)
        _data = doc.get('suggest')
        if _data:
            data = _data['items']['item']
        else:
            data = []
        if isinstance(data, dict):
            title = data.get("title")
            explain = data.get("explain")
            if title != None and explain != None:
                results.append({"title": title, "explain": explain})
        elif isinstance(data, list):
            for item in data:
                title = item.get("title")
                explain = item.get("explain")
                if title != None and explain != None:
                    results.append({"title": title, "explain": explain})
        else:
            print("Unknown data type, debug here:", type(data))
    except Exception as e:
        print("[Error] get suggest from network:", e)
        traceback.print_exc(file=sys.stdout)
    if not results:
        with open_offline_dict() as obj:
            words = obj.suggest(text)
            for word in words:
                ret = obj.query(word)
                if ret:
                    explain = ret[1].replace("\\n", " ")
                    results.append({"title": word, "explain": explain})
    if len(results) > num:
        results = results[:num]
    return results

class SuggestModel(QtCore.QAbstractListModel):
    TitleRole = QtCore.Qt.UserRole + 1
    ExplainRole = QtCore.Qt.UserRole + 2

    _roles = { TitleRole: b"title", ExplainRole: b"explain" }

    _totalNotify = QtCore.pyqtSignal()
    suggested = QtCore.pyqtSignal(int, object)
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SuggestModel, self).__init__(parent)
        self.suggestThreadId = 0
        self.suggested.connect(self.onSuggestedData)
        self._data = []
        self._totalNotify.emit()

    def setSuggestData(self, data):
        self.beginResetModel()
        del self._data
        self._data = data
        self.endResetModel()
        self.finished.emit()
        self._totalNotify.emit()

    def resetSuggestData(self):
        self.beginResetModel()
        self.endResetModel()
        self.finished.emit()

    def addSuggestData(self, suggest):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(suggest)
        self.endInsertRows()
        self._totalNotify.emit()

    @QtCore.pyqtSlot(int, result=str)
    def getTitle(self, index):
        return self._data[index]["title"]

    @QtCore.pyqtProperty(int, notify=_totalNotify)
    def total(self):
        return len(self._data)

    def removeSuggestData(self):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.pop()
        self.endInsertRows()
        self._totalNotify.emit()

    def roleNames(self):
        return self._roles

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def data(self, index, role):

        if not index.isValid() or index.row() > len(self._data):
            return QtCore.QVariant()

        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()

        if role == self.TitleRole:
            return item.get("title", "")
        elif role == self.ExplainRole:
            return item.get("explain", "")
        return QtCore.QVariant()

    def parseSuggested(self, data):
        if data is not None:
            self.setSuggestData(data)
        else:
            self.resetSuggestData()

    def emitSuggestResult(self, data, threadId):
        if threadId == self.suggestThreadId:
            self.suggested.emit(threadId, data)

    def onSuggestedData(self, threadId, data):
        if threadId == self.suggestThreadId:
            self.parseSuggested(data)

    def asyncSuggest(self, suggestFunc, args):
        self.suggestThreadId += 1
        thread_id = copy.deepcopy(self.suggestThreadId)
        utils.ThreadFetch(
            fetch_funcs=(suggestFunc, args),
            success_funcs=(self.emitSuggestResult, (thread_id,))).start()

    @QtCore.pyqtSlot(str)
    def suggest(self, text):
        self.asyncSuggest(get_suggest, (text,))

    @QtCore.pyqtSlot(str)
    @QtCore.pyqtSlot(str, int)
    def suggestWithNum(self, text, num=10):
        self.asyncSuggest(get_suggest, (text, num))

suggestModel = SuggestModel()

class KeyDict(dict):

    def __eq__(self, other):
        try:
            return self.owner == other.owner
        except:
            return False

    @property
    def owner(self):
        return self.get("title")

    def __cmp__(self, other):
        try:
            return cmp(self.owner, other.owner)
        except:
            return -1

class HistoryModel(QtCore.QAbstractListModel):
    TitleRole = QtCore.Qt.UserRole + 1
    ExplainRole = QtCore.Qt.UserRole + 2

    _roles = { TitleRole: b"title", ExplainRole: b"explain" }
    finished = QtCore.pyqtSignal()
    MAX_NUM = 10

    _currentPageNotify = QtCore.pyqtSignal()
    _totalPageNotify = QtCore.pyqtSignal()
    _countNotify = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(HistoryModel, self).__init__(parent)
        self._all_data = []
        self._current_page = 1
        self._total_page = 1

        self._db = utils.get_cache_file("history.db")
        self._data = []
        self.load_all_data()

    def load_all_data(self):
        objs = utils.load_db(self._db)
        if objs:
            self._all_data = objs
        self._total_page = self.get_total_page()
        self.reload_data()

    def reload_data(self):
        start_index = self.MAX_NUM * (self._current_page - 1)
        if len(self._all_data) > start_index + self.MAX_NUM:
            self._data = self._all_data[start_index:start_index+self.MAX_NUM]
        else:
            self._data = self._all_data[start_index:]

    @QtCore.pyqtProperty(int, notify=_countNotify)
    def count(self):
        return len(self._all_data)

    @QtCore.pyqtProperty(int, notify=_currentPageNotify)
    def currentPage(self):
        return self._current_page

    @currentPage.setter
    def currentPage(self, new_page):
        if self._current_page != new_page:
            if new_page <= self._total_page and new_page > 0:
                self._current_page = new_page
                self._currentPageNotify.emit()
                self.reload_model()

    def get_total_page(self):
        total_index = len(self._all_data) - 1
        return int(total_index/self.MAX_NUM) + 1

    def update_total_page(self):
        new_total_page = self.get_total_page()
        if new_total_page != self._total_page:
            self._total_page = new_total_page
            self._totalPageNotify.emit()

    @QtCore.pyqtProperty(int, notify=_totalPageNotify)
    def totalPage(self):
        return self._total_page

    @QtCore.pyqtSlot()
    def save(self):
        if self._all_data:
            utils.save_db(self._all_data, self._db)

    def resetHistoryData(self):
        self.beginResetModel()
        self.endResetModel()
        self.finished.emit()

    def reload_model(self):
        self.reload_data()
        self.resetHistoryData()

    @QtCore.pyqtSlot(str, str, str)
    def addSearchData(self, title, explain, web):
        title = title.strip()
        explain = explain.split("<br>")[0]
        if not explain:
            explain = web

        explain = explain.split("\n")[0]

        kd = KeyDict(title=title, explain=explain)
        change = False
        if kd in self._all_data:
            idx = self._all_data.index(kd)
            if idx != 0:
                self._all_data.pop(idx)
                self._all_data.insert(0, kd)
                change = True
        else:
            self._all_data.insert(0, kd)
            self._countNotify.emit()
            change = True

        if change:
            self.currentPage = 1
            self.reload_model()
            self.update_total_page()
            self.save()

    @QtCore.pyqtSlot()
    def clearAllData(self):
        self._all_data = []
        self._countNotify.emit()
        self.currentPage = 1
        self.update_total_page()
        self.save()
        self.reload_model()

    # overridden
    def roleNames(self):
        return self._roles

    # overridden
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[:self.MAX_NUM])

    # overridden
    def data(self, index, role):

        if not index.isValid() or index.row() > len(self._data):
            return QtCore.QVariant()

        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()

        if role == self.TitleRole:
            return item.get("title", "")
        elif role == self.ExplainRole:
            return item.get("explain", "")
        return QtCore.QVariant()

historyModel = HistoryModel()
