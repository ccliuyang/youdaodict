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

Item {
    id: ocrResultWindow
    width: 326
    height: 400

    property var constant: Constant {}

    property int contentHeight: topToolBarBox.height + resultBox.height
    onContentHeightChanged: {
        heightChangedTimer.restart()
    }

    Timer{
        id: heightChangedTimer
        interval: 200
        onTriggered: {
            mainView.setHeight(contentHeight)
        }
    }

    function isPinned(){
        return false
    }

    function hideWindow(){
        topToolBarBox.visible = false
        mainView.hide()
    }

    property int cursorX: 0
    property int cursorY: 0
    property int showCursorX: 0
    property int showCursorY: 0

    property bool ctrlKeyHold: false
    property bool altKeyHold: false
    property bool shiftKeyHold: false

    function handle_modifier_keys_released(ocr_mode){
        if(!mainView.visible && settingConfig.get_getword("ocr")){
            if(settingConfig.get_getword("ocr_mode") == ocr_mode){
                getwordDaemon.EmitOcr(cursorX, cursorY)
            }
        }
    }

    Timer{
        id: cursorPauseTimer
        interval: 1000
        onTriggered: {
            if(!mainView.visible && settingConfig.get_getword("ocr")){
                var ocr_mode = settingConfig.get_getword("ocr_mode")
                if (ocr_mode == "0" || (ocr_mode == "1" && ctrlKeyHold) || (ocr_mode == "4" && altKeyHold) || (ocr_mode == "2" && shiftKeyHold)){
                    getwordDaemon.EmitOcr(cursorX, cursorY)
                }
            }
        }
    }

    Connections {
        target: getwordDaemon
        onCursorPositionChanged: {
            cursorX = x
            cursorY = y
            if(mainView.visible){
                var distance = Math.sqrt(Math.pow(cursorY - showCursorY, 2) + Math.pow(cursorX - showCursorX, 2))
                if(distance > 50 && !mainView.in_translate_area()){
                    if(!pinButton.active){
                        hideWindow()
                    }
                }
                if(mainView.in_translate_area()){
                    topToolBarBox.visible = true
                }
            }
            else {
                if(cursorPauseTimer.running){
                    cursorPauseTimer.stop()
                }
                cursorPauseTimer.start()
            }
        }
        onOcrRecognized: {
            mainView.startTranslate(x, y, text)
        }
        onHide: {
            if(!pinButton.active){
                mainView.hideHandler()
            }
        }
        onCtrlPressed: {
            ctrlKeyHold = true
        }
        onCtrlReleased: {
            ctrlKeyHold = false
            handle_modifier_keys_released("1")
        }
        onAltPressed: {
            altKeyHold = true
        }
        onAltReleased: {
            altKeyHold = false
            handle_modifier_keys_released("4")
        }
        onShiftPressed: {
            shiftKeyHold = true
        }
        onShiftReleased: {
            shiftKeyHold = false
            handle_modifier_keys_released("2")
        }
        onWheelKeyReleased: {
            handle_modifier_keys_released("3")
        }
    }

    Connections {
        target: mainView
        onVisibleChanged: {
            if(mainView.visible){
                showCursorX = cursorX
                showCursorY = cursorY
                mainView.adjustPosition()
            }
            else{
                topToolBarBox.visible = false
            }
        }
    }

    Item {
        id: topToolBarBox
        width: parent.width
        height: 26
        visible: false

        Rectangle {
            anchors.right: parent.right
            width: toolButtonRow.width + 6
            height: 25
            color: constant.blueColor

            DragableArea {
                id: dragableArea
                anchors.fill: parent
                window: mainView
                property bool hasDrag: false

                onDragFinished: {
                    if (!hasDrag){
                        hasDrag = true
                    }
                }
            }

            Row {
                id: toolButtonRow
                anchors.centerIn: parent
                height: 19
                spacing: 2
                ImageButton{
                    normal_image: "images/ocr_tools/ocr_logo_normal.png"
                    hover_image: "images/ocr_tools/ocr_logo_hover.png"
                    press_image: "images/ocr_tools/ocr_logo_normal.png"
                    onClicked: contentColumn.queryDetail()
                }
                ImageButton{
                    normal_image: "images/ocr_tools/ocr_search_normal.png"
                    hover_image: "images/ocr_tools/ocr_search_hover.png"
                    press_image: "images/ocr_tools/ocr_search_normal.png"
                    onClicked: {
                        //var youdao_search_url = "http://www.youdao.com/search?q=%1&client=deskdictdeepin".arg(translateInfo.text)
                        var youdao_search_url = "https://www.google.com/search?q=%1".arg(translateInfo.text)
                        Qt.openUrlExternally(youdao_search_url)
                    }
                }
                ImageButton{
                    normal_image: "images/ocr_tools/ocr_copy_normal.png"
                    hover_image: "images/ocr_tools/ocr_copy_hover.png"
                    press_image: "images/ocr_tools/ocr_copy_normal.png"
                    onClicked: windowApi.copyText(contentColumn.getResultContent())
                }
                ImageButton{
                    normal_image: "images/ocr_tools/ocr_setting_normal.png"
                    hover_image: "images/ocr_tools/ocr_setting_hover.png"
                    press_image: "images/ocr_tools/ocr_setting_normal.png"
                    onClicked: {
                        if(!pinButton.active){
                            hideWindow()
                        }
                        windowApi.option(1)
                    }
                }
                ImageCheckButton {
                    id: pinButton
                    inactivatedNormalImage: "images/ocr_tools/ocr_pin_normal.png"
                    inactivatedHoverImage: "images/ocr_tools/ocr_pin_hover.png"
                    inactivatedPressImage: "images/ocr_tools/ocr_pin_normal.png"

                    activatedNormalImage: "images/ocr_tools/ocr_unpin_normal.png"
                    activatedHoverImage: "images/ocr_tools/ocr_unpin_hover.png"
                    activatedPressImage: "images/ocr_tools/ocr_unpin_normal.png"
                }
                ImageButton{
                    normal_image: "images/ocr_tools/ocr_close_normal.png"
                    hover_image: "images/ocr_tools/ocr_close_hover.png"
                    press_image: "images/ocr_tools/ocr_close_normal.png"
                    onClicked: hideWindow()
                }
            }
        }
    }

    Rectangle {
        id: resultBox
        anchors.top: topToolBarBox.bottom
        width: parent.width
        height: contentFlickable.height + 4
        border.width: 2
        border.color: constant.blueColor

        DFlickable {
            id: contentFlickable
            width: parent.width
            height: 290
            clip: true

            contentWidth: parent.width
            contentHeight: contentColumn.height

            onContentHeightChanged: {
                if(contentHeight < 290 && contentHeight > 0 ){
                    contentFlickable.height = contentHeight + 2
                }
                else{
                    contentFlickable.height = 290
                }
            }

            TranslateContent{
                id: contentColumn
            }
        }
    }
}
