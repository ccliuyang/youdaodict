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

import QtQuick 2.2

Item {
    id: rootLogo
    width: 30
    height: 30
    opacity: 1

    property int cursorX: 0
    property int cursorY: 0
    property string queryWords: ""

    function changeQueryWords(queryWords){
        rootLogo.queryWords = queryWords
        rootLogo.opacity = 1
        transparentAnimation.restart()
    }

    function startTranslate(x, y, text){
        text = text.trim()
        if(text != ""){
            strokeResultWindow.updateStrokeIconPosition(x, y)
            strokeResultWindow.translate(text)
        }
    }

    function showStrokeIcon(x, y, text){
        if(text.trim() != ""){
            mainView.setX(x)
            mainView.setY(y - 40)
            mainView.show()
        }
    }

    Connections {
        target: strokeResultWindow
        onResultWindowHide: {
            queryWords = ""
            getwordDaemon.ClearStroke()
        }
    }

    Connections{
        target: getwordDaemon
        onCursorPositionChanged: {
            cursorX = x
            cursorY = y
        }
        onStrokeRecognized: {
            var strokeEnable = settingConfig.get_getword("stroke")
            var strokeMode = settingConfig.get_getword("stroke_mode")
            if(strokeEnable) {
                queryWords = text
                if(strokeMode == "0") {
                    showStrokeIcon(x, y, text)
                    rootLogo.opacity = 1
                    transparentAnimation.restart()
                }
                else if(strokeMode == "1"){
                    startTranslate(x, y, text)
                }
            }
        }
        onHide: {
            if(mainView.visible && !mainView.in_translate_area()){
                mainView.hide()
                getwordDaemon.ClearStroke()
                queryWords = ""
            }
        }
        onDoubleCtrlReleased: {
            var strokeEnable = settingConfig.get_getword("stroke")
            var strokeMode = settingConfig.get_getword("stroke_mode")
            if(strokeEnable && strokeMode == "2") {
                if(queryWords != ""){
                    startTranslate(cursorX, cursorY, queryWords)
                }
            }
        }
    }

    Image {
        anchors.centerIn: parent
        source: "images/stroke_logo.png"
    }

    NumberAnimation {
        id: transparentAnimation
        duration: 4000
        target: rootLogo
        property: "opacity"
        to: 0.05
    }

    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            if(transparentAnimation.running){
                transparentAnimation.stop()
            }
            rootLogo.opacity = 1
            startTranslate(mainView.x, mainView.y+10, rootLogo.queryWords)
        }
        onExited: {
            if (mainView.visible){
                transparentAnimation.restart()
            }
        }
    }

}
