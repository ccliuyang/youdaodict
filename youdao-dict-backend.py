#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2015 Deepin, Inc.
#               2011~2015 Kaisheng Ye
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

import os
import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt5 import QtDBus, QtWidgets, QtCore
if os.name == 'posix':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)

from backend.backend import DBUS_NAME, DBUS_PATH, GetWord

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    session_bus = QtDBus.QDBusConnection.sessionBus()
    if not session_bus.registerService(DBUS_NAME):
        print("Service is running: %s" % DBUS_NAME)
        sys.exit(0)

    get_word = GetWord()
    session_bus.registerObject(DBUS_PATH, get_word)
    print("Youdao Backend Service is started...")

    sys.exit(app.exec_())
