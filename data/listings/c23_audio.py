# runner: ticks=60 env=QT_AUDIO_BACKEND:pulseaudio
"""Reprodução e decodificação de áudio: QMediaPlayer, QAudioOutput, QAudioDecoder."""

import math
import os
import struct
import sys
import tempfile
import wave

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import (
    QAudioBuffer,
    QAudioDecoder,
    QAudioOutput,
    QMediaDevices,
    QMediaPlayer,
)
from PyQt6.QtWidgets import QApplication


def gerar_wav(
    caminho: str, freq_hz: float = 440.0, duracao_s: float = 0.5, taxa: int = 44_100
) -> None:
    n = int(taxa * duracao_s)
    quadros = b"".join(
        struct.pack("<h", int(12_000 * math.sin(2 * math.pi * freq_hz * i / taxa)))
        for i in range(n)
    )
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(taxa)
        w.writeframes(quadros)


def main() -> int:
    app = QApplication(sys.argv)
    pasta = tempfile.mkdtemp()
    arquivo = os.path.join(pasta, "alarme.wav")
    gerar_wav(arquivo)
    url = QUrl.fromLocalFile(arquivo)

    saidas = QMediaDevices.audioOutputs()
    print(
        f"Saídas de áudio: {len(saidas)}; padrão: "
        f"{QMediaDevices.defaultAudioOutput().description() or '(nenhuma)'}"
    )

    player = QMediaPlayer()
    saida = QAudioOutput()
    saida.setVolume(0.8)  # 0.0 a 1.0 (escala linear)
    player.setAudioOutput(saida)  # sem saída associada, o player não emite som
    player.mediaStatusChanged.connect(lambda s: print(f"  player: {s.name}"))
    player.errorOccurred.connect(
        lambda e, msg: print(f"  player: erro {e.name}: {msg}")
    )
    player.durationChanged.connect(lambda ms: print(f"  player: duração = {ms} ms"))
    player.setSource(url)
    player.play()

    decodificador = QAudioDecoder()
    decodificador.setSource(url)
    estat = {"buffers": 0, "quadros": 0, "pico": 0}

    def buffer_pronto() -> None:
        buf: QAudioBuffer = decodificador.read()
        amostras = struct.unpack(
            f"<{buf.sampleCount()}h", buf.constData().asstring(buf.byteCount())
        )
        estat["buffers"] += 1
        estat["quadros"] += buf.frameCount()
        estat["pico"] = max(estat["pico"], max(abs(a) for a in amostras))
        estat["formato"] = buf.format()

    def decodificado() -> None:
        fmt = estat["formato"]
        print(
            f"Decodificador: {estat['buffers']} buffers, {estat['quadros']} quadros, "
            f"{fmt.sampleRate()} Hz, {fmt.channelCount()} canal, "
            f"{fmt.sampleFormat().name}; "
            f"pico = {estat['pico']} (amplitude gerada: 12000)"
        )

    decodificador.bufferReady.connect(buffer_pronto)
    decodificador.finished.connect(decodificado)
    decodificador.start()

    def fim() -> None:
        print(
            f"Estado final do player: {player.playbackState().name}, "
            f"status {player.mediaStatus().name}"
        )
        app.quit()

    QTimer.singleShot(2500, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
