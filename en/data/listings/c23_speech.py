# runner: ticks=60
"""QTextToSpeech: engines, voices, languages, speech queue and states."""

import sys

from PyQt6.QtCore import QLocale, QTimer
from PyQt6.QtTextToSpeech import QTextToSpeech
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    engines = QTextToSpeech.availableEngines()
    print("Available engines:", engines)
    # In production, use the system's default engine: QTextToSpeech().
    # "mock" is the test engine shipped with Qt: simulated, deterministic speech.
    speech = QTextToSpeech("mock")
    print(f"Engine: {speech.engine()}; state: {speech.state().name}")
    print("Languages:", [loc.name() for loc in speech.availableLocales()])
    print(
        "Voices:",
        [(v.name(), v.gender().name, v.age().name) for v in speech.availableVoices()],
    )
    portuguese = [
        v
        for v in speech.availableVoices()
        if v.locale().language() == QLocale.Language.Portuguese
    ]
    print("Portuguese voices in this engine's current locale:", len(portuguese))
    speech.setRate(0.2)  # -1.0 (slow) to 1.0 (fast)
    speech.setPitch(0.0)
    speech.setVolume(0.9)
    target = speech.availableVoices()[-1]
    speech.setVoice(target)
    print(f"Chosen voice: {speech.voice().name()} ({speech.voice().locale().name()})")
    speech.stateChanged.connect(lambda s: print("  state ->", s.name))
    speech.errorOccurred.connect(lambda e, msg: print("  error:", e.name, msg))
    ids = [
        speech.enqueue("Annulus pressure stabilized."),
        speech.enqueue("Start the leak test."),
    ]
    print("Identifiers returned by enqueue():", ids)

    def finish() -> None:
        print("Final state:", speech.state().name)
        app.quit()

    QTimer.singleShot(3000, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
