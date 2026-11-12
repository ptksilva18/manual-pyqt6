"""QSplashScreen durante a inicialização."""
import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    imagem = QPixmap(400, 200)
    imagem.fill(QColor("#1F3864"))
    splash = QSplashScreen(imagem)
    splash.show()
    for etapa in ("Carregando configurações…", "Conectando ao banco…", "Pronto."):
        alinhamento = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        splash.showMessage(etapa, alinhamento, QColor("white"))
        app.processEvents()                 # mantém a splash responsiva
        time.sleep(0.05)                    # simula trabalho de inicialização
        print(etapa)
    janela = QMainWindow()
    janela.show()
    splash.finish(janela)                   # some quando a janela principal aparece
    print("splash visível?", splash.isVisible())
    sys.exit(app.exec())
