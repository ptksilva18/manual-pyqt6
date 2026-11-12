import QtQuick
import QtQuick3D

View3D {
    id: view
    property real lidAngle: 0             // controlled by Python
    environment: SceneEnvironment {
        clearColor: "#1E2F40"
        backgroundMode: SceneEnvironment.Color
        antialiasingMode: SceneEnvironment.MSAA
    }
    PerspectiveCamera { position: Qt.vector3d(0, 120, 380); eulerRotation.x: -15 }
    DirectionalLight { eulerRotation.x: -40; eulerRotation.y: -30; brightness: 1.2 }

    Model {                                // equipment body
        objectName: "body"
        source: "#Cylinder"
        scale: Qt.vector3d(1.2, 1.6, 1.2)
        materials: PrincipledMaterial {
            baseColor: "#C55A11"; metalness: 0.6; roughness: 0.35
        }
    }
    Model {                                // hinged lid
        objectName: "lid"
        source: "#Cube"
        position: Qt.vector3d(0, 95, 0)
        eulerRotation.y: view.lidAngle
        scale: Qt.vector3d(1.6, 0.2, 1.6)
        materials: PrincipledMaterial {
            baseColor: "#2E75B6"; metalness: 0.3; roughness: 0.5
        }
    }
}
