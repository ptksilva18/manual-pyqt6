"""dataclass + Enum alimentando um QComboBox (dado associado com userData)."""
import sys
from dataclasses import dataclass, field
from enum import Enum

from PyQt6.QtWidgets import QApplication, QComboBox


class Material(Enum):
    ACO_CARBONO = "Aço carbono"
    INOX_316L = "Inox 316L"
    DUPLEX = "Duplex 2205"


@dataclass(frozen=True)
class Tubo:
    diametro_mm: float
    espessura_mm: float
    material: Material = Material.ACO_CARBONO
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def diametro_interno_mm(self) -> float:
        return self.diametro_mm - 2 * self.espessura_mm


if __name__ == "__main__":
    app = QApplication(sys.argv)
    combo = QComboBox()
    for m in Material:
        combo.addItem(m.value, userData=m)       # texto exibido + objeto associado
    combo.setCurrentIndex(1)
    escolhido: Material = combo.currentData()
    tubo = Tubo(273.1, 12.7, escolhido, tags=("linha de serviço",))
    print(f"material escolhido: {escolhido!r}")
    print(f"tubo: OD={tubo.diametro_mm} mm, t={tubo.espessura_mm} mm, tags={tubo.tags}")
    print(f"DI = {tubo.diametro_interno_mm:.1f} mm")
    print("imutável?", Tubo.__dataclass_params__.frozen)
