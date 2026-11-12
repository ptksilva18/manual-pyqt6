"""QLocale: formatação e leitura de números, datas e moeda por idioma."""

from PyQt6.QtCore import QDate, QLocale

br = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
us = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
d = QDate(2026, 11, 11)

for nome, loc in (("pt_BR", br), ("en_US", us)):
    print(
        f"{nome}: {loc.toString(1234567.891, 'f', 2):>14} | "
        f"{loc.toString(d, QLocale.FormatType.ShortFormat):>10} | "
        f"{loc.toCurrencyString(1500.5)}"
    )

valor, ok = br.toDouble("1.234,5")
print("pt_BR.toDouble('1.234,5') ->", (valor, ok))
valor, ok = br.toDouble("1234.5")
print("pt_BR.toDouble('1234.5')  ->", (valor, ok))
print(
    "separador decimal pt_BR:",
    repr(br.decimalPoint()),
    "| milhar:",
    repr(br.groupSeparator()),
)
print("nome nativo do idioma:", br.nativeLanguageName(), "/", br.nativeTerritoryName())
