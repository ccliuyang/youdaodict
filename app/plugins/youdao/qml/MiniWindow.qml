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

    property var constant: Constant {}

    function hideMiniWindow(){
        pinButton.active = false
        mainView.hide()
        mainView.recordCurrentVisible("false")
    }

    Connections{
        target: mainView
        onIsFocusWindowChanged: {
            if(mainView.isFocusWindow){
                mainView.opacity = 1.0
            }
            else{
                if (frame.showConetnt == "suggest"){
                    frame.showConetnt = ""
                }
                historyButton.showHistory = false
                if(isPinned()){
                    mainView.opacity = 1.0
                }
                else{
                    mainView.opacity = 0.8
                }
            }
        }
    }

    Connections{
        target: youdaoTranslate
        onTranslateFinished: {
            frame.showConetnt = "translate"
            historyButton.showHistory = false
            historyModel.addSearchData(translateInfo.text, translateInfo.trans, translateInfo.webtrans)
        }
    }

    onHeightChanged: {
        mainView.setHeight(height)
    }

    property int textMargin: 8

    function isPinned(){
        return pinButton.active
    }

    RectangularGlow {
        id: effect
        anchors.fill: frame
        glowRadius: 5
        spread: 0.1
        color: Qt.rgba(0, 0, 0, 0.5)
        cornerRadius: frame.radius + glowRadius

        Component.onCompleted: mainView.setDeepinWindowShadowHint(5)
    }

    Rectangle {
        id: frame
        color: "transparent"
        anchors.centerIn: parent
        width: 288
        height: childrenRect.height
        radius: 0
        clip: true

        property string showConetnt: ""

        Item {
            id: title
            anchors.top: frame.top
            anchors.left: frame.left
            anchors.right: frame.right
            height: 26

            Image {
                id: logoImage
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                source: "images/mini_title_bg.png"
            }

            DragableArea {
                id: dragableArea
                anchors.fill: parent
                window: mainView
                property bool hasDrag: false
                onDragFinished: {
                    mainView.recordCurrentPosition()
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
                onClicked: popupMenu.showAtCursor()
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
                onClicked: hideMiniWindow()
            }
        }

        Rectangle{
            id: keywordsBox
            anchors.top: title.bottom
            width: parent.width
            height: 36
            color: "#f5f5f5"
            clip: true

            TextField {
                id: queryTextInput
                anchors.left: parent.left
                anchors.leftMargin: textMargin - 6
                anchors.right: historyButton.left
                anchors.top: parent.top
                anchors.topMargin: Math.round((parent.height - height)/2)
                clip: true
                style: TextFieldStyle {
                    background: Item {
                        width: parent.width
                        height: parent.height
                    }
                }
                property bool pause: false

                onAccepted: {
                    youdaoTranslate.get_translate(text)
                }

                onTextChanged: {
                    historyButton.showHistory = false
                    if(pause){
                        pause = false
                        return
                    }
                    if(text){
                        frame.showConetnt = "suggest"
                        suggestModel.suggestWithNum(text)
                    }
                    else{
                        frame.showConetnt = ""
                    }
                }
            }

            ImageButton {
                id: historyButton
                anchors.bottom: parent.bottom
                anchors.right: searchButton.left
                normal_image: "images/mini_history_normal.png"
                hover_image: "images/mini_history_hover.png"
                press_image: "images/mini_history_press.png"
                property bool showHistory: false
                onClicked: {
                    if(historyModel.count > 0){
                        showHistory = !showHistory
                    }
                }
            }

            ImageButton {
                id: searchButton
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                normal_image: "images/mini_search_normal.png"
                hover_image: "images/mini_search_hover.png"
                press_image: "images/mini_search_press.png"
                onClicked: {
                    youdaoTranslate.get_translate(queryTextInput.text)
                }
            }
        }

        
        Rectangle {
            anchors.top: keywordsBox.bottom
            width: parent.width
            height: {
                if (historyButton.showHistory){
                    return 0
                }
                if (frame.showConetnt == "translate" && (mainView.isFocusWindow || isPinned())){
                    return contentFlickable.height
                }
                return 0
            }
            clip: true

            DFlickable {
                id: contentFlickable 
                width: parent.width
                height: maxHeight
                clip: true
                property int maxHeight: 300

                contentWidth: parent.width
                contentHeight: translateContent.height
                onContentHeightChanged: {
                    if(contentHeight < maxHeight && contentHeight > 0 ){
                        height = contentHeight
                    }
                    else{
                        height = maxHeight
                    }
                }

                TranslateContent {
                    id: translateContent
                }
            }

            Image {
                width: parent.width
                fillMode: Image.TileHorizontally
                verticalAlignment: Image.AlignLeft
                source: "images/input_shadow.png"
            }
        }

        Rectangle {
            id: suggestListBox
            anchors.top: keywordsBox.bottom
            anchors.topMargin: height > 0 ? 1 : 0
            width: parent.width
            height: frame.showConetnt == "suggest" && mainView.isFocusWindow && !historyButton.showHistory ? suggestListView.height + 2 : 0
            border.color: constant.blueColor
            border.width: 1
            color: "transparent"
            visible: frame.showConetnt == "suggest"

            ListView {
                id: suggestListView
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 1
                width: parent.width - 2
                height: childrenRect.height
                model: suggestModel
                delegate: queryDelegate
            }
        }

        Rectangle {
            id: historyBox
            anchors.top: keywordsBox.bottom
            anchors.topMargin: height > 0 ? 1 : 0
            width: parent.width
            height: historyButton.showHistory ? historyPopupContent.height + 2: 0
            border.color: constant.blueColor
            border.width: 1
            clip: true

            Column {
                id: historyPopupContent
                width: parent.width - 2
                anchors.top: parent.top
                anchors.topMargin: 1
                anchors.horizontalCenter: parent.horizontalCenter
                ListView {
                    id: historyListView
                    width: parent.width
                    height: childrenRect.height
                    model: historyModel
                    delegate: queryDelegate
                }
                Rectangle{
                    width: parent.width
                    height: 27
                    color: "#e7f2f7"

                    Row {
                        anchors.left: parent.left
                        anchors.leftMargin: 5
                        height: parent.height
                        spacing: 5

                        ImageButton{
                            anchors.verticalCenter: parent.verticalCenter
                            normal_image: "images/history/left_normal.png"
                            hover_image: "images/history/left_hover.png"
                            press_image: hover_image
                            onClicked: historyModel.currentPage -= 1

                            disable_image: "images/history/left_disable.png"
                            disabled: historyModel.currentPage == 1
                        }

                        Label {
                            anchors.verticalCenter: parent.verticalCenter
                            text: "%1/%2".arg(historyModel.currentPage).arg(historyModel.totalPage)
                        }

                        ImageButton {
                            anchors.verticalCenter: parent.verticalCenter
                            normal_image: "images/history/right_normal.png"
                            hover_image: "images/history/right_hover.png"
                            press_image: hover_image
                            onClicked: historyModel.currentPage += 1

                            disable_image: "images/history/right_disable.png"
                            disabled: historyModel.currentPage == historyModel.totalPage
                        }
                    }

                    ImageButton{
                        anchors.right: parent.right
                        anchors.rightMargin: 5
                        anchors.verticalCenter: parent.verticalCenter
                        normal_image: "images/history/clear_normal.png"
                        hover_image: "images/history/clear_hover.png"
                        press_image: hover_image
                        onClicked: {
                            historyButton.showHistory = false
                            historyModel.clearAllData()
                        }
                    }

                }
            }
        }
    }

    Component{
        id: queryDelegate

        Item {
            width: parent.width
            height: 25

            Rectangle{
                id: contentBox
                width: parent.width
                height: 24
                color: hovered ? "#d3eafe" : "#ffffff"

                property bool hovered: false
                
                Text {
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                    anchors.right: parent.right
                    anchors.rightMargin: 6
                    anchors.verticalCenter: parent.verticalCenter
                    text: "<b>" + title + "</b> " + explain
                    elide: Text.ElideRight
                    color: "#333"
                }
            }

            Rectangle{
                width: parent.width
                height: 1
                anchors.bottom: parent.bottom
                color: "#e8f3f7"
            }

            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: contentBox.hovered = true
                onExited: contentBox.hovered = false

                onClicked: {
                    youdaoTranslate.get_translate(title)
                    queryTextInput.pause = true
                    queryTextInput.text = title
                }
            }
        }
    }

    Timer{
        id: showTimer
        running: true
        interval: 2000
        onTriggered: {
            var visible = settingConfig.get("Mini Window", "visible")
            if(visible == "true"){
                mainView.show()
            }
        }
    }
}
