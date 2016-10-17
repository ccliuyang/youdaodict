/****************************************************************************
**
**  Copyright (C) 2011~2014 Deepin, Inc.
**                2011~2014 Kaisheng Ye
**
**  Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
**  Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
**
**  This program is free software: you can redistribute it and/or modify
**  it under the terms of the GNU General Public License as published by
**  the Free Software Foundation, either version 3 of the License, or
**  any later version.
**
**  This program is distributed in the hope that it will be useful,
**  but WITHOUT ANY WARRANTY; without even the implied warranty of
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**  GNU General Public License for more details.
**
**  You should have received a copy of the GNU General Public License
**  along with this program.  If not, see <http://www.gnu.org/licenses/>.
**
****************************************************************************/

import QtQuick 2.1

Rectangle{
    id: rootBox
    width: 134
    height: menuContent.height + 4

    property var constant: Constant {}

    border.width: 1
    border.color: constant.blueColor
    radius: 2

    Column {
        id: menuContent
        width: 130
        anchors.centerIn: parent

        MenuItem {
            itemText: "屏幕取词"
            itemImage: windowApi.ocrEnabled ? "menu_icon/menu_ico04.png" : "menu_icon/menu_ico04_disable.png"
            onClicked: windowApi.setOcrEnable(!windowApi.ocrEnabled)
        }

        MenuItem {
            itemText: "划词翻译"
            itemImage: windowApi.strokeEnabled ? "menu_icon/menu_ico05.png" : "menu_icon/menu_ico05_disable.png"
            onClicked: windowApi.setStrokeEnable(!windowApi.strokeEnabled)
        }

        MenuItem {
            isSeparator: true
        }

        MenuItem {
            itemText: "显示主窗口"
            itemImage: "menu_icon/menu_ico01.png"
            onClicked: windowApi.showMainWindow()
        }

        MenuItem {
            itemText: "软件设置"
            itemImage: "menu_icon/menu_ico03.png"
            onClicked: windowApi.option()
        }

        MenuItem {
            isSeparator: true
        }

        MenuItem {
            itemText: "关闭迷你窗口"
            itemImage: "menu_icon/menu_ico10.png"
            onClicked: miniWindow.hideWindow()
        }

    }
}

