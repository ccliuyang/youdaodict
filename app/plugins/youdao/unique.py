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

from PyQt5 import QtCore, QtDBus

DBUS_NAME = "com.youdao.dict"
DBUS_PATH = "/com/youdao/dict"
DBUS_INTERFACE = "com.youdao.dict"

session_bus = QtDBus.QDBusConnection.sessionBus()

class Interface(QtDBus.QDBusAbstractAdaptor):
    QtCore.Q_CLASSINFO("D-Bus Interface", DBUS_INTERFACE)

    def __init__(self, parent):
        QtDBus.QDBusAbstractAdaptor.__init__(self, parent)
        self.parent = parent

    @QtCore.pyqtSlot()
    def Raise(self):
        return self.parent.raise_to_top()

class UniqueService(QtCore.QObject):

    name = "service"

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.webview = None
        self.window = None
        self.assets = None

        self._interface = Interface(self)

    def enable(self, webview):
        self.webview = webview
        self.window = webview.window
        self.assets = webview.assets

    def raise_to_top(self):
        if self.window:
            self.window.show()
            self.window.activateWindow()

