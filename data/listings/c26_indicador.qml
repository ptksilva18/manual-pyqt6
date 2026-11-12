import QtQuick
import QtQuick.Shapes

Item {
    id: raiz
    property real valor: 0          // definido pelo Python (QSlider)
    property real maximo: 400
    signal alarme(real valor)       // emitido para o Python
    implicitWidth: 260; implicitHeight: 200
    onValorChanged: if (valor > 0.8 * maximo) alarme(valor)

    Shape {
        anchors.fill: parent
        ShapePath {                 // arco de fundo
            strokeColor: "#D9D9D9"; strokeWidth: 18; fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            PathAngleArc { centerX: raiz.width / 2; centerY: raiz.height * 0.75
                           radiusX: 100; radiusY: 100; startAngle: 180; sweepAngle: 180 }
        }
        ShapePath {                 // arco proporcional ao valor
            strokeColor: raiz.valor > 0.8 * raiz.maximo ? "#C00000" : "#2E75B6"
            strokeWidth: 18; fillColor: "transparent"; capStyle: ShapePath.RoundCap
            PathAngleArc { centerX: raiz.width / 2; centerY: raiz.height * 0.75
                           radiusX: 100; radiusY: 100; startAngle: 180
                           sweepAngle: 180 * Math.min(raiz.valor / raiz.maximo, 1) }
        }
    }
    Text {
        objectName: "leitura"
        anchors.horizontalCenter: parent.horizontalCenter; y: raiz.height * 0.55
        font.pixelSize: 28; font.bold: true
        text: raiz.valor.toFixed(0) + " bar"
    }
    Behavior on valor { NumberAnimation { duration: 150 } }   // transição suave
}
