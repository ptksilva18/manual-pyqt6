import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Engineering 1.0

ApplicationWindow {
    id: window
    width: 420; height: 260
    visible: true
    title: "Hydrostatic calculator (QML)"
    // exposes to Python the object created below (not a QObject child of the window)
    property QtObject tank: tankQml

    Tank { id: tankQml; diameter: 3.0; level: 2.5 }  // type defined in Python

    ColumnLayout {
        anchors.fill: parent; anchors.margins: 16; spacing: 10
        RowLayout {
            Label { text: "Depth (m):" }
            SpinBox { id: depth; objectName: "depth"; from: 0; to: 3000; stepSize: 50
                      value: 1350; editable: true }
        }
        Label {  // binding: re-evaluated when depth.value or Calculator.unit change
            objectName: "pressureLabel"
            text: "Pressure: " + Calculator.pressure(depth.value).toFixed(2) + " "
                  + Calculator.unit
        }
        Label {
            objectName: "volumeLabel"
            text: "Tank volume: " + tankQml.volume.toFixed(3) + " m³"
        }
        Button { objectName: "unitButton"; text: "Toggle bar/psi"
                 onClicked: Calculator.toggleUnit() }
        Label { id: notice; objectName: "noticeLabel"; color: "#C00000" }
    }
    Connections {  // Python signal -> handler in QML
        target: Calculator
        function onNotice(text) { notice.text = text }
    }
}
