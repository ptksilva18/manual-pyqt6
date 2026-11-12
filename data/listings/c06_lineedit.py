"""QLineEdit: validadores, máscara, modo de eco e autocompletar."""
import sys

from PyQt6.QtCore import QLocale, QRegularExpression, Qt
from PyQt6.QtGui import QDoubleValidator, QRegularExpressionValidator, QValidator
from PyQt6.QtWidgets import QApplication, QCompleter, QLineEdit

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1) Validador numérico: 0 a 690 bar, até 2 casas, notação padrão
    pressao = QLineEdit()
    v = QDoubleValidator(0.0, 690.0, 2)
    v.setNotation(QDoubleValidator.Notation.StandardNotation)
    v.setLocale(QLocale.c())          # ponto decimal, independente do idioma do sistema
    pressao.setValidator(v)
    for txt in ("345.5", "345.555", "700", "abc"):
        estado, _, _ = v.validate(txt, 0)
        print(f"validar {txt!r:10} -> {estado.name}")

    # 2) Expressão regular: tag no formato AA-999
    tag = QLineEdit()
    tag.setValidator(QRegularExpressionValidator(QRegularExpression(r"[A-Z]{2}-\d{3}")))
    estado, _, _ = tag.validator().validate("PT-101", 0)
    aceitavel = estado == QValidator.State.Acceptable
    print("tag 'PT-101' ->", estado.name, "| aceitável?", aceitavel)

    # 3) Máscara de entrada: data dd/mm/aaaa
    data = QLineEdit()
    data.setInputMask("99/99/9999;_")
    data.setText("11112026")
    print("máscara aplicada:", data.text(), "| completa?", data.hasAcceptableInput())

    # 4) Senha e placeholder
    senha = QLineEdit(placeholderText="senha")
    senha.setEchoMode(QLineEdit.EchoMode.Password)
    senha.setText("s3gr3do")
    print("texto real:", senha.text(), "| exibido:", senha.displayText())

    # 5) Autocompletar
    pocos = ["PX-001", "PX-002", "PY-010", "PZ-123"]
    busca = QLineEdit()
    comp = QCompleter(pocos)
    comp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    busca.setCompleter(comp)
    comp.setCompletionPrefix("px")
    modelo = comp.completionModel()
    sugestoes = [modelo.index(i, 0).data() for i in range(comp.completionCount())]
    print("sugestões para 'px':", sugestoes)
