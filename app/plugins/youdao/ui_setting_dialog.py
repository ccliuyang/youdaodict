# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_dialog.ui'
#
# Created: Fri Nov  7 14:45:01 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_YoudaoSettingDialog(object):
    def setupUi(self, YoudaoSettingDialog):
        YoudaoSettingDialog.setObjectName("YoudaoSettingDialog")
        YoudaoSettingDialog.setWindowModality(QtCore.Qt.WindowModal)
        YoudaoSettingDialog.resize(470, 460)
        YoudaoSettingDialog.setMinimumSize(QtCore.QSize(470, 460))
        YoudaoSettingDialog.setMaximumSize(QtCore.QSize(470, 460))
        self.verticalLayoutWidget = QtWidgets.QWidget(YoudaoSettingDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 451, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.basicTab = QtWidgets.QWidget()
        self.basicTab.setObjectName("basicTab")
        self.groupBox = QtWidgets.QGroupBox(self.basicTab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 415, 101))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 401, 56))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bootStartCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.bootStartCheck.setObjectName("bootStartCheck")
        self.verticalLayout_2.addWidget(self.bootStartCheck)
        self.startMinCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.startMinCheck.setObjectName("startMinCheck")
        self.verticalLayout_2.addWidget(self.startMinCheck)
        self.groupBox_2 = QtWidgets.QGroupBox(self.basicTab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 415, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 401, 56))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.topMostCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.topMostCheck.setObjectName("topMostCheck")
        self.verticalLayout_4.addWidget(self.topMostCheck)
        self.closeToTrayCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.closeToTrayCheck.setObjectName("closeToTrayCheck")
        self.verticalLayout_4.addWidget(self.closeToTrayCheck)
        self.tabWidget.addTab(self.basicTab, "")
        self.getwordTab = QtWidgets.QWidget()
        self.getwordTab.setObjectName("getwordTab")
        self.ocrEnableCheckButton = QtWidgets.QCheckBox(self.getwordTab)
        self.ocrEnableCheckButton.setGeometry(QtCore.QRect(8, 10, 421, 24))
        self.ocrEnableCheckButton.setObjectName("ocrEnableCheckButton")
        self.scrollArea = QtWidgets.QScrollArea(self.getwordTab)
        self.scrollArea.setGeometry(QtCore.QRect(10, 40, 421, 71))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 419, 69))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(6, 8, 64, 24))
        self.label.setObjectName("label")
        self.ocrRadio_0 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.ocrRadio_0.setGeometry(QtCore.QRect(70, 8, 91, 24))
        self.ocrRadio_0.setObjectName("ocrRadio_0")
        self.ocrRadio_3 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.ocrRadio_3.setGeometry(QtCore.QRect(160, 8, 121, 24))
        self.ocrRadio_3.setObjectName("ocrRadio_3")
        self.ocrRadio_4 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.ocrRadio_4.setGeometry(QtCore.QRect(280, 8, 114, 24))
        self.ocrRadio_4.setObjectName("ocrRadio_4")
        self.ocrRadio_1 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.ocrRadio_1.setGeometry(QtCore.QRect(70, 40, 121, 24))
        self.ocrRadio_1.setObjectName("ocrRadio_1")
        self.ocrRadio_2 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.ocrRadio_2.setGeometry(QtCore.QRect(280, 40, 131, 24))
        self.ocrRadio_2.setObjectName("ocrRadio_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.strokeEnableCheckButton = QtWidgets.QCheckBox(self.getwordTab)
        self.strokeEnableCheckButton.setGeometry(QtCore.QRect(10, 140, 421, 24))
        self.strokeEnableCheckButton.setObjectName("strokeEnableCheckButton")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.getwordTab)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 170, 421, 81))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 419, 79))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setGeometry(QtCore.QRect(6, 10, 64, 24))
        self.label_2.setObjectName("label_2")
        self.strokeRadio_0 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_2)
        self.strokeRadio_0.setGeometry(QtCore.QRect(70, 10, 131, 24))
        self.strokeRadio_0.setObjectName("strokeRadio_0")
        self.strokeRadio_1 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_2)
        self.strokeRadio_1.setGeometry(QtCore.QRect(240, 10, 131, 24))
        self.strokeRadio_1.setObjectName("strokeRadio_1")
        self.strokeRadio_2 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_2)
        self.strokeRadio_2.setGeometry(QtCore.QRect(70, 40, 161, 24))
        self.strokeRadio_2.setObjectName("strokeRadio_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget.addTab(self.getwordTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.cancelButton = QtWidgets.QPushButton(YoudaoSettingDialog)
        self.cancelButton.setGeometry(QtCore.QRect(360, 420, 95, 27))
        self.cancelButton.setObjectName("cancelButton")
        self.saveButton = QtWidgets.QPushButton(YoudaoSettingDialog)
        self.saveButton.setGeometry(QtCore.QRect(250, 420, 95, 27))
        self.saveButton.setObjectName("saveButton")

        self.retranslateUi(YoudaoSettingDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(YoudaoSettingDialog)

    def retranslateUi(self, YoudaoSettingDialog):
        _translate = QtCore.QCoreApplication.translate
        YoudaoSettingDialog.setWindowTitle(_translate("YoudaoSettingDialog", "软件设置"))
        self.groupBox.setTitle(_translate("YoudaoSettingDialog", "启动"))
        self.bootStartCheck.setText(_translate("YoudaoSettingDialog", "开机时自动启动"))
        self.startMinCheck.setText(_translate("YoudaoSettingDialog", "启动后最小化到系统托盘"))
        self.groupBox_2.setTitle(_translate("YoudaoSettingDialog", "主窗口"))
        self.topMostCheck.setText(_translate("YoudaoSettingDialog", "主窗口总在最上面"))
        self.closeToTrayCheck.setText(_translate("YoudaoSettingDialog", "窗口关闭时最小化到托盘"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.basicTab), _translate("YoudaoSettingDialog", "基本设置"))
        self.ocrEnableCheckButton.setText(_translate("YoudaoSettingDialog", "启用屏幕取词"))
        self.label.setText(_translate("YoudaoSettingDialog", "取词方式"))
        self.ocrRadio_0.setText(_translate("YoudaoSettingDialog", "鼠标取词"))
        self.ocrRadio_1.setText(_translate("YoudaoSettingDialog", "Ctrl+鼠标取词"))
        self.ocrRadio_2.setText(_translate("YoudaoSettingDialog", "Shift+鼠标取词"))
        self.ocrRadio_3.setText(_translate("YoudaoSettingDialog", "鼠标中键取词"))
        self.ocrRadio_4.setText(_translate("YoudaoSettingDialog", "Alt+鼠标取词"))
        self.strokeEnableCheckButton.setText(_translate("YoudaoSettingDialog", "启用划词释义"))
        self.label_2.setText(_translate("YoudaoSettingDialog", "展示方式"))
        self.strokeRadio_0.setText(_translate("YoudaoSettingDialog", "展示划词图标"))
        self.strokeRadio_1.setText(_translate("YoudaoSettingDialog", "直接展示结果"))
        self.strokeRadio_2.setText(_translate("YoudaoSettingDialog", "双击Ctrl后展示结果"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.getwordTab), _translate("YoudaoSettingDialog", "取词划词"))
        self.cancelButton.setText(_translate("YoudaoSettingDialog", "取消"))
        self.saveButton.setText(_translate("YoudaoSettingDialog", "保存设置"))
