import QtQuick 2.2

Column {

    id: contentColumn
    property int textMargin: 8

    width: parent.width
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.leftMargin: textMargin
    anchors.rightMargin: textMargin

    property color contentFontColor: "#333"

    function queryDetail(){
        windowApi.showMainWindow()
        windowApi.emitDictQuery(translateInfo.text, translateInfo.lang)
    }

    function getResultContent(){
        var copyTextContent = translateInfo.text
        if(translateInfo.phonetic != ""){
            copyTextContent += " [%1]\n".arg(translateInfo.phonetic)
        }
        copyTextContent += "基本翻译\n"
        copyTextContent += "%1\n".arg(translateInfo.trans)
        copyTextContent += "网络释义\n"
        copyTextContent += "%1\n".arg(translateInfo.webtrans)
        return copyTextContent
    }

    // header line
    Item {
        width: parent.width
        height: dictText.height + 6

        TextEdit {
            id: dictText
            selectByMouse: true
            wrapMode: TextEdit.WordWrap
            readOnly: true
            anchors.verticalCenter: parent.verticalCenter
            font { pixelSize: 13}
            color: "#2699eb"
            text: "词典 "
        }

        Image {
            anchors.left: dictText.right
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width - dictText.width - 6
            height: 1
            fillMode: Image.TileHorizontally
            verticalAlignment: Image.AlignLeft
            source: "images/dict_title_line.png"
        }
    }

    // word tool line
    Row {
        id: wordToolLine
        width: parent.width
        height: 30
        spacing: 6

        TextEdit {
            id: phoneticText
            anchors.verticalCenter: parent.verticalCenter
            selectByMouse: true
            wrapMode: TextEdit.WordWrap
            readOnly: true
            font.pixelSize: 13
            text: translateInfo.phonetic != "" ? "[%1]".arg(translateInfo.phonetic) : ""
        }

        ImageButton{
            id: soundButton
            anchors.verticalCenter: parent.verticalCenter
            normal_image: "images/sound-production-normal.png"
            hover_image: "images/sound-production-hover.png"
            press_image: hover_image
            pointingHandEnabled: true
            onClicked: {
                windowApi.playSound(translateInfo.voices[0])
            }
        }

        TextEdit {
            id: detailsText
            anchors.verticalCenter: parent.verticalCenter
            selectByMouse: true
            wrapMode: TextEdit.WordWrap
            readOnly: true
            text: "详情>>"
            font.pixelSize: 12
            color: "#2699eb"

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    cursorShape = Qt.PointingHandCursor
                }
                onExited: {
                    cursorShape = Qt.ArrowCursor
                }
                onClicked: {
                    queryDetail()
                }
            }
        }

        TextEdit{
            color: "#ff0000"
            anchors.verticalCenter: parent.verticalCenter
            text: " 保存"
            selectByMouse: true
            readOnly: true
            font.pixelSize: 15
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onExited: {
                    cursorShape = Qt.ArrowCursor
                }
                onClicked: {
                    saveToFile.saveToFile(translateInfo.text, translateInfo.webtrans)
                    if (parent.color == "#2699eb"){
                        parent.color = "#ff0000";
                    }
                    else{
                        if(parent.color == "#ff0000"){
                            parent.color = "#2699eb"
                        }
                    }
                }
            }
        }
    }

    TextEdit{
            id: keywordsText
            width: parent.width
            //anchors.verticalCenter: parent.verticalCenter
            selectByMouse: true
            readOnly: true
            text: translateInfo.text
            wrapMode: Text.WordWrap
            font.pixelSize: 13
            font.bold: true
    }

    TextEdit {
        id: trans
        text: translateInfo.trans
        width: parent.width
        wrapMode: TextEdit.WordWrap
        selectByMouse: true
        font { pixelSize: 14 }
        readOnly: true
        color: contentFontColor
    }

    Item {
        width: parent.width
        height: netText.height + 10

        TextEdit {
            id: netText
            anchors.verticalCenter: parent.verticalCenter
            selectByMouse: true
            readOnly: true
            font { pixelSize: 13}
            color: "#2699eb"
            text: "网络释义 "
        }

        Image {
            anchors.left: netText.right
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width - netText.width - 6
            height: 1
            fillMode: Image.TileHorizontally
            verticalAlignment: Image.AlignLeft
            source: "images/dict_title_line.png"
        }
    }

    TextEdit {
        id: webtrans
        text: translateInfo.webtrans
        width: parent.width
        wrapMode: TextEdit.WordWrap
        selectByMouse: true
        font { pixelSize: 14 }
        readOnly: true
        color: contentFontColor
    }

    Item {
        width: parent.width
        height: 10
    }
}
