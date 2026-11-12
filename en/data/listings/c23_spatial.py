# runner: ticks=40 env=QT_AUDIO_BACKEND:pulseaudio
"""QtSpatialAudio: engine, listener and sound sources positioned in 3D."""

import math
import os
import struct
import sys
import tempfile
import wave

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QQuaternion, QVector3D
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtSpatialAudio import QAudioEngine, QAudioListener, QAudioRoom, QSpatialSound
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    file_name = os.path.join(tempfile.mkdtemp(), "beep.wav")
    with wave.open(file_name, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48_000)
        w.writeframes(
            b"".join(
                struct.pack("<h", int(9_000 * math.sin(2 * math.pi * 880 * i / 48_000)))
                for i in range(4_800)
            )
        )
    engine = QAudioEngine()
    engine.setOutputMode(QAudioEngine.OutputMode.Headphone)  # binaural rendering
    engine.setDistanceScale(
        QAudioEngine.DistanceScaleMeter
    )  # position units in meters
    listener = QAudioListener(engine)
    listener.setPosition(QVector3D(0.0, 0.0, 0.0))
    listener.setRotation(QQuaternion())
    room = QAudioRoom(engine)  # reflections and reverberation of a rectangular room
    room.setDimensions(QVector3D(12.0, 3.0, 8.0))  # meters
    room.setWallMaterial(
        QAudioRoom.Wall.Floor, QAudioRoom.Material.ConcreteBlockPainted
    )
    alarm = QSpatialSound(engine)
    alarm.setSource(QUrl.fromLocalFile(file_name))
    alarm.setPosition(QVector3D(3.0, 0.0, -4.0))  # 3 m to the right, 4 m ahead
    alarm.setDistanceModel(QSpatialSound.DistanceModel.Logarithmic)
    alarm.setLoops(
        QSpatialSound.Loops.Infinite.value
    )  # setLoops() takes an int in PyQt6

    def xyz(v: QVector3D) -> str:
        return f"({v.x():g}, {v.y():g}, {v.z():g})"

    print(
        f"Output mode: {engine.outputMode().name}; distanceScale = "
        f"{engine.distanceScale():g} cm per unit (units in meters)"
    )
    print(
        f"Source at {xyz(alarm.position())}; distance to the listener = "
        f"{alarm.position().distanceToPoint(listener.position()):.1f} m"
    )
    print(
        f"Room {xyz(room.dimensions())} m; floor: "
        f"{room.wallMaterial(QAudioRoom.Wall.Floor).name}"
    )
    if QMediaDevices.audioOutputs():
        engine.start()
        print("Engine started; paused =", engine.paused())
        engine.stop()
    else:
        print("No audio output device: engine not started.")
    # Destroy sources, room and listener before the engine: in the test (PyQt6 6.12),
    # leaving the order to the garbage collector ended the process with a segmentation
    # fault on exit.
    del alarm, room, listener
    del engine
    return 0


if __name__ == "__main__":
    sys.exit(main())
