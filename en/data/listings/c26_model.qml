import QtQuick
import QtQuick.Controls

ListView {
    id: list
    width: 360; height: 220
    model: wellModel                         // context property defined in Python
    spacing: 4
    delegate: Rectangle {
        required property string name         // model roles (roleNames) as
        required property real waterDepth     //   required properties of the delegate
        required property bool active
        width: ListView.view.width; height: 36; radius: 4
        color: active ? "#EAF1FA" : "#F2F2F2"
        Text { anchors.verticalCenter: parent.verticalCenter; x: 10
               text: name + " — WD " + waterDepth.toFixed(0) + " m"
                     + (active ? "" : " (inactive)") }
    }
}
