import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Engenharia 1.0

ApplicationWindow {
    id: janela
    width: 420; height: 260
    visible: true
    title: "Calculadora hidrostática (QML)"
    // expõe ao Python o objeto criado abaixo (ele não é filho QObject da janela)
    property QtObject tanque: tanqueQml

    Tanque { id: tanqueQml; diametro: 3.0; nivel: 2.5 }  // tipo definido em Python

    ColumnLayout {
        anchors.fill: parent; anchors.margins: 16; spacing: 10
        RowLayout {
            Label { text: "Profundidade (m):" }
            SpinBox { id: prof; objectName: "prof"; from: 0; to: 3000; stepSize: 50
                      value: 1350; editable: true }
        }
        Label {  // binding: reavaliado quando prof.value ou Calculadora.unidade mudam
            objectName: "rotuloPressao"
            text: "Pressão: " + Calculadora.pressao(prof.value).toFixed(2) + " "
                  + Calculadora.unidade
        }
        Label {
            objectName: "rotuloVolume"
            text: "Volume do tanque: " + tanqueQml.volume.toFixed(3) + " m³"
        }
        Button { objectName: "botaoUnidade"; text: "Alternar bar/psi"
                 onClicked: Calculadora.alternarUnidade() }
        Label { id: aviso; objectName: "rotuloAviso"; color: "#C00000" }
    }
    Connections {  // sinal Python -> manipulador em QML
        target: Calculadora
        function onAviso(texto) { aviso.text = texto }
    }
}
