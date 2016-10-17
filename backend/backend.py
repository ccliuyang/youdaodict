#!/usr/bin/env python3
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

from PyQt5 import QtDBus, QtCore, QtMultimedia
from PyQt5.QtWidgets import qApp as app

from .event import EventHandler, EventRecord
from .tesseract import OcrWord
from .utils import threaded

DBUS_NAME = "com.youdao.backend"
DBUS_PATH = "/com/youdao/backend"
DBUS_INTERFACE = "com.youdao.backend"

ocr_support_languages = ["en", "zh-CN", "zh-TW"]

class GetWordInterface(QtDBus.QDBusAbstractAdaptor):
    QtCore.Q_CLASSINFO("D-Bus Interface", DBUS_INTERFACE)

    hide = QtCore.pyqtSignal()
    ocrRecognized = QtCore.pyqtSignal(int, int, str)
    strokeRecognized = QtCore.pyqtSignal(int, int, str)
    ocrEnableChanged = QtCore.pyqtSignal(bool)
    strokeEnableChanged = QtCore.pyqtSignal(bool)

    cursorPositionChanged = QtCore.pyqtSignal(int, int)

    doubleCtrlReleased = QtCore.pyqtSignal()
    altPressed = QtCore.pyqtSignal()
    ctrlPressed = QtCore.pyqtSignal()
    shiftPressed = QtCore.pyqtSignal()
    altReleased = QtCore.pyqtSignal()
    ctrlReleased = QtCore.pyqtSignal()
    shiftReleased = QtCore.pyqtSignal()

    keyPressed = QtCore.pyqtSignal(str)
    keyReleased = QtCore.pyqtSignal(str)

    wheelKeyReleased = QtCore.pyqtSignal()

    def __init__(self, parent):
        QtDBus.QDBusAbstractAdaptor.__init__(self, parent)
        self.parent = parent
        self.parent.onOcrFinished.connect(self.ocrRecognized)

        self._media_player = QtMultimedia.QMediaPlayer()

    def setEnable(self, key, value):
        if self.getEnable(key) != value:
            self.parent.setEnable(key, value)
            if key == "ocr":
                self.ocrEnableChanged.emit(value)
            elif key == "stroke":
                self.strokeEnableChanged.emit(value)

    def getEnable(self, key):
        return self.parent.getEnable(key)

    @QtCore.pyqtSlot(str)
    def PlaySound(self, url):
        media_url = QtCore.QUrl(url)
        media_content = QtMultimedia.QMediaContent(media_url)
        self._media_player.setMedia(media_content)
        self._media_player.play()

    @QtCore.pyqtSlot()
    def StopSound(self):
        if self._media_player:
            self._media_player.stop()

    @QtCore.pyqtSlot()
    def ClearStroke(self):
        self.parent._event_handler.clear_clipbaoard()

    @QtCore.pyqtSlot(bool)
    def SetOcrEnable(self, value):
        self.setEnable("ocr", value)

    @QtCore.pyqtSlot(result=bool)
    def GetOcrEnable(self):
        return self.getEnable("ocr")

    @QtCore.pyqtSlot(bool)
    def SetStrokeEnable(self, value):
        self.setEnable("stroke", value)

    @QtCore.pyqtSlot(result=bool)
    def GetStrokeEnable(self):
        return self.getEnable("stroke")

    @QtCore.pyqtSlot(int, int)
    def EmitOcr(self, x, y):
        self.parent.ocrHandler(x, y)

    @QtCore.pyqtSlot()
    def Quit(self):
        self.parent.quit()

class GetWord(QtCore.QObject):

    onOcrFinished = QtCore.pyqtSignal(int, int, str)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._interface = GetWordInterface(self)

        self._event_handler = EventHandler(app.clipboard())
        self._event_handler.translate_selection.connect(self.strokeWorkHandler)

        self._event_handler.esc_pressed.connect(self.hideHandler)
        self._event_handler.wheel_press.connect(self.hideHandler)
        self._event_handler.left_button_press.connect(self.hideHandler)
        self._event_handler.right_button_press.connect(self.hideHandler)

        self._event_handler.double_ctrl_released.connect(self._interface.doubleCtrlReleased)
        self._event_handler.alt_pressed.connect(self._interface.altPressed)
        self._event_handler.ctrl_pressed.connect(self._interface.ctrlPressed)
        self._event_handler.shift_pressed.connect(self._interface.shiftPressed)
        self._event_handler.alt_released.connect(self._interface.altReleased)
        self._event_handler.ctrl_released.connect(self._interface.ctrlReleased)
        self._event_handler.shift_released.connect(self._interface.shiftReleased)

        self._event_handler.key_pressed.connect(self._interface.keyPressed)
        self._event_handler.key_released.connect(self._interface.keyReleased)

        self._event_handler.wheel_key_released.connect(self._interface.wheelKeyReleased)

        self._event_handler.cursorPositionChanged.connect(self._interface.cursorPositionChanged)

        self._event_record = EventRecord()
        self._event_record.capture_event.connect(self._event_handler.handle_event)
        self._event_record.start()

        self._stroke_enable = True
        self._ocr_enable = True
        self._ocr_word = OcrWord(app)

    @threaded
    def ocr_word_thread(self, x, y):
        for lang in ocr_support_languages:
            text = self._ocr_word.recognize(x, y, lang)
            if text:
                self.onOcrFinished.emit(x, y, text)
                return

    def ocrHandler(self, x, y):
        if self._ocr_enable:
            self.ocr_word_thread(x, y)

    def strokeWorkHandler(self, x, y, text):
        if self._stroke_enable:
            self._interface.strokeRecognized.emit(x, y, text)

    def hideHandler(self):
        self._interface.hide.emit()

    def setEnable(self, key, value):
        if key == "ocr":
            self._ocr_enable = value
        elif key == "stroke":
            self._stroke_enable = value

        self._event_handler._enable = self._ocr_enable and self._stroke_enable

    def getEnable(self, key):
        if key == "ocr":
            return self._ocr_enable
        elif key == "stroke":
            return self._stroke_enable

    def quit(self):
        app.quit()

