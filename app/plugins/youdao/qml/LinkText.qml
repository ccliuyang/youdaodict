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

Text {
    id: linkText
    property url link: ""
    color: "#555"
    font.underline: true

    states: [
        State {
            name: "hover"
            PropertyChanges { target: linkText; color: "#111"}
        },
        State {
            name: "press"
            PropertyChanges { target: linkText; color: "#000"}
        }
    ]

    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            linkText.state = "hover"
        }
        onExited: {
            linkText.state = ""
        }
        onPressed: {
            linkText.state = "press"
        }
        onReleased: {
            if(containsMouse){
                linkText.state = "hover"
            }
            else{
                linkText.state = ""
            }
        }
        onClicked: {
            Qt.openUrlExternally(linkText.link)
        }
    }
}

