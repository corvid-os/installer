"""Install step. In this skeleton it only SIMULATES progress (GLib.timeout) --
real pacstrap/genfstab/chroot/snapper calls arrive with the backend."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep, Validation
from corvid_installer.ui.page import build_step_page

STAGE_KEYS = [
    "progress.stage.partition",
    "progress.stage.format",
    "progress.stage.pacstrap",
    "progress.stage.genfstab",
    "progress.stage.chroot",
    "progress.stage.grub",
    "progress.stage.snapper",
    "progress.stage.cleanup",
]


class ProgressStep(InstallStep):
    id = "progress"
    title = "Installing"

    _finished = False

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        self._finished = False
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
        self._state = state
        self._append_log(tr(state, "progress.placeholder_log"))
        GLib.timeout_add(600, self._advance)

        return build_step_page(
            icon_name="emblem-system-symbolic",
            title=tr(state, "progress.title"),
            subtitle=tr(state, "progress.subtitle"),
            groups=[group],
        )

    def validate(self, state: InstallState) -> Validation:
        if not self._finished:
            return Validation.error(tr(state, "progress.not_finished"))
        return Validation.ok()

    def _append_log(self, text: str) -> None:
        buf = self._log_view.get_buffer()
        buf.insert(buf.get_end_iter(), text + "\n")

    def _advance(self) -> bool:
        if self._stage_index >= len(STAGE_KEYS):
            self._progress_bar.set_fraction(1.0)
            self._progress_bar.set_text(tr(self._state, "progress.done"))
            self._append_log(tr(self._state, "progress.complete_log"))
            self._finished = True
            if self.request_revalidate:
                self.request_revalidate()
            return GLib.SOURCE_REMOVE

        stage = tr(self._state, STAGE_KEYS[self._stage_index])
        self._append_log(stage)
        self._stage_index += 1
        self._progress_bar.set_fraction(self._stage_index / len(STAGE_KEYS))
        self._progress_bar.set_text(stage)
        return GLib.SOURCE_CONTINUE
