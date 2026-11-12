"""Qt messages redirected to the logging module (qInstallMessageHandler)."""

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
qt_log = logging.getLogger("qt")
LEVEL = {
    QtMsgType.QtDebugMsg: logging.DEBUG,
    QtMsgType.QtInfoMsg: logging.INFO,
    QtMsgType.QtWarningMsg: logging.WARNING,
    QtMsgType.QtCriticalMsg: logging.ERROR,
    QtMsgType.QtFatalMsg: logging.CRITICAL,
}


def handler(msg_type: QtMsgType, context, message: str) -> None:
    category = context.category or "default"
    qt_log.log(LEVEL[msg_type], "[%s] %s", category, message)


if __name__ == "__main__":
    # from here on, everything goes through logging
    qInstallMessageHandler(handler)
    app = QApplication(sys.argv)
    # In PyQt6, qWarning()/qCritical() accept only ASCII text (accented letters raise
    # UnicodeEncodeError); for non-ASCII messages, use the logging module.
    qWarning("warning emitted by the Python code")
    qCritical("simulated critical error")
    QLoggingCategory.setFilterRules("qt.qpa.*=false")  # silences a Qt category
    painter = QPainter()
    # null device: Qt itself emits a warning
    painter.begin(QPixmap())
    logging.getLogger("app").info("application finished normally")
