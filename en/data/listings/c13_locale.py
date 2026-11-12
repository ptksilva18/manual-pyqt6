"""QLocale: formatting and parsing numbers, dates and currency per language."""

from PyQt6.QtCore import QDate, QLocale

br = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
us = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
d = QDate(2026, 11, 11)

for name, loc in (("pt_BR", br), ("en_US", us)):
    print(
        f"{name}: {loc.toString(1234567.891, 'f', 2):>14} | "
        f"{loc.toString(d, QLocale.FormatType.ShortFormat):>10} | "
        f"{loc.toCurrencyString(1500.5)}"
    )

value, ok = br.toDouble("1.234,5")
print("pt_BR.toDouble('1.234,5') ->", (value, ok))
value, ok = br.toDouble("1234.5")
print("pt_BR.toDouble('1234.5')  ->", (value, ok))
print(
    "pt_BR decimal separator:",
    repr(br.decimalPoint()),
    "| thousands:",
    repr(br.groupSeparator()),
)
print("native language name:", br.nativeLanguageName(), "/", br.nativeTerritoryName())
