"""Install step. In this skeleton it only SIMULATES progress (GLib.timeout) --
real pacstrap/genfstab/chroot/snapper calls arrive with the backend."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

FAKE_STAGES = [
    "Partitioning the disk…",
    "Formatting Btrfs subvolumes…",
    "pacstrap — installing base packages…",
    "genfstab — writing fstab…",
    "Configuring in chroot (locale, user, bootloader)…",
    "Installing GRUB…",
    "Initializing snapper…",
    "Cleaning up…",
]


class ProgressStep(InstallStep):
    id = "progress"
    title = "Installing"

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
        self._append_log("(simulated — backend not implemented yet)")
        GLib.timeout_add(600, self._advance)

        return build_step_page(
            icon_name="emblem-system-symbolic",
            title="Installing",
            subtitle="Don't turn off your computer.",
            groups=[group],
        )

    def _append_log(self, text: str) -> None:
        buf = self._log_view.get_buffer()
        buf.insert(buf.get_end_iter(), text + "\n")

    def _advance(self) -> bool:
        if self._stage_index >= len(FAKE_STAGES):
            self._progress_bar.set_fraction(1.0)
            self._progress_bar.set_text("Done")
            self._append_log("Install (simulated) complete.")
            return GLib.SOURCE_REMOVE

        stage = FAKE_STAGES[self._stage_index]
        self._append_log(stage)
        self._stage_index += 1
        self._progress_bar.set_fraction(self._stage_index / len(FAKE_STAGES))
        self._progress_bar.set_text(stage)
        return GLib.SOURCE_CONTINUE
