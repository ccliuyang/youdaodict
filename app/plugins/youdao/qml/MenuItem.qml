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
import QtQuick.Controls 1.1

Rectangle {
    id: menuItem
    width: 130
    height: isSeparator ? 3 : 24

    property bool isSeparator: false
    property bool isHovered: false
    property string itemImage: ""
    property string itemText: ""

    signal clicked()

    Rectangle{
        id: leftBox
        width: 27
        height: parent.height
        color: isHovered ? "#c9e5f8" : "#eee"

        Image{
            source: itemImage
            anchors.centerIn: parent
            visible: !isSeparator
        }
    }

    Rectangle{
        id: rightBox
        width: parent.width - leftBox.width
        height: parent.height
        anchors.right: parent.right
        color: isHovered ? "#c9e5f8" : "#fff"

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            text: itemText
            font.pixelSize: 13
            visible: !isSeparator
        }

        Rectangle {
            width: parent.width - 4
            height: 1
            anchors.centerIn: parent
            visible: isSeparator
            color: "#bcc3c6"
        }
    }
    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        enabled: !isSeparator
        onEntered: {
            isHovered = true
        }
        onExited: {
            isHovered = false
        }
        onClicked: {
            mainView.hide()
            menuItem.clicked()
        }
    }
}
