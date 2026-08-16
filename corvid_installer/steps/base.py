"""Wspólny interfejs kroku instalatora. Dodanie nowego kroku = nowy plik
w tym katalogu + wpis na liście kroków w window.py. Zero zmian gdzie indziej."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

if TYPE_CHECKING:
    from corvid_installer.state import InstallState


class ValidationResult(Enum):
    OK = auto()
    ERROR = auto()


@dataclass
class Validation:
    result: ValidationResult
    message: str = ""

    @classmethod
    def ok(cls) -> "Validation":
        return cls(ValidationResult.OK)

    @classmethod
    def error(cls, message: str) -> "Validation":
        return cls(ValidationResult.ERROR, message)


class InstallStep:
    """Bazowa klasa kroku. W tym szkielecie (M1, UI-only) `validate()` zawsze
    zwraca OK, a `apply()` jest no-opem — logika backendu przyjdzie później."""

    id: str = "step"
    title: str = "Krok"

    def build_widget(self, state: "InstallState") -> Gtk.Widget:
        raise NotImplementedError

    def validate(self, state: "InstallState") -> Validation:
        return Validation.ok()

    def apply(self, state: "InstallState") -> None:
        """Zapisuje wybory z widgetów do state. Nie dotyka dysku/systemu."""
        pass

    def is_visible(self, state: "InstallState") -> bool:
        return True
