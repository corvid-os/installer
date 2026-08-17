"""Shared interface every install step implements. Adding a step means one
new file in this package plus a line in window.py's step list -- nothing
else changes."""

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
    """Base class for a step. In this skeleton (M1, UI only) validate()
    always passes and apply() is a no-op -- the backend logic comes later."""

    id: str = "step"
    title: str = "Step"

    # Set by the window right before build_widget() is called. Steps whose
    # validity can change from user interaction (e.g. a checkbox) call this
    # to make the Next button re-evaluate sensitivity immediately, instead
    # of only on click.
    request_revalidate: "callable | None" = None

    # Also set by the window. Call this after changing state.language so
    # the window rebuilds the current step (and its own chrome) in the new
    # language, with a crossfade instead of the usual step-to-step slide.
    request_language_refresh: "callable | None" = None

    # Also set by the window. Closes the installer -- used by FinishStep's
    # "stay in the live session" action, which has no other way to reach
    # the window.
    request_close: "callable | None" = None

    def build_widget(self, state: "InstallState") -> Gtk.Widget:
        raise NotImplementedError

    def validate(self, state: "InstallState") -> Validation:
        return Validation.ok()

    def apply(self, state: "InstallState") -> None:
        """Writes the widgets' values into state. Never touches disk/system."""
        pass

    def is_visible(self, state: "InstallState") -> bool:
        return True
