import QtQuick
import QtQuick.Shapes

Item {
    id: root
    property real value: 0          // set by Python (QSlider)
    property real maximum: 400
    signal alarm(real value)        // emitted to Python
    implicitWidth: 260; implicitHeight: 200
    onValueChanged: if (value > 0.8 * maximum) alarm(value)

    Shape {
        anchors.fill: parent
        ShapePath {                 // background arc
            strokeColor: "#D9D9D9"; strokeWidth: 18; fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            PathAngleArc { centerX: root.width / 2; centerY: root.height * 0.75
                           radiusX: 100; radiusY: 100; startAngle: 180; sweepAngle: 180 }
        }
        ShapePath {                 // arc proportional to the value
            strokeColor: root.value > 0.8 * root.maximum ? "#C00000" : "#2E75B6"
            strokeWidth: 18; fillColor: "transparent"; capStyle: ShapePath.RoundCap
            PathAngleArc { centerX: root.width / 2; centerY: root.height * 0.75
                           radiusX: 100; radiusY: 100; startAngle: 180
                           sweepAngle: 180 * Math.min(root.value / root.maximum, 1) }
        }
    }
    Text {
        objectName: "reading"
        anchors.horizontalCenter: parent.horizontalCenter; y: root.height * 0.55
        font.pixelSize: 28; font.bold: true
        text: root.value.toFixed(0) + " bar"
    }
    Behavior on value { NumberAnimation { duration: 150 } }   // smooth transition
}
