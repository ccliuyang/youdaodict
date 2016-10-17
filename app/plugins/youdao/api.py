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
import requests

import webbrowser
from PyQt5.QtCore import QObject, pyqtSlot, QVariant, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import qApp

from config import setting_config
from window import LogoWindow, MiniWindow, OcrResultWindow, AboutWindow, TrayIconMenu
from setting_dialog import SettingDialog
from dbus_proxy import GetwordDaemon
from models import get_suggest, get_main_query

import const

vendor = 'deskdict'
appId = "YoudaoDict"

class ExternalApi(QObject):
    name = "api"

    onlimitHistory = pyqtSignal(QVariant)
    onsetUserDict = pyqtSignal(QVariant)
    onchangeCurClick = pyqtSignal(QVariant)
    onlangChange = pyqtSignal(QVariant)
    onwordStrokeStateChange = pyqtSignal(QVariant)
    onscreenTransStateChange = pyqtSignal(QVariant)
    ontopMost = pyqtSignal(QVariant)
    onfanyiQuery = pyqtSignal(QVariant)
    ondictQuery = pyqtSignal(QVariant)
    onnetStateChange = pyqtSignal(QVariant)

    onSplashTimeout = pyqtSignal()

    _ocrEnableNotify = pyqtSignal()
    _strokeEnableNotify = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self._media_player = None
        self._clipboard = None

        self.getword_daemon = GetwordDaemon()
        self.getword_daemon.keyReleased.connect(self.handle_getword_daemon_key_released)

        self._logo_window = LogoWindow(self.getword_daemon, setting_config, self)
        self._mini_window = MiniWindow(self.getword_daemon, setting_config, self)
        self._ocr_result_window = OcrResultWindow(self.getword_daemon, setting_config, self)
        self._trayicon_menu = TrayIconMenu(self.getword_daemon, self)

        setting_config.hasSaved.connect(self.handle_setting_dialog_saved)

        self._main_window = None
        self._sub_windows = []

    def handle_getword_daemon_key_released(self, keyname):
        if keyname == "F8":
            self.setOcrEnable(not self.ocrEnabled)

    def handle_setting_dialog_saved(self, change_options):
        for option in change_options:
            section, key = option

            if section == "getword":
                if key == "ocr" or key == "ocr_mode":
                    self.initOcrState()
                elif key == "stroke" or key == "stroke_mode":
                    self.initStrokeState()

            elif section == "basic_option":
                if key == "main_window_topmost":
                    self.initTopMost()

    def enable(self, webview):
        window = webview.window
        if window.parent:
            self._sub_windows.append(window)
        else:
            self._main_window = window

    def set_getword_config(self, key, value):
        setting_config.set_getword(key, value)
        if key == "ocr":
            mode = setting_config.get_getword("ocr_mode")
            self.onscreenTransStateChange.emit([value, mode])
        elif key == "stroke":
            mode = setting_config.get_getword("stroke_mode")
            self.onwordStrokeStateChange.emit([value, mode])

    def initStrokeState(self):
        enable = setting_config.get_getword("stroke")
        mode = setting_config.get_getword("stroke_mode")
        self.getword_daemon.SetStrokeEnable(enable)
        self._strokeEnableNotify.emit()
        self.onwordStrokeStateChange.emit([enable, mode])

    def initOcrState(self):
        enable = setting_config.get_getword("ocr")
        mode = setting_config.get_getword("ocr_mode")
        self.getword_daemon.SetOcrEnable(enable)
        self._ocrEnableNotify.emit()
        self.onscreenTransStateChange.emit([enable, mode])

    @pyqtSlot(result=str)
    def getSelectText(self):
        if not self._clipboard:
            self._clipboard = qApp.clipboard()
        return self._clipboard.text(mode=QClipboard.Selection)

    @pyqtSlot()
    def clearSelectText(self):
        if not self._clipboard:
            self._clipboard = qApp.clipboard()
        text = self._clipboard.text(mode=QClipboard.Selection)
        if text.strip() != "":
            self._clipboard.clear(mode=QClipboard.Selection)

    @pyqtSlot(str, str, str, result=str)
    def fanyi(self, keyword, keyfrom, lang):
        url = "http://fanyi.youdao.com/translate?dogVersion=1.0&ue=utf8"
        url += "&doctype=json&xmlVersion=1.6&client=%s&id=92dc50aa4970fb72d" % const.client
        url += "&vendor=YoudaoDict&in=YoudaoDict&appVer=1.0.3&appZengqiang=0"
        url += "&abTest=5&smartresult=dict&smartresult=rule"
        url += "&i=" + keyword
        url += "&keyfrom=" + keyfrom
        url += "&type=" + lang
        try:
            return requests.get(url).text
        except:
            return ""

    @pyqtSlot(bool)
    def emitNetStateChange(self, state):
        self.onnetStateChange.emit([state])

    @pyqtSlot()
    def clear_action(self):
        self.getword_daemon.ClearStroke()

    @pyqtSlot()
    def startInitState(self):
        self.initOcrState()
        self.initStrokeState()

    @pyqtSlot()
    def initTopMost(self):
        state = setting_config.get_basic_option("main_window_topmost")
        self.emitTopMost(state)

    @pyqtSlot(bool)
    def setOcrEnable(self, value):
        self.getword_daemon.SetOcrEnable(value)
        self.set_getword_config("ocr", value)
        self._ocrEnableNotify.emit()

    @pyqtSlot(result=bool)
    def getOcrEnable(self):
        return self.getword_daemon.GetOcrEnable()

    @pyqtProperty(bool, notify=_ocrEnableNotify)
    def ocrEnabled(self):
        enable = setting_config.get_getword("ocr")
        return enable

    @pyqtSlot(bool)
    def setStrokeEnable(self, value):
        self.getword_daemon.SetStrokeEnable(value)
        self.set_getword_config("stroke", value)
        self._strokeEnableNotify.emit()

    @pyqtSlot(result=bool)
    def getStrokeEnable(self):
        return self.getword_daemon.GetStrokeEnable()

    @pyqtProperty(bool, notify=_strokeEnableNotify)
    def strokeEnabled(self):
        enable = setting_config.get_getword("stroke")
        return enable

    @pyqtSlot()
    def getwordQuit(self):
        print("getword daemon exit...")
        self.getword_daemon.Quit()

    @pyqtSlot(bool)
    def emitTopMost(self, new_state):
        self.ontopMost.emit([new_state])

    @pyqtSlot(str, str)
    def emitDictQuery(self, text, lang):
        param = [text, lang]
        self.ondictQuery.emit(param)

    '''
        implemented api for externalAPI in business.js
    '''

    @pyqtSlot()
    def toggleTopMost(self):
        state = setting_config.get_basic_option("main_window_topmost")
        self.emitTopMost(not state)

    @pyqtSlot()
    def strokeTrans(self):
        self.setStrokeEnable(not self.strokeEnabled)

    @pyqtSlot()
    def screenTrans(self):
        self.setOcrEnable(not self.ocrEnabled)

    @pyqtSlot()
    def openZFanyi(self):
        webbrowser.open("http://f.youdao.com/?vendor=%s&client=%s" % (vendor, const.client))

    @pyqtSlot()
    def openPictDict(self):
        if self._main_window and self._main_window.assets:
            if not hasattr(self, "_pict_dict_window"):
                app_dir = self._main_window.assets.manifest["app_dir"]
                pictDictIndexPath = "file://" + os.path.join(app_dir, "assets/pic/picdict.html")
                self._pict_dict_window = self._main_window.api.createWindow(pictDictIndexPath, 900, 680)
            self._pict_dict_window.show()

    @pyqtSlot()
    def openStudy(self):
        webbrowser.open("http://xue.youdao.com/?keyfrom=%s&client=%s" % (vendor, const.client))

    @pyqtSlot()
    def openBbs(self):
        webbrowser.open("http://dg.youdao.com/")

    @pyqtSlot()
    def openMini(self):
        self._mini_window.show()
        self._mini_window.recordCurrentVisible("true")
        if self._main_window and self._mini_window not in self._main_window.assets.windows:
            self._main_window.assets.windows.append(self._mini_window)

    @pyqtSlot()
    def changeFrameAdv(self):
        pass

    @pyqtSlot(QVariant)
    def langChange(self, lang):
        print("langChange:", lang)

    @pyqtSlot(result=str)
    def getAppID(self):
        return appId

    @pyqtSlot(result=str)
    def getVendor(self):
        return vendor

    @pyqtSlot(result=str)
    def getAppVersionString(self):
        return self._main_window.assets.manifest["version"]

    @pyqtSlot()
    @pyqtSlot(int)
    def option(self, index=0):
        if not hasattr(self, "_setting_window") or not self._setting_window:
            self._setting_window = SettingDialog(setting_config)
            self._setting_window.setWindowIcon(self._main_window.windowIcon())
        self._setting_window.reload_settings()
        self._setting_window.setCurrentIndex(index)
        self._setting_window.show()

    @pyqtSlot()
    def aboutDlg(self):
        if not hasattr(self, "_about_dialog") or not self._about_dialog:
            self._about_dialog = AboutWindow()
            self._about_dialog.setIcon(self._main_window.windowIcon())
        self._about_dialog.showCenter()

    @pyqtSlot()
    def quit(self):
        if self._main_window:
            self._main_window.quit()

    @pyqtSlot(str)
    def copyText(self, text):
        from PyQt5.QtGui import QGuiApplication
        clip = QGuiApplication.clipboard()
        clip.setText(text)

    @pyqtSlot()
    def showTrayIconMenu(self):
        self._trayicon_menu.showAtCursor()

    @pyqtSlot()
    def showMainWindow(self):
        self._main_window.show()
        self._main_window.activate()

    @pyqtSlot(str, result=QVariant)
    @pyqtSlot(str, int, result=QVariant)
    def getSuggest(self, text, num=10):
        return get_suggest(text, num)

    @pyqtSlot(str, result=QVariant)
    def getMainQuery(self, text):
        return get_main_query(text)

    @pyqtSlot(str)
    def playSound(self, url):
        self.getword_daemon.PlaySound(url)

    @pyqtSlot()
    def stopSound(self):
        self.getword_daemon.StopSound()

if __name__ == '__main__':
    import sys
    import signal
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    if os.name == 'posix':
        QApplication.setAttribute(Qt.AA_X11InitThreads, True)

    app = QApplication(sys.argv)
    obj = ExternalApi()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
