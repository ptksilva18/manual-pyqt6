import QtQuick
import QtGraphs

Rectangle {
    id: root
    color: "white"

    GraphsView {
        anchors.fill: parent
        anchors.margins: 8
        theme: GraphsTheme {
            colorScheme: GraphsTheme.ColorScheme.Light
            seriesColors: ["#2E75B6", "#C55A11"]
            grid.mainColor: "#D0D0D0"
        }
        axisX: ValueAxis { objectName: "xAxis"; min: 0; max: 3000; tickInterval: 500
                           labelFormat: "%.0f"; titleText: "Depth (m)" }
        axisY: ValueAxis { objectName: "yAxis"; min: 0; max: 600; tickInterval: 100
                           labelFormat: "%.0f"; titleText: "Pressure (bar)" }

        LineSeries { objectName: "hydrostatic"; name: "Hydrostatic"; width: 3 }
        ScatterSeries { objectName: "measured"; name: "Measured (RFT)" }
    }
}
