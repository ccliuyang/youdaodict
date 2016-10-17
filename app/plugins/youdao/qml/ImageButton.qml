import QtQuick 2.1

Item {
    id: button
    
    property url normal_image
    property url hover_image
    property url press_image
    property alias containsMouse: mouseArea.containsMouse

    property alias mouseArea: mouseArea
    property alias sourceSize: image.sourceSize

    property bool disabled: false
    property url disable_image: ""
    property bool pointingHandEnabled: false

    onDisabledChanged: {
        if(disabled){
            button.state = "disable"
        }
        else{
            button.state = ""
        }
    }
    
    signal clicked
    signal entered
    signal exited

    property bool pressed: state == "pressed"

    states: [
        State {
            name: "hovered"
            PropertyChanges { target: image; source: button.hover_image }
        },
        State {
            name: "pressed"
            PropertyChanges { target: image; source: button.press_image }
        },
        State {
            name: "disable"
            PropertyChanges { target: image; source: button.disable_image }
        }
    ]
    
    width: image.width;    height: image.height
    
    Image {
        id: image
        source: normal_image
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: !button.disabled
        cursorShape: pointingHandEnabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onEntered: {
            if(!button.disabled){
                button.state = "hovered"; button.entered()
            }
        }
        onExited: {
            if(!button.disabled){
                button.state = ""; button.exited()
            }
        }
        onPressed: {
            if(!button.disabled){
                button.state = "pressed"
            }
        }
        onReleased: {
            if(!button.disabled){
                button.state = mouseArea.containsMouse ? "hovered" : "" 
            }
        }
        onClicked: {
            if(!button.disabled){
                button.clicked()
            }
        }
    }
}
