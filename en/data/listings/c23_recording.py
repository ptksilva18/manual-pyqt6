# runner: ticks=80 env=QT_AUDIO_BACKEND:pulseaudio
"""Capture: QMediaCaptureSession with a camera (if any) and recording of audio generated
by the app."""

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
    mode = QMediaFormat.ConversionMode.Encode
    print(
        "Containers for recording:",
        [f.name for f in QMediaFormat().supportedFileFormats(mode)],
    )
    print(
        "Audio codecs:", [c.name for c in QMediaFormat().supportedAudioCodecs(mode)]
    )

    cameras = QMediaDevices.videoInputs()
    print(f"Cameras: {len(cameras)}; microphones: {len(QMediaDevices.audioInputs())}")
    if cameras:  # path with hardware: preview, photo and video
        cam_session = QMediaCaptureSession()
        camera = QCamera(cameras[0])
        cam_session.setCamera(camera)
        cam_session.setImageCapture(QImageCapture())
        camera.start()

    # Without a microphone, the app supplies the samples (Qt 6.8+: QAudioBufferInput).
    fmt = QAudioFormat()
    fmt.setSampleRate(16_000)
    fmt.setChannelCount(1)
    fmt.setSampleFormat(QAudioFormat.SampleFormat.Int16)
    audio_input = QAudioBufferInput(fmt)
    session = QMediaCaptureSession()
    session.setAudioBufferInput(audio_input)
    recorder = QMediaRecorder()
    session.setRecorder(recorder)
    media_format = QMediaFormat()
    media_format.setFileFormat(QMediaFormat.FileFormat.Wave)
    media_format.setAudioCodec(QMediaFormat.AudioCodec.Wave)
    recorder.setMediaFormat(media_format)
    target = os.path.join(tempfile.mkdtemp(), "record.wav")
    recorder.setOutputLocation(QUrl.fromLocalFile(target))

    sent = [0]
    blocks, samples_per_block = 10, 1_600  # 10 x 0.1 s = 1 s of audio

    def send() -> None:
        k = sent[0]
        if k >= blocks:
            audio_input.readyToSendAudioBuffer.disconnect(send)
            recorder.stop()
            return
        data = b"".join(
            struct.pack(
                "<h",
                int(
                    8_000
                    * math.sin(
                        2 * math.pi * 440 * (k * samples_per_block + i) / 16_000
                    )
                ),
            )
            for i in range(samples_per_block)
        )
        audio_input.sendAudioBuffer(QAudioBuffer(QByteArray(data), fmt))
        sent[0] += 1

    audio_input.readyToSendAudioBuffer.connect(send)
    # In PyQt6 6.12, QMediaRecorder's recorderStateChanged and errorOccurred do not
    # connect (signal signature not found); the state is followed by periodic polling.
    checker = QTimer()

    def check() -> None:
        if recorder.error() != QMediaRecorder.Error.NoError:
            print("Recording error:", recorder.errorString())
            app.quit()
        elif (
            sent[0] >= blocks
            and recorder.recorderState() == QMediaRecorder.RecorderState.StoppedState
        ):
            checker.stop()
            with wave.open(recorder.actualLocation().toLocalFile()) as w:
                print(
                    f"Recorded: {os.path.basename(target)} — {w.getframerate()} Hz, "
                    f"{w.getnchannels()} channel, {w.getnframes()} frames "
                    f"({w.getnframes() / w.getframerate():.2f} s); "
                    f"duration() = {recorder.duration()} ms"
                )
            app.quit()

    checker.timeout.connect(check)
    checker.start(100)
    recorder.record()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
