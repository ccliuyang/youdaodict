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
import QtQuick.Window 2.0
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1

Item {
    id: rootBox
    width: frame.width + effect.cornerRadius * 2
    height: frame.height + effect.cornerRadius * 2

    property var constant: Constant {}
    property int textMargin: 8

    property int strokeIconX: 0
    property int strokeIconY: 0

    property int cursorX: 0
    property int cursorY: 0

    function changeQueryWords(text) {
        text = text.trim()
        if(text != ""){
            if(queryTextInput.text != text){
                queryTextInput.text = text
            }
        }
        else{
            mainView.clear_translate()
        }
    }

    function translateWords(text){
        text = text.trim()
        if(text != ""){
            mainView.translate(text)
        }
        else{
            mainView.clear_translate()
        }
    }

    function isPinned(){
        return pinButton.active
    }

    function updateStrokeIconPosition(x, y){
        strokeIconX = x
        strokeIconY = y
    }

    function hideWindow(){
        mainView.hide()
        getwordDaemon.ClearStroke()
        changeQueryWords("")
        mainView.resultWindowHide()
    }

    function isCursorResultArea(){
        if(mainView.in_translate_area()){
            var x = mainView.x
            var y = mainView.y + topBox.height
            var width = mainView.width
            var height = mainView.height - topBox.height
            return (cursorX >= x) && (cursorX <= x+width) && (cursorY >= y) && (cursorY <= y + height)
        }
        else{
            return false
        }
    }

    Timer{
        id: repaintWindow
        interval: 200
        repeat: true
        property int count: 0
        onTriggered: {
            if(count < 20){
                mainView.update()
                count += 1
            }
            else{
                count = 0
                running = false
            }
        }
        onRunningChanged: {
            if(running){
                count = 0
            }
        }
    }

    Connections {
        target: mainView
        onVisibleChanged: {
            if(!mainView.visible){
                dragableArea.hasDrag = false
                mainView.resultWindowHide()
            }
            else{
                delayUpdateResultBox.restart()
            }
        }
        onTranslateFinished: {
            showResult()
        }
    }

    Connections{
        target: getwordDaemon
        onHide: {
            if(mainView.visible && !isPinned()){
                if((!topBox.visible && !isCursorResultArea()) || (topBox.visible && !mainView.in_translate_area())){
                    hideWindow()
                }
            }
        }
        onCursorPositionChanged: {
            cursorX = x
            cursorY = y
            if(isCursorResultArea() && mainView.visible && !topBox.visible){
                showTopBox()
            }
        }
    }

    RectangularGlow {
        id: effect
        anchors.fill: frame
        glowRadius: 5
        spread: 0.1
        color: Qt.rgba(0, 0, 0, 0.3)
        cornerRadius: frame.radius + glowRadius
        visible: topBox.visible
    }

    function showResult(){
        print("show result...")
        if(!isPinned()){
            mainView.setX(strokeIconX)
            mainView.setY(strokeIconY)
        }
        if(!mainView.visible){
            topBox.updateVisible(false)
        }
        delayUpdateResultBox.restart()
        mainView.show()
        mainView.raise()
        mainView.requestActivate()
        repaintWindow.restart()
    }

    function showTopBox(){
        print("show top box...")
        topBox.updateVisible(true)
        delayUpdateResultBox.restart()
        mainView.show()
        mainView.raise()
        mainView.requestActivate()
        repaintWindow.restart()
    }

    Rectangle {
        id: frame
        anchors.centerIn: parent
        width: 339
        height: topBox.height + resultBox.height
        radius: 0
        clip: true
        color: "transparent"

        Rectangle {
            id: topBox
            width: parent.width
            height: titleBox.height + keywordsBox.height + 1
            clip: true

            function updateVisible(show){
                visible = show
            }

            Item {
                id: titleBox
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width
                height: 32

                Image {
                    id: logoImage
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    source: "images/title_bg.png"
                }

                DragableArea {
                    id: dragableArea
                    anchors.fill: parent
                    window: mainView
                    property bool hasDrag: false

                    onDragFinished: {
                        if (!hasDrag){
                            pinButton.active = true
                            hasDrag = true
                        }
                    }
                }

                ImageButton {
                    id: settingButton
                    anchors.right: pinButton.left
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.rightMargin: 8
                    normal_image: "images/setting_normal.png"
                    hover_image: "images/setting_hover.png"
                    press_image: "images/setting_press.png"
                    onClicked: {
                        if(!isPinned()){
                            hideWindow()
                        }
                        windowApi.option(1)
                    }
                }

                ImageCheckButton {
                    id: pinButton
                    anchors.right: closeButton.left
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter

                    inactivatedNormalImage: "images/pin_off_normal.png"
                    inactivatedHoverImage: "images/pin_off_hover.png"
                    inactivatedPressImage: "images/pin_off_press.png"

                    activatedNormalImage: "images/pin_on_normal.png"
                    activatedHoverImage: "images/pin_on_hover.png"
                    activatedPressImage: "images/pin_on_press.png"
                }

                ImageButton {
                    id: closeButton
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    normal_image: "images/close_normal.png"
                    hover_image: "images/close_hover.png"
                    press_image: "images/close_press.png"
                    onClicked: {
                        pinButton.active = false
                        mainView.hide()
                    }
                }
            }

            Item {
                id: keywordsBox
                anchors.top: titleBox.bottom
                anchors.topMargin: 1
                width: parent.width
                height: 35
                clip: true

                Image {
                    anchors.left: parent.left
                    anchors.right: searchButton.right
                    fillMode: Image.TileHorizontally
                    verticalAlignment: Image.AlignLeft
                    source: "images/input_bg.png"
                }

                ImageButton {
                    id: searchButton
                    anchors.right: parent.right
                    normal_image: "images/search_normal.png"
                    hover_image: "images/search_hover.png"
                    press_image: "images/search_press.png"
                    onClicked: {
                        translateWords(queryTextInput.text)
                    }
                }

                TextField {
                    id: queryTextInput
                    anchors.left: parent.left
                    anchors.leftMargin: textMargin - 6
                    anchors.right: searchButton.left
                    anchors.rightMargin: 4
                    anchors.top: parent.top
                    anchors.topMargin: Math.round((parent.height - 5 - height)/2)
                    clip: true
                    style: TextFieldStyle {
                        background: Item {
                            width: parent.width
                            height: parent.height
                        }
                    }
                    onAccepted: {
                        getwordDaemon.ClearStroke()
                        translateWords(text)
                    }
                }
            }
        }

        Rectangle{
            id: resultBox
            width: parent.width
            height: resultContent.height
            anchors.top: topBox.bottom

            DFlickable {
                id: resultContent
                height: maxHeight
                width: parent.width
                clip: true
                property int maxHeight: 300

                contentWidth: parent.width
                contentHeight: contentColumn.height

                function updateHeight(){
                    if(contentHeight > maxHeight || contentHeight <= 0){
                        height = maxHeight
                    }
                    else{
                        height = contentHeight
                    }
                }

                Timer{
                    id: delayUpdateResultBox
                    interval: 200
                    onTriggered: {
                        resultContent.updateHeight()
                        mainView.adjustPosition()
                        repaintWindow.restart()
                    }
                }

                TranslateContent{
                    id: contentColumn
                }
            }

            Rectangle{
                id: contentBorder
                anchors.fill: parent
                color: "transparent"
                border.color: constant.blueColor
                border.width: 1
                visible: !topBox.visible
                Rectangle {
                    height: 3
                    width: parent.width
                    color: parent.border.color
                }
            }
        }
    }
}
