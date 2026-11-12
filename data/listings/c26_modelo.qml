import QtQuick
import QtQuick.Controls

ListView {
    id: lista
    width: 360; height: 220
    model: modeloPocos                       // propriedade de contexto definida no Python
    spacing: 4
    delegate: Rectangle {
        required property string nome         // papéis do modelo (roleNames) como
        required property real lamina         //   propriedades obrigatórias do delegate
        required property bool ativo
        width: ListView.view.width; height: 36; radius: 4
        color: ativo ? "#EAF1FA" : "#F2F2F2"
        Text { anchors.verticalCenter: parent.verticalCenter; x: 10
               text: nome + " — LDA " + lamina.toFixed(0) + " m"
                     + (ativo ? "" : " (inativo)") }
    }
}
