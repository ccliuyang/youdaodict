import QtQuick 2.1

Item {
    id: imageCheckButton
    width: currentImage.width
    height: currentImage.height

    property string inactivatedNormalImage
    property string inactivatedHoverImage
    property string inactivatedPressImage

    property string activatedNormalImage
    property string activatedHoverImage
    property string activatedPressImage

    signal clicked
    property bool active: false

    property bool hover: false
    property bool pressed: false

    Image {
        id: currentImage
        anchors.centerIn: parent
        cache: false
        source: {
            if(parent.active){
                if(parent.pressed){
                    return parent.activatedPressImage
                }
                else{
                    if (parent.hover){
                        return parent.activatedHoverImage
                    }
                    else{
                        return parent.activatedNormalImage
                    }
                }
            }
            else{
                if(parent.pressed){
                    return parent.inactivatedPressImage
                }
                else{
                    if (parent.hover){
                        return parent.inactivatedHoverImage
                    }
                    else{
                        return parent.inactivatedNormalImage
                    }
                }
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onPressed: {
            parent.hover = false
            parent.pressed = true
        }

        onReleased: {
            parent.hover = containsMouse
            parent.active = !parent.active
            imageCheckButton.clicked()
            parent.pressed = false
        }

        onEntered: {
            parent.hover = true
            parent.pressed = false
        }

        onExited: {
            parent.hover = false
            parent.pressed = false
        }
    }
}
