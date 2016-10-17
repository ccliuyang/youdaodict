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
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1

Item {
    id: rootBox
    width: frame.width + effect.cornerRadius * 2
    height: frame.height + effect.cornerRadius * 2

    RectangularGlow {
        id: effect
        anchors.fill: frame
        glowRadius: 5
        spread: 0.1
        color: Qt.rgba(0, 0, 0, 0.2)
        cornerRadius: frame.radius + glowRadius
    }

    Rectangle {
        id: frame
        color: "white"
        anchors.centerIn: parent
        width: 550
        height: 300
        radius: 0
        clip: true
        border.color: "#a1a1a1"
        border.width: 1

        Image {
            anchors.centerIn: parent
            source: "images/youdao_splash.png"
        }
    }
}
