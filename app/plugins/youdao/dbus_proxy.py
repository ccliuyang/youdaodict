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

from PyQt5 import QtCore
from PyQt5.QtDBus import QDBusInterface, QDBusConnection

class GetwordDaemon(QtCore.QObject):

    DBUS_NAME = "com.youdao.backend"
    DBUS_PATH = "/com/youdao/backend"
    DBUS_IFACE = "com.youdao.backend"

    hide = QtCore.pyqtSignal()
    ocrRecognized = QtCore.pyqtSignal(int, int, str, arguments=['x', 'y', 'text'])
    strokeRecognized = QtCore.pyqtSignal(int, int, str, arguments=['x', 'y', 'text'])
    ocrEnableChanged = QtCore.pyqtSignal(bool, arguments=['enabled'])
    strokeEnableChanged = QtCore.pyqtSignal(bool, arguments=['enabled'])
    cursorPositionChanged = QtCore.pyqtSignal(int, int, arguments=['x', 'y'])

    doubleCtrlReleased = QtCore.pyqtSignal()
    altPressed = QtCore.pyqtSignal()
    ctrlPressed = QtCore.pyqtSignal()
    shiftPressed = QtCore.pyqtSignal()
    altReleased = QtCore.pyqtSignal()
    ctrlReleased = QtCore.pyqtSignal()
    shiftReleased = QtCore.pyqtSignal()

    keyPressed = QtCore.pyqtSignal(str, arguments=["name"])
    keyReleased = QtCore.pyqtSignal(str, arguments=["name"])

    wheelKeyReleased = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.session_bus = QDBusConnection.sessionBus()
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'hide', self.hideSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'ocrRecognized', self.ocrRecognizedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'strokeRecognized', self.strokeRecognizedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'ocrEnableChanged', self.ocrEnableChangedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'strokeEnableChanged', self.strokeEnableChangedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'cursorPositionChanged', self.cursorPositionChangedSlot)

        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'doubleCtrlReleased', self.doubleCtrlReleasedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'altPressed', self.altPressedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'ctrlPressed', self.ctrlPressedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'shiftPressed', self.shiftPressedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'altReleased', self.altReleasedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'ctrlReleased', self.ctrlReleasedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'shiftReleased', self.shiftReleasedSlot)

        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'keyPressed', self.keyPressedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'keyReleased', self.keyReleasedSlot)

        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'wheelKeyReleased', self.wheelKeyReleasedSlot)

        self.getword_iface = QDBusInterface(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE, self.session_bus)

    # signal slot
    @QtCore.pyqtSlot()
    def hideSlot(self):
        self.hide.emit()

    @QtCore.pyqtSlot()
    def doubleCtrlReleasedSlot(self):
        self.doubleCtrlReleased.emit()

    @QtCore.pyqtSlot()
    def altPressedSlot(self):
        self.altPressed.emit()

    @QtCore.pyqtSlot()
    def altReleasedSlot(self):
        self.altReleased.emit()

    @QtCore.pyqtSlot()
    def ctrlPressedSlot(self):
        self.ctrlPressed.emit()

    @QtCore.pyqtSlot()
    def ctrlReleasedSlot(self):
        self.ctrlReleased.emit()

    @QtCore.pyqtSlot()
    def shiftPressedSlot(self):
        self.shiftPressed.emit()

    @QtCore.pyqtSlot()
    def shiftReleasedSlot(self):
        self.shiftReleased.emit()

    @QtCore.pyqtSlot(str)
    def keyPressedSlot(self, name):
        self.keyPressed.emit(name)

    @QtCore.pyqtSlot(str)
    def keyReleasedSlot(self, name):
        self.keyReleased.emit(name)

    @QtCore.pyqtSlot()
    def wheelKeyReleasedSlot(self):
        self.wheelKeyReleased.emit()

    @QtCore.pyqtSlot(int, int, str)
    def ocrRecognizedSlot(self, x, y, text):
        self.ocrRecognized.emit(x, y, text)

    @QtCore.pyqtSlot(int, int, str)
    def strokeRecognizedSlot(self, x, y, text):
        self.strokeRecognized.emit(x, y, text)

    @QtCore.pyqtSlot(bool)
    def ocrEnableChangedSlot(self, enable):
        self.ocrEnableChanged.emit(enable)

    @QtCore.pyqtSlot(bool)
    def strokeEnableChangedSlot(self, enable):
        self.strokeEnableChanged.emit(enable)

    @QtCore.pyqtSlot(int, int)
    def cursorPositionChangedSlot(self, x, y):
        self.cursorPositionChanged.emit(x, y)

    # method wrap
    @QtCore.pyqtSlot(str)
    def PlaySound(self, url):
        self.getword_iface.call("PlaySound", url)

    @QtCore.pyqtSlot()
    def StopSound(self):
        self.getword_iface.call("StopSound")

    @QtCore.pyqtSlot()
    def ClearStroke(self):
        self.getword_iface.call("ClearStroke")

    @QtCore.pyqtSlot(bool)
    def SetOcrEnable(self, value):
        self.getword_iface.call("SetOcrEnable", value)

    @QtCore.pyqtSlot(result=bool)
    def GetOcrEnable(self):
        return self.getword_iface.call("GetOcrEnable").arguments()[0]

    @QtCore.pyqtSlot(bool)
    def SetStrokeEnable(self, value):
        self.getword_iface.call("SetStrokeEnable", value)

    @QtCore.pyqtSlot(result=bool)
    def GetStrokeEnable(self):
        return self.getword_iface.call("GetStrokeEnable").arguments()[0]

    @QtCore.pyqtSlot(int, int)
    def EmitOcr(self, x, y):
        self.getword_iface.call("EmitOcr", x, y)

    @QtCore.pyqtSlot()
    def Quit(self):
        self.getword_iface.call("Quit")

class YoudaoIndicator(QtCore.QObject):

    DBUS_NAME = "com.youdao.indicator"
    DBUS_PATH = "/com/youdao/indicator"
    DBUS_IFACE = "com.youdao.indicator"

    onMenuItemClicked = QtCore.pyqtSignal(str)
    onCheckMenuItemClicked = QtCore.pyqtSignal(str, bool)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.session_bus = QDBusConnection.sessionBus()
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'MenuItemClicked', self.MenuItemClickedSlot)
        self.session_bus.connect(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE,
            'CheckMenuItemClicked', self.CheckMenuItemClickedSlot)

        self._iface = QDBusInterface(self.DBUS_NAME, self.DBUS_PATH, self.DBUS_IFACE, self.session_bus)

    @QtCore.pyqtSlot(result=bool)
    def isExists(self):
        self._iface.call("Hello")
        return not self._iface.lastError().isValid()

    @QtCore.pyqtSlot(str)
    def MenuItemClickedSlot(self, menu_id):
        self.onMenuItemClicked.emit(menu_id)

    @QtCore.pyqtSlot(str, bool)
    def CheckMenuItemClickedSlot(self, menu_id, enable):
        self.onCheckMenuItemClicked.emit(menu_id, enable)

    @QtCore.pyqtSlot(bool)
    def SetOcrEnable(self, enable):
        self._iface.call("SetOcrEnable", enable)

    @QtCore.pyqtSlot(bool)
    def SetStrokeEnable(self, enable):
        self._iface.call("SetStrokeEnable", enable)

    @QtCore.pyqtSlot()
    def Quit(self):
        self._iface.call("Quit")

