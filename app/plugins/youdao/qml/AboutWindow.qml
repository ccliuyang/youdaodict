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
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.1

Item {
    id: rootBox
    width: frame.width + effect.cornerRadius * 2
    height: frame.height + effect.cornerRadius * 2

    property int contentTopMargin: 32

    RectangularGlow {
        id: effect
        anchors.fill: frame
        glowRadius: 5
        spread: 0.1
        color: Qt.rgba(0, 0, 0, 0.5)
        cornerRadius: frame.radius + glowRadius
    }

    Rectangle{
        id: frame
        width: 360
        height: titleBox.height + centerBox.height + bottomBox.height
        anchors.centerIn: parent
        radius: 0

        Rectangle{
            id: titleBox
            width: parent.width
            height: 30
            color: "#299bec"

            DragableArea {
                id: dragableArea
                anchors.fill: parent
                window: mainView
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 10
                color: "#fff"
                text: "有道词典"
            }

            ImageButton{
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 6
                normal_image: "images/window_close_normal.png"
                hover_image: "images/window_close_hover.png"
                press_image: "images/window_close_hover.png"
                onClicked: {
                    mainView.hide()
                }
            }
        }

        Item {
            id: centerBox
            width: parent.width
            height: 140
            anchors.top: titleBox.bottom

            Item {
                id: leftBox
                width: parent.width/2
                height: parent.height
                anchors.bottom: parent.bottom

                Image {
                    source: "images/youdao_deepin_logo.png"
                    anchors.top: parent.top
                    anchors.topMargin: contentTopMargin
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            Item {
                id: rightBox
                width: parent.width/2
                height: parent.height
                anchors.left: leftBox.right
                anchors.bottom: parent.bottom

                Column {
                    width: parent.width
                    anchors.top: parent.top
                    anchors.topMargin: contentTopMargin
                    spacing: 4

                    Text{
                        text: "当前版本 1.0"
                    }
                    Text{
                        text: "版权所有©2014网易公司"
                    }
                    LinkText{
                        text: "cidian.youdao.com"
                        link: "http://cidian.youdao.com/?client=deskdictdeepin"
                    }
                    Text{
                        text: "版权所有©2014深之度"
                    }
                    LinkText{
                        text: "www.deepin.org"
                        link: "http://www.deepin.org"
                    }
                }
            }
        }

        Column {
            id: bottomBox
            anchors.top: centerBox.bottom
            width: parent.width
            height: childrenRect.height
            spacing: 6

            Rectangle {
                width: parent.width - 40
                anchors.horizontalCenter: parent.horizontalCenter
                height: 1
                color: "#aaa"
            }

            Label {
                width: parent.width - 40
                anchors.horizontalCenter: parent.horizontalCenter
                text: "警告：本计算机程序受著作权法和国际公约的保护，未经授权擅自复制或传播本程序的部分或全部，可能受到严厉的民事及刑事制裁，并将在法律许可的范围内受到可能的起诉。"
                wrapMode: Text.WordWrap
            }
            Item {
                width: parent.width
                height: 6
            }
        }
    }
}
