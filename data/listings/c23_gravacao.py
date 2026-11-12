# runner: ticks=80 env=QT_AUDIO_BACKEND:pulseaudio
"""Captura: QMediaCaptureSession com câmera (se houver) e gravação de áudio gerado pelo
app."""

import math
import os
import struct
import sys
import tempfile
import wave

from PyQt6.QtCore import QByteArray, QTimer, QUrl
from PyQt6.QtMultimedia import (
    QAudioBuffer,
    QAudioBufferInput,
    QAudioFormat,
    QCamera,
    QImageCapture,
    QMediaCaptureSession,
    QMediaDevices,
    QMediaFormat,
    QMediaRecorder,
)
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    modo = QMediaFormat.ConversionMode.Encode
    print(
        "Contêineres para gravação:",
        [f.name for f in QMediaFormat().supportedFileFormats(modo)],
    )
    print(
        "Codecs de áudio:", [c.name for c in QMediaFormat().supportedAudioCodecs(modo)]
    )

    cameras = QMediaDevices.videoInputs()
    print(f"Câmeras: {len(cameras)}; microfones: {len(QMediaDevices.audioInputs())}")
    if cameras:  # caminho com hardware: visualização, foto e vídeo
        sessao_cam = QMediaCaptureSession()
        camera = QCamera(cameras[0])
        sessao_cam.setCamera(camera)
        sessao_cam.setImageCapture(QImageCapture())
        camera.start()

    # Sem microfone, o próprio app fornece as amostras (Qt 6.8+: QAudioBufferInput).
    fmt = QAudioFormat()
    fmt.setSampleRate(16_000)
    fmt.setChannelCount(1)
    fmt.setSampleFormat(QAudioFormat.SampleFormat.Int16)
    entrada = QAudioBufferInput(fmt)
    sessao = QMediaCaptureSession()
    sessao.setAudioBufferInput(entrada)
    gravador = QMediaRecorder()
    sessao.setRecorder(gravador)
    formato = QMediaFormat()
    formato.setFileFormat(QMediaFormat.FileFormat.Wave)
    formato.setAudioCodec(QMediaFormat.AudioCodec.Wave)
    gravador.setMediaFormat(formato)
    destino = os.path.join(tempfile.mkdtemp(), "registro.wav")
    gravador.setOutputLocation(QUrl.fromLocalFile(destino))

    enviados = [0]
    blocos, amostras_por_bloco = 10, 1_600  # 10 x 0,1 s = 1 s de áudio

    def enviar() -> None:
        k = enviados[0]
        if k >= blocos:
            entrada.readyToSendAudioBuffer.disconnect(enviar)
            gravador.stop()
            return
        dados = b"".join(
            struct.pack(
                "<h",
                int(
                    8_000
                    * math.sin(
                        2 * math.pi * 440 * (k * amostras_por_bloco + i) / 16_000
                    )
                ),
            )
            for i in range(amostras_por_bloco)
        )
        entrada.sendAudioBuffer(QAudioBuffer(QByteArray(dados), fmt))
        enviados[0] += 1

    entrada.readyToSendAudioBuffer.connect(enviar)
    # No PyQt6 6.12, recorderStateChanged e errorOccurred do QMediaRecorder não conectam
    # (assinatura do sinal não encontrada); o estado é acompanhado por consulta periódica.
    verificador = QTimer()

    def verificar() -> None:
        if gravador.error() != QMediaRecorder.Error.NoError:
            print("Erro de gravação:", gravador.errorString())
            app.quit()
        elif (
            enviados[0] >= blocos
            and gravador.recorderState() == QMediaRecorder.RecorderState.StoppedState
        ):
            verificador.stop()
            with wave.open(gravador.actualLocation().toLocalFile()) as w:
                print(
                    f"Gravado: {os.path.basename(destino)} — {w.getframerate()} Hz, "
                    f"{w.getnchannels()} canal, {w.getnframes()} quadros "
                    f"({w.getnframes() / w.getframerate():.2f} s); "
                    f"duration() = {gravador.duration()} ms"
                )
            app.quit()

    verificador.timeout.connect(verificar)
    verificador.start(100)
    gravador.record()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
