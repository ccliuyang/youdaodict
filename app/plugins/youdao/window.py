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
from PyQt5 import QtCore, QtQuick, QtWidgets, QtGui

from utils import get_parent_dir
from models import suggestModel, historyModel

from translate import YoudaoTranslate

class Window(QtQuick.QQuickView):

    _focusWindowNotify = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtQuick.QQuickView.__init__(self, parent)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)

        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)

        self.qml_context = self.rootContext()
        self.qml_context.setContextProperty("mainView", self)
        self.root_object = self.rootObject()
        #@ 单词保存到文件
        self.saveToFile = saveToFile()
        self.qml_context.setContextProperty("saveToFile", self.saveToFile)

        self._staysOnTop = False
        self._isFocusWindow = False

        QtWidgets.qApp.focusWindowChanged.connect(self.window_focus_changed_handler)



    def window_focus_changed_handler(self, win):
        self._isFocusWindow = win == self
        self._focusWindowNotify.emit()

    def load_qml(self, filename):
        qml_path = os.path.join(get_parent_dir(__file__), "qml", filename)
        self.setSource(QtCore.QUrl(qml_path))

    @QtCore.pyqtSlot(result=bool)
    def in_translate_area(self):
        pos = self.getCursorPos()
        mouse_x = pos.x()
        mouse_y = pos.y()
        return self.x() < mouse_x < self.x() + self.width() and self.y() < mouse_y < self.y() + self.height()

    @QtCore.pyqtSlot()
    def hideHandler(self):
        if self.isVisible() and not self.in_translate_area():
            self.hide()

    @QtCore.pyqtSlot()
    def showScreenCenter(self):
        screen = QtWidgets.qApp.primaryScreen()
        geometry = screen.availableGeometry()
        self.setX(geometry.x() + (geometry.width() - self.width())/2)
        self.setY(geometry.y() + (geometry.height() - self.height())/2)
        self.show()

    @QtCore.pyqtSlot()
    def adjustPosition(self):
        screen = QtWidgets.qApp.primaryScreen()
        geometry = screen.geometry()
        if self.x() + self.width() > geometry.x() + geometry.width():
            self.setX(geometry.x() + geometry.width() - self.width() - 10)
        if self.y() + self.height() > geometry.y() + geometry.height():
            self.setY(geometry.y() + geometry.height() - self.height() - 10)

    @QtCore.pyqtSlot(result="QVariant")
    def getScreenRect(self):
        screen = QtWidgets.qApp.primaryScreen()
        return screen.geometry()

    @QtCore.pyqtSlot(result="QVariant")
    def getCursorPos(self):
        return QtGui.QCursor.pos()

    @QtCore.pyqtProperty(bool, notify=_focusWindowNotify)
    def isFocusWindow(self):
        return self._isFocusWindow

    @QtCore.pyqtSlot(int)
    def setDeepinWindowShadowHint(self, width):
        pass

#@ 保存到文件
class saveToFile(QtCore.QObject):
    @QtCore.pyqtSlot(str, str)
    def saveToFile(self,fromText,toText):
        import os
        import csv
        from dae.utils import get_conf
        toText = str(toText).replace('谷歌翻译:','')
        toText = toText.split('有道:')
        firstText = ''
        if toText[0]:
            firstText = toText[0].strip('\n')
        lastText = toText[1].replace('有道:','').strip('\n').lstrip('w. ')
        if (firstText or lastText):
            if not firstText:
                firstText = ' '
            if not lastText:
                lastText = ' '
            conf = get_conf()
            savePath = str(conf['savePath']).rstrip('/') + '/translate.csv'

            if not os.path.exists(savePath):
                with open(savePath,'a+') as f:
                    writer = csv.writer(f)
                    writer.writerow(['翻译内容','谷歌翻译','有道词典'])
                    writeData = [
                        fromText, firstText, lastText
                    ]
                    writer.writerow(writeData)
                    f.close()
                return
            with open(savePath,'a+') as f:
                writer = csv.writer(f)
                writeData = [
                    fromText, firstText, lastText
                ]
                writer.writerow(writeData)
                f.close()
            return
        return

