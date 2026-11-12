# runner: ticks=60
"""QTextToSpeech: motores, vozes, idiomas, fila de falas e estados."""

import sys

from PyQt6.QtCore import QLocale, QTimer
from PyQt6.QtTextToSpeech import QTextToSpeech
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    motores = QTextToSpeech.availableEngines()
    print("Motores disponíveis:", motores)
    # Em produção, use o motor padrão do sistema: QTextToSpeech().
    # "mock" é o motor de teste distribuído com o Qt: fala simulada e determinística.
    voz = QTextToSpeech("mock")
    print(f"Motor: {voz.engine()}; estado: {voz.state().name}")
    print("Idiomas:", [loc.name() for loc in voz.availableLocales()])
    print(
        "Vozes:",
        [(v.name(), v.gender().name, v.age().name) for v in voz.availableVoices()],
    )
    portugues = [
        v
        for v in voz.availableVoices()
        if v.locale().language() == QLocale.Language.Portuguese
    ]
    print("Vozes em português na localidade atual deste motor:", len(portugues))
    voz.setRate(0.2)  # -1.0 (lenta) a 1.0 (rápida)
    voz.setPitch(0.0)
    voz.setVolume(0.9)
    alvo = voz.availableVoices()[-1]
    voz.setVoice(alvo)
    print(f"Voz escolhida: {voz.voice().name()} ({voz.voice().locale().name()})")
    voz.stateChanged.connect(lambda s: print("  estado ->", s.name))
    voz.errorOccurred.connect(lambda e, msg: print("  erro:", e.name, msg))
    ids = [
        voz.enqueue("Pressão do anular estabilizada."),
        voz.enqueue("Iniciar o teste de estanqueidade."),
    ]
    print("Identificadores devolvidos por enqueue():", ids)

    def fim() -> None:
        print("Estado final:", voz.state().name)
        app.quit()

    QTimer.singleShot(3000, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
