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
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtDBus
from PyQt5 import QtWidgets

from dbus_proxy import YoudaoIndicator
from window import SplashWindow
from api import ExternalApi
from config import setting_config
from unique import UniqueService, session_bus, DBUS_NAME, DBUS_PATH, DBUS_INTERFACE
import sys

def export_objects():
    app = QtWidgets.qApp
    app.setApplicationVersion("0.4.1")
    app.setOrganizationName("Youdao")
    app.setApplicationName("Youdao Dict")

    # set default font
    defaultFont = QtGui.QFont()
    defaultFont.setPointSize(11)
    app.setFont(defaultFont)

    if not session_bus.registerService(DBUS_NAME):
        print("Service is running: %s" % DBUS_NAME)
        iface = QtDBus.QDBusInterface(DBUS_NAME, DBUS_PATH, DBUS_INTERFACE, session_bus)
        iface.call("Raise")
        sys.exit(0)
    else:
        unique_obj = UniqueService()
        session_bus.registerObject(DBUS_PATH, unique_obj)
        print("Youdao Dict Unique Service is started...")
        youdao_api = ExternalApi()
        splash_window = SplashWindow(youdao_api)
        if not "--autostart" in sys.argv and not setting_config.get_basic_option("start_mini"):
            splash_window.showCenter()
            splash_window.startTimer()
        indicator = YoudaoIndicator()
        return [
                dict(name=unique_obj.name, obj=unique_obj),
                dict(name="indicator", obj=indicator),
                dict(name="splash_window", obj=splash_window),
                dict(name=youdao_api.name, obj=youdao_api),
                dict(name="config", obj=setting_config),
               ]
