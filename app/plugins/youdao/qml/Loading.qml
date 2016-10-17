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

import QtQuick 2.0

Image {
    id: container
    property bool on: false

    property string picNumber: "00"
    source: "loading/IMG000%1.bmp".arg(picNumber)

    Timer {
        running: true
        repeat: true
        interval: 50
        onTriggered: {
            var n = parseInt(container.picNumber)
            if(n == 11){
                n = 0
            }
            else{
                n += 1
            }

            if(n >= 10){
                container.picNumber = n.toString()
            }
            else{
                container.picNumber = "0" + n.toString()
            }
        }
    }

}
