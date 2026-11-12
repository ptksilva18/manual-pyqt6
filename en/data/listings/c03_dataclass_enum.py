"""dataclass + Enum feeding a QComboBox (associated data via userData)."""
import sys
from dataclasses import dataclass, field
from enum import Enum

from PyQt6.QtWidgets import QApplication, QComboBox


class Material(Enum):
    CARBON_STEEL = "Carbon steel"
    SS_316L = "Stainless 316L"
    DUPLEX = "Duplex 2205"


@dataclass(frozen=True)
class Pipe:
    diameter_mm: float
    wall_mm: float
    material: Material = Material.CARBON_STEEL
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def inner_diameter_mm(self) -> float:
        return self.diameter_mm - 2 * self.wall_mm


if __name__ == "__main__":
    app = QApplication(sys.argv)
    combo = QComboBox()
    for m in Material:
        combo.addItem(m.value, userData=m)       # displayed text + associated object
    combo.setCurrentIndex(1)
    chosen: Material = combo.currentData()
    pipe = Pipe(273.1, 12.7, chosen, tags=("service line",))
    print(f"chosen material: {chosen!r}")
    print(f"pipe: OD={pipe.diameter_mm} mm, t={pipe.wall_mm} mm, tags={pipe.tags}")
    print(f"ID = {pipe.inner_diameter_mm:.1f} mm")
    print("immutable?", Pipe.__dataclass_params__.frozen)
