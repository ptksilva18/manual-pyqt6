# runner: ticks=40 env=QT_AUDIO_BACKEND:pulseaudio
"""QtSpatialAudio: motor, ouvinte e fontes sonoras posicionadas em 3D."""

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
    arquivo = os.path.join(tempfile.mkdtemp(), "bip.wav")
    with wave.open(arquivo, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48_000)
        w.writeframes(
            b"".join(
                struct.pack("<h", int(9_000 * math.sin(2 * math.pi * 880 * i / 48_000)))
                for i in range(4_800)
            )
        )
    motor = QAudioEngine()
    motor.setOutputMode(QAudioEngine.OutputMode.Headphone)  # renderização binaural
    motor.setDistanceScale(
        QAudioEngine.DistanceScaleMeter
    )  # unidades de posição em metros
    ouvinte = QAudioListener(motor)
    ouvinte.setPosition(QVector3D(0.0, 0.0, 0.0))
    ouvinte.setRotation(QQuaternion())
    sala = QAudioRoom(motor)  # reflexões e reverberação de uma sala retangular
    sala.setDimensions(QVector3D(12.0, 3.0, 8.0))  # metros
    sala.setWallMaterial(
        QAudioRoom.Wall.Floor, QAudioRoom.Material.ConcreteBlockPainted
    )
    alarme = QSpatialSound(motor)
    alarme.setSource(QUrl.fromLocalFile(arquivo))
    alarme.setPosition(QVector3D(3.0, 0.0, -4.0))  # 3 m à direita, 4 m à frente
    alarme.setDistanceModel(QSpatialSound.DistanceModel.Logarithmic)
    alarme.setLoops(
        QSpatialSound.Loops.Infinite.value
    )  # setLoops() recebe int no PyQt6

    def xyz(v: QVector3D) -> str:
        return f"({v.x():g}, {v.y():g}, {v.z():g})"

    print(
        f"Modo de saída: {motor.outputMode().name}; distanceScale = "
        f"{motor.distanceScale():g} cm por unidade (unidades em metros)"
    )
    print(
        f"Fonte em {xyz(alarme.position())}; distância ao ouvinte = "
        f"{alarme.position().distanceToPoint(ouvinte.position()):.1f} m"
    )
    print(
        f"Sala {xyz(sala.dimensions())} m; piso: "
        f"{sala.wallMaterial(QAudioRoom.Wall.Floor).name}"
    )
    if QMediaDevices.audioOutputs():
        motor.start()
        print("Motor iniciado; pausado =", motor.paused())
        motor.stop()
    else:
        print("Sem dispositivo de saída de áudio: motor não iniciado.")
    # Destrua fontes, sala e ouvinte antes do motor: no teste (PyQt6 6.12), deixar a ordem
    # ao coletor de lixo encerrou o processo com falha de segmentação na saída.
    del alarme, sala, ouvinte
    del motor
    return 0


if __name__ == "__main__":
    sys.exit(main())
