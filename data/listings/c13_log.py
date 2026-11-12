"""Mensagens do Qt redirecionadas ao módulo logging (qInstallMessageHandler)."""

import logging
import sys

from PyQt6.QtCore import (
    QLoggingCategory,
    QtMsgType,
    qCritical,
    qInstallMessageHandler,
    qWarning,
)
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(levelname)-8s %(name)s: %(message)s",
)
log_qt = logging.getLogger("qt")
NIVEL = {
    QtMsgType.QtDebugMsg: logging.DEBUG,
    QtMsgType.QtInfoMsg: logging.INFO,
    QtMsgType.QtWarningMsg: logging.WARNING,
    QtMsgType.QtCriticalMsg: logging.ERROR,
    QtMsgType.QtFatalMsg: logging.CRITICAL,
}


def manipulador(tipo: QtMsgType, contexto, mensagem: str) -> None:
    categoria = contexto.category or "default"
    log_qt.log(NIVEL[tipo], "[%s] %s", categoria, mensagem)


if __name__ == "__main__":
    # a partir daqui, tudo passa pelo logging
    qInstallMessageHandler(manipulador)
    app = QApplication(sys.argv)
    # No PyQt6, qWarning()/qCritical() aceitam apenas texto ASCII (acentos geram
    # UnicodeEncodeError); para mensagens em português, use o módulo logging.
    qWarning("aviso emitido pelo codigo Python")
    qCritical("erro critico simulado")
    QLoggingCategory.setFilterRules("qt.qpa.*=false")  # silencia uma categoria do Qt
    pintor = QPainter()
    # dispositivo nulo: o próprio Qt emite um aviso
    pintor.begin(QPixmap())
    logging.getLogger("app").info("aplicação encerrada normalmente")
