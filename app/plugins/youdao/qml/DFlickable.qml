import QtQuick 2.0;
Flickable{
    id: root
    property Flickable flickable : root

    Item {
        id: scrollbar
        width: handleSize
        height: flickable.contentHeight
        visible: (flickable.visibleArea.heightRatio < 1.0)
        anchors.right: parent.right
        z: 10

        property int handleSize: 12
        property alias backHandle: backHandle
        property color inactiveColor: Qt.rgba(0, 0, 0, 0.5)
        property color activeColor: Qt.rgba(0, 0, 0, 0.9)
        property bool inInteractive: false

        function scrollDown () {
            flickable.contentY = Math.min (flickable.contentY + (flickable.height / 4), flickable.contentHeight - flickable.height)
        }
        function scrollUp () {
            flickable.contentY = Math.max (flickable.contentY - (flickable.height / 4), 0)
        }

        function handleShow(){
            backHandle.opacity = 0.7
            backHandle.color = activeColor
            scrollbar.inInteractive = true
        }

        function handleHide(){
            if (hideTimer.running){
                hideTimer.stop()
            }
            hideTimer.restart()
            backHandle.color = inactiveColor
            scrollbar.inInteractive = false
        }

        Binding {
            target: handle
            property: "y"
            value: (flickable.contentY * clicker.drag.maximumY / (flickable.contentHeight - flickable.height))
            when: (!clicker.drag.active)
        }
        
        Binding {
            target: flickable
            property: "contentY"
            value: (handle.y * (flickable.contentHeight - flickable.height) / clicker.drag.maximumY)
            when: (clicker.drag.active || clicker.pressed)
        }

        Connections {
            target: handle
            onYChanged: {
                scrollbar.handleShow()
                scrollbar.handleHide()
            }
        }
        
        Item {
            id: groove
            clip: true
            anchors {
                fill: parent
                margins: 1
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                
                drag.target: handle
                drag.axis: Drag.YAxis
                drag.minimumY: 0
                drag.maximumY: (groove.height - handle.height)
                drag.filterChildren: true
                
                onClicked: { 
                    flickable.contentY = (mouse.y / groove.height * (flickable.contentHeight - flickable.height)) 
                }

                onEntered: {
                    scrollbar.handleShow()
                }
                
                onExited: {
                    scrollbar.handleHide()
                }
            }
            
            Item {
                id: handle
                height: Math.max(30, (flickable.visibleArea.heightRatio * flickable.height))
                anchors {
                    left: parent.left
                    right: parent.right
                }

                Rectangle {
                    id: backHandle
                    color: scrollbar.inactiveColor
                    anchors { fill: parent }
                    border.color: "#44ffffff"
                    border.width: 1
                    radius: 6
                    opacity: 0

                    Behavior on opacity { NumberAnimation { duration: 150 } }
                }
                
                MouseArea {
                    id: clicker
                    anchors.fill: parent
                    hoverEnabled: true

                    drag.target: handle
                    drag.axis: Drag.YAxis
                    drag.minimumY: 0
                    drag.maximumY: (groove.height - handle.height)
                    drag.filterChildren: true

                    onPressed: {
                    }
            
                    onEntered: {
                        scrollbar.handleShow()
                    }
                    
                    onExited: {
                        scrollbar.handleHide()
                    }
                }
            }
        }

        Timer {
            id: hideTimer
            interval: 150
            repeat: false
            onTriggered: {
                if (!scrollbar.inInteractive) {
                    backHandle.opacity = 0
                }
            }
        }
    }
}
