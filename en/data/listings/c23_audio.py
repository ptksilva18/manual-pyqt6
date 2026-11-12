# runner: ticks=60 env=QT_AUDIO_BACKEND:pulseaudio
"""Audio playback and decoding: QMediaPlayer, QAudioOutput, QAudioDecoder."""

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


def make_wav(
    path: str, freq_hz: float = 440.0, duration_s: float = 0.5, rate: int = 44_100
) -> None:
    n = int(rate * duration_s)
    frames = b"".join(
        struct.pack("<h", int(12_000 * math.sin(2 * math.pi * freq_hz * i / rate)))
        for i in range(n)
    )
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)


def main() -> int:
    app = QApplication(sys.argv)
    folder = tempfile.mkdtemp()
    file_name = os.path.join(folder, "alarm.wav")
    make_wav(file_name)
    url = QUrl.fromLocalFile(file_name)

    outputs = QMediaDevices.audioOutputs()
    print(
        f"Audio outputs: {len(outputs)}; default: "
        f"{QMediaDevices.defaultAudioOutput().description() or '(none)'}"
    )

    player = QMediaPlayer()
    output = QAudioOutput()
    output.setVolume(0.8)  # 0.0 to 1.0 (linear scale)
    player.setAudioOutput(output)  # without an output, the player makes no sound
    player.mediaStatusChanged.connect(lambda s: print(f"  player: {s.name}"))
    player.errorOccurred.connect(
        lambda e, msg: print(f"  player: error {e.name}: {msg}")
    )
    player.durationChanged.connect(lambda ms: print(f"  player: duration = {ms} ms"))
    player.setSource(url)
    player.play()

    decoder = QAudioDecoder()
    decoder.setSource(url)
    stats = {"buffers": 0, "frames": 0, "peak": 0}

    def buffer_ready() -> None:
        buf: QAudioBuffer = decoder.read()
        samples = struct.unpack(
            f"<{buf.sampleCount()}h", buf.constData().asstring(buf.byteCount())
        )
        stats["buffers"] += 1
        stats["frames"] += buf.frameCount()
        stats["peak"] = max(stats["peak"], max(abs(a) for a in samples))
        stats["format"] = buf.format()

    def decoded() -> None:
        fmt = stats["format"]
        print(
            f"Decoder: {stats['buffers']} buffers, {stats['frames']} frames, "
            f"{fmt.sampleRate()} Hz, {fmt.channelCount()} channel, "
            f"{fmt.sampleFormat().name}; "
            f"peak = {stats['peak']} (generated amplitude: 12000)"
        )

    decoder.bufferReady.connect(buffer_ready)
    decoder.finished.connect(decoded)
    decoder.start()

    def finish() -> None:
        print(
            f"Final player state: {player.playbackState().name}, "
            f"status {player.mediaStatus().name}"
        )
        app.quit()

    QTimer.singleShot(2500, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
