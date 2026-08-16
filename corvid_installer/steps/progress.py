"""Krok instalacji. W tym szkielecie tylko SYMULUJE postęp (GLib.timeout) —
prawdziwe wywołania pacstrap/genfstab/chroot/snapper przyjdą wraz z backendem."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

FAKE_STAGES = [
    "Partycjonowanie dysku…",
    "Formatowanie subwolumenów Btrfs…",
    "pacstrap — instalacja pakietów bazowych…",
    "genfstab — zapis fstab…",
    "Konfiguracja w chroot (locale, użytkownik, bootloader)…",
    "Instalacja GRUB…",
    "Inicjalizacja snapper…",
    "Sprzątanie i finalizacja…",
]


class ProgressStep(InstallStep):
    id = "progress"
    title = "Instalacja"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        self._progress_bar = Gtk.ProgressBar(show_text=True)
        box.append(self._progress_bar)

        log_scroller = Gtk.ScrolledWindow(min_content_height=180, vexpand=True)
        self._log_view = Gtk.TextView(editable=False, cursor_visible=False)
        self._log_view.add_css_class("monospace")
        log_scroller.set_child(self._log_view)
        box.append(log_scroller)

        group.add(box)

        self._stage_index = 0
        self._append_log("(symulacja — backend jeszcze niezaimplementowany)")
        GLib.timeout_add(600, self._advance)

        return build_step_page(
            icon_name="emblem-system-symbolic",
            title="Trwa instalacja",
            subtitle="Nie wyłączaj komputera.",
            groups=[group],
        )

    def _append_log(self, text: str) -> None:
        buf = self._log_view.get_buffer()
        buf.insert(buf.get_end_iter(), text + "\n")

    def _advance(self) -> bool:
        if self._stage_index >= len(FAKE_STAGES):
            self._progress_bar.set_fraction(1.0)
            self._progress_bar.set_text("Gotowe")
            self._append_log("Instalacja (symulowana) zakończona.")
            return GLib.SOURCE_REMOVE

        stage = FAKE_STAGES[self._stage_index]
        self._append_log(stage)
        self._stage_index += 1
        self._progress_bar.set_fraction(self._stage_index / len(FAKE_STAGES))
        self._progress_bar.set_text(stage)
        return GLib.SOURCE_CONTINUE
