import QtQuick
import QtGraphs

Rectangle {
    id: raiz
    color: "white"

    GraphsView {
        anchors.fill: parent
        anchors.margins: 8
        theme: GraphsTheme {
            colorScheme: GraphsTheme.ColorScheme.Light
            seriesColors: ["#2E75B6", "#C55A11"]
            grid.mainColor: "#D0D0D0"
        }
        axisX: ValueAxis { objectName: "eixoX"; min: 0; max: 3000; tickInterval: 500
                           labelFormat: "%.0f"; titleText: "Profundidade (m)" }
        axisY: ValueAxis { objectName: "eixoY"; min: 0; max: 600; tickInterval: 100
                           labelFormat: "%.0f"; titleText: "Pressão (bar)" }

        LineSeries { objectName: "hidrostatica"; name: "Hidrostática"; width: 3 }
        ScatterSeries { objectName: "medida"; name: "Medida (RFT)" }
    }
}