class LogoWindow(Window):

    onQuit = QtCore.pyqtSignal()
    onMainWindowToggled = QtCore.pyqtSignal()

    def __init__(self, getword_daemon, setting_config, api):
        Window.__init__(self)
        self.getword_daemon = getword_daemon
        self.setting_config = setting_config

        self.setFlags(QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.strokeResultWindow = StrokeResultWindow(self.getword_daemon, setting_config, api)
        self.qml_context.setContextProperty("strokeResultWindow", self.strokeResultWindow)
        self.qml_context.setContextProperty("getwordDaemon", self.getword_daemon)
        self.qml_context.setContextProperty("settingConfig", self.setting_config)
        self.qml_context.setContextProperty("windowApi", api)

        self.load_qml("LogoWindow.qml")

    def toggleMainWindow(self):
        self.onMainWindowToggled.emit()

    @QtCore.pyqtSlot(result=str)
    def getQueryWords(self):
        return self.strokeResultWindow.translate_info.text

class StrokeResultWindow(Window):

    translateFinished = QtCore.pyqtSignal()
    resultWindowHide = QtCore.pyqtSignal()

    def __init__(self, getword_daemon, setting_config, api):
        Window.__init__(self)
        self.getword_daemon = getword_daemon
        self.setting_config = setting_config

        self.setFlags(QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.setFlags(QtCore.Qt.Popup)
        self.youdaoTranslate = YoudaoTranslate()
        self.translate_info = self.youdaoTranslate.translate_info
        self.youdaoTranslate.translateFinished.connect(self.translateFinished)
        self.qml_context.setContextProperty("translateInfo", self.translate_info)
        self.qml_context.setContextProperty("getwordDaemon", self.getword_daemon)
        self.qml_context.setContextProperty("settingConfig", self.setting_config)
        self.qml_context.setContextProperty("windowApi", api)

        self.load_qml("StrokeResultWindow.qml")



    @QtCore.pyqtSlot(int, int)
    def updateStrokeIconPosition(self, x, y):
        self.rootObject().updateStrokeIconPosition(x, y)

    @QtCore.pyqtSlot(str)
    def translate(self, text):
        text = text.strip()
        if text:
            self.rootObject().changeQueryWords(text)
            self.youdaoTranslate.get_translate(text)

    @QtCore.pyqtSlot()
    def clear_translate(self):
        self.youdaoTranslate.clear_translate()

    def isPinned(self):
        return self.rootObject().isPinned()



class OcrResultWindow(Window):

    def __init__(self, getword_daemon, setting_config, api):
        Window.__init__(self)
        self.getword_daemon = getword_daemon
        self.setting_config = setting_config
        self.setFlags(QtCore.Qt.Tool | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.youdaoTranslate = YoudaoTranslate()
        self.translate_info = self.youdaoTranslate.translate_info
        self.youdaoTranslate.translateFinished.connect(self.handleTranslateFinished)

        self.qml_context.setContextProperty("translateInfo", self.translate_info)
        self.qml_context.setContextProperty("getwordDaemon", self.getword_daemon)
        self.qml_context.setContextProperty("settingConfig", self.setting_config)
        self.qml_context.setContextProperty("windowApi", api)
        self.load_qml("OcrResultWindow.qml")

    @QtCore.pyqtSlot()
    def handleTranslateFinished(self):
        if not self.isVisible():
            self.show()

    @QtCore.pyqtSlot(int, int, str)
    def startTranslate(self, x, y, text):
        self.setPos(x, y)
        self.translate(text)

    @QtCore.pyqtSlot(str)
    def translate(self, text):
        text = text.strip()
        if text:
            self.youdaoTranslate.get_translate(text)

    @QtCore.pyqtSlot(int, int)
    def setPos(self, x, y):
        self.setX(x)
        self.setY(y)


    def isPinned(self):
        return self.rootObject().isPinned()

class MiniWindow(Window):

    def __init__(self, getword_daemon, setting_config, api):
        Window.__init__(self)
        self.setting_config = setting_config
        self.setFlags(QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.FramelessWindowHint | \
                QtCore.Qt.WindowStaysOnTopHint)

        self.youdaoTranslate = YoudaoTranslate()
        self.qml_context.setContextProperty("youdaoTranslate", self.youdaoTranslate)
        self.qml_context.setContextProperty("translateInfo", self.youdaoTranslate.translate_info)
        self.qml_context.setContextProperty("suggestModel", suggestModel)
        self.qml_context.setContextProperty("historyModel", historyModel)
        self.qml_context.setContextProperty("getwordDaemon", getword_daemon)
        self.qml_context.setContextProperty("windowApi", api)
        self._menu = MiniWindowMenu(getword_daemon, api, self)
        self.qml_context.setContextProperty("popupMenu", self._menu)
        self.qml_context.setContextProperty("settingConfig", self.setting_config)

        self.config_group = "Mini Window"
        default_x = self.setting_config.get(self.config_group, "x")
        default_y = self.setting_config.get(self.config_group, "y")
        if default_x == None or default_y == None:
            # set default position at topright
            desktop = QtWidgets.qApp.desktop()
            geo = desktop.screenGeometry(desktop.primaryScreen())
            default_x = geo.x() + geo.width() - 388
            default_y = geo.y() + 100
        else:
            default_x = int(default_x)
            default_y = int(default_y)
        self.setX(default_x)
        self.setY(default_y)

        self.load_qml("MiniWindow.qml")

    @QtCore.pyqtSlot()
    def hideWindow(self):
        self.rootObject().hideMiniWindow()

    @QtCore.pyqtSlot()
    def recordCurrentPosition(self):
        self.setting_config.set(self.config_group, "x", self.x())
        self.setting_config.set(self.config_group, "y", self.y())

    @QtCore.pyqtSlot(str)
    def recordCurrentVisible(self, visible):
        self.setting_config.set(self.config_group, "visible", visible)

class SplashWindow(Window):

    ontimeout = QtCore.pyqtSignal()

    def __init__(self, api):
        Window.__init__(self)
        self.setFlags(QtCore.Qt.SplashScreen)
        self.setModality(QtCore.Qt.ApplicationModal)

        self.load_qml("Splash.qml")
        self._api = api

    @QtCore.pyqtSlot()
    def showCenter(self):
        # show center
        desktop = QtWidgets.qApp.desktop()
        geometry = desktop.screenGeometry(desktop.primaryScreen())
        x = geometry.x() + (geometry.width() - self.width())/2
        y = geometry.y() + (geometry.height() - self.height())/2
        self.setX(x)
        self.setY(y)
        self.show()

    @QtCore.pyqtSlot()
    def startTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.timeoutHandler)
        self.timer.start()

    def timeoutHandler(self):
        self.timer.stop()
        self.ontimeout.emit()
        self.hide()
        self.destroy()

class AboutWindow(Window):
    def __init__(self, parent=None):
        Window.__init__(self, parent)
        self.setFlags(QtCore.Qt.CustomizeWindowHint)
        self.setModality(QtCore.Qt.WindowModal)
        self.setTitle("有道词典")

        self.load_qml("AboutWindow.qml")

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(QtCore.QVariant)
    def showCenter(self, parent=None):
        # show center
        if parent:
            self.setParent(parent)
            x = parent.x() + (parent.width() - self.width())/2
            y = parent.y() + (parent.height() - self.height())/2
        else:
            desktop = QtWidgets.qApp.desktop()
            geometry = desktop.screenGeometry(desktop.primaryScreen())
            x = geometry.x() + (geometry.width() - self.width())/2
            y = geometry.y() + (geometry.height() - self.height())/2
        self.setX(x)
        self.setY(y)
        self.show()

class Menu(Window):
    def __init__(self, getword_daemon, parent=None):
        Window.__init__(self, parent)
        self.setFlags(QtCore.Qt.X11BypassWindowManagerHint|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        self.getword_daemon = getword_daemon
        self.qml_context.setContextProperty("getwordDaemon", getword_daemon)

        self.getword_daemon.hide.connect(self.hideHandler)

        self.timeoutShowTimer = QtCore.QTimer()
        self.timeoutShowTimer.setInterval(200)
        self.timeoutShowTimer.setSingleShot(True)
        self.timeoutShowTimer.timeout.connect(self.show)

    @QtCore.pyqtSlot()
    def showAtCursor(self):
        pos = self.getCursorPos()
        x = pos.x()
        y = pos.y()
        desktop = QtWidgets.qApp.desktop()
        geometry = desktop.screenGeometry(desktop.primaryScreen())
        if x + self.width() > geometry.x() + geometry.width():
            x = x - self.width()

        if y + self.height() > geometry.y() + geometry.height():
            y = y - self.height()

        self.setX(x)
        self.setY(y)
        if self.timeoutShowTimer.isActive():
            self.timeoutShowTimer.stop()
        self.timeoutShowTimer.start()

class TrayIconMenu(Menu):
    def __init__(self, getword_daemon, api):
        Menu.__init__(self, getword_daemon)
        self.qml_context.setContextProperty("windowApi", api)
        self.load_qml("TrayIconMenu.qml")

class MiniWindowMenu(Menu):
    def __init__(self, getword_daemon, api, miniWindow):
        Menu.__init__(self, getword_daemon)
        self.qml_context.setContextProperty("windowApi", api)
        self.qml_context.setContextProperty("miniWindow", miniWindow)
        self.load_qml("MiniWindowMenu.qml")
