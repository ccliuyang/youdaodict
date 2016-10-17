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


from PyQt5 import QtWidgets, QtCore
from ui_setting_dialog import Ui_YoudaoSettingDialog

SCREEN_TRANS_PROMPT = [ "鼠标取词", "CTRL+鼠标取词", "SHIFT+鼠标取词", "鼠标中键取词", "ALT+鼠标取词" ]
WORD_STROKE_PROMPT = [ "展示划词图标", "直接展示结果", "双击Ctrl后展示结果" ]

class SettingDialog(QtWidgets.QWidget):

    closeWindow = QtCore.pyqtSignal()

    def __init__(self, setting_config, parent=None):
        super(SettingDialog, self).__init__(parent)
        self.setting_config = setting_config

        self.ui = Ui_YoudaoSettingDialog()
        self.ui.setupUi(self)
        self.initSetting()

        self.closeWindow.connect(self.handle_close_window)

        self.ui.ocrRadio_0.clicked.connect(lambda toggled: self.handleOcrModeChanged(0, toggled))
        self.ui.ocrRadio_1.clicked.connect(lambda toggled: self.handleOcrModeChanged(1, toggled))
        self.ui.ocrRadio_2.clicked.connect(lambda toggled: self.handleOcrModeChanged(2, toggled))
        self.ui.ocrRadio_3.clicked.connect(lambda toggled: self.handleOcrModeChanged(3, toggled))
        self.ui.ocrRadio_4.clicked.connect(lambda toggled: self.handleOcrModeChanged(4, toggled))

        self.ui.strokeRadio_0.clicked.connect(lambda toggled: self.handleStrokeModeChanged(0, toggled))
        self.ui.strokeRadio_1.clicked.connect(lambda toggled: self.handleStrokeModeChanged(1, toggled))
        self.ui.strokeRadio_2.clicked.connect(lambda toggled: self.handleStrokeModeChanged(2, toggled))

    def setCurrentIndex(self, index):
        self.ui.tabWidget.setCurrentIndex(index)

    def reload_settings(self):
        self.setting_config.reload()
        self.initSetting()

    def handle_close_window(self):
        self.reload_settings()
        self.hide()

    def initSetting(self):
        self.setChecked(self.ui.bootStartCheck, self.setting_config.get_basic_option("boot_start"))
        self.setChecked(self.ui.startMinCheck, self.setting_config.get_basic_option("start_mini"))
        self.setChecked(self.ui.topMostCheck, self.setting_config.get_basic_option("main_window_topmost"))
        self.setChecked(self.ui.closeToTrayCheck, self.setting_config.get_basic_option("close_to_tray"))

        ocrEnabled = self.setting_config.get_getword("ocr")
        self.setChecked(self.ui.ocrEnableCheckButton, ocrEnabled)
        self.setOcrRadioDisable(not ocrEnabled)

        strokeEnabled = self.setting_config.get_getword("stroke")
        self.setChecked(self.ui.strokeEnableCheckButton, strokeEnabled)
        self.setStrokeRadioDisable(not strokeEnabled)

        stroke_mode = self.setting_config.get_getword("stroke_mode")
        getattr(self.ui, "strokeRadio_" + str(stroke_mode)).setChecked(True)
        ocr_mode = self.setting_config.get_getword("ocr_mode")
        getattr(self.ui, "ocrRadio_" + str(ocr_mode)).setChecked(True)

    def setChecked(self, check_box, checked):
        check_box.setCheckState(QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)

    def getChecked(self, check_box):
        return check_box.checkState() == QtCore.Qt.Checked

    def on_bootStartCheck_clicked(self):
        checked = self.getChecked(self.ui.bootStartCheck)
        self.setting_config.set_basic_option("boot_start", checked, False)

    def on_startMinCheck_clicked(self):
        checked = self.getChecked(self.ui.startMinCheck)
        self.setting_config.set_basic_option("start_mini", checked, False)

    def on_topMostCheck_clicked(self):
        checked = self.getChecked(self.ui.topMostCheck)
        self.setting_config.set_basic_option("main_window_topmost", checked, False)

    def on_closeToTrayCheck_clicked(self):
        checked = self.getChecked(self.ui.closeToTrayCheck)
        self.setting_config.set_basic_option("close_to_tray", checked, False)

    def on_ocrEnableCheckButton_clicked(self):
        checked = self.getChecked(self.ui.ocrEnableCheckButton)
        disable = not checked
        self.setting_config.set_getword("ocr", checked, False)
        self.setOcrRadioDisable(disable)

    def setOcrRadioDisable(self, disable):
        self.ui.ocrRadio_0.setDisabled(disable)
        self.ui.ocrRadio_1.setDisabled(disable)
        self.ui.ocrRadio_2.setDisabled(disable)
        self.ui.ocrRadio_3.setDisabled(disable)
        self.ui.ocrRadio_4.setDisabled(disable)

    def on_strokeEnableCheckButton_clicked(self):
        checked = self.getChecked(self.ui.strokeEnableCheckButton)
        disable = not checked
        self.setting_config.set_getword("stroke", checked, False)
        self.setStrokeRadioDisable(disable)

    def setStrokeRadioDisable(self, disable):
        self.ui.strokeRadio_0.setDisabled(disable)
        self.ui.strokeRadio_1.setDisabled(disable)
        self.ui.strokeRadio_2.setDisabled(disable)

    def on_saveButton_clicked(self):
        self.setting_config.save()
        self.closeWindow.emit()

    def on_cancelButton_clicked(self):
        self.closeWindow.emit()

    def handleStrokeModeChanged(self, button_id, choosed):
        if choosed:
            self.setting_config.set_getword("stroke_mode", button_id, False)

    def handleOcrModeChanged(self, button_id, choosed):
        if choosed:
            self.setting_config.set_getword("ocr_mode", button_id, False)

    def closeEvent(self, e):
        self.closeWindow.emit()
        e.ignore()

if __name__ == '__main__':
    import os
    import sys
    import signal
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    from config import setting_config
    if os.name == 'posix':
        QApplication.setAttribute(Qt.AA_X11InitThreads, True)

    app = QApplication(sys.argv)
    obj = SettingDialog(setting_config)
    obj.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
