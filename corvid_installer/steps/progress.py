"""Install step. Runs the real backend (backend/installer.py STAGES) in a
background thread so the GTK main loop stays responsive, and marshals
progress/log updates back via GLib.idle_add. Respects state.dry_run --
see state.py and main.py's --execute flag."""

import threading

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.backend.installer import STAGES
from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep, Validation
from corvid_installer.ui.page import build_step_page


class ProgressStep(InstallStep):
    id = "progress"
    title = "Installing"

    _finished = False
    _failed = False

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        self._finished = False
        self._failed = False
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

        if state.dry_run:
            self._append_log("(dry run -- commands are logged, not executed; pass --execute to actually install)")
        else:
            self._append_log("(LIVE install -- this will write to " + str(state.disk) + ")")

        thread = threading.Thread(target=self._run_stages, args=(state,), daemon=True)
        thread.start()

        return build_step_page(
            icon_name="emblem-system-symbolic",
            title=tr(state, "progress.title"),
            subtitle=tr(state, "progress.subtitle"),
            groups=[group],
        )

    def validate(self, state: InstallState) -> Validation:
        if self._failed:
            return Validation.error("Fix the error above, then go Back and try again.")
        if not self._finished:
            return Validation.error(tr(state, "progress.not_finished"))
        return Validation.ok()

    # -- runs on a background thread --
    def _run_stages(self, state: InstallState) -> None:
        for index, stage in enumerate(STAGES):
            label = tr(state, stage.key)
            GLib.idle_add(self._on_stage_start, label, index, len(STAGES))
            try:
                stage.run(state, lambda msg: GLib.idle_add(self._append_log, msg))
            except Exception as exc:  # noqa: BLE001 -- surface any failure to the log, not just crash silently
                GLib.idle_add(self._on_stage_failed, label, str(exc))
                return
        GLib.idle_add(self._on_all_done, state)

    # -- everything below runs on the main thread via GLib.idle_add --
    def _on_stage_start(self, label: str, index: int, total: int) -> bool:
        self._append_log(label)
        self._progress_bar.set_fraction(index / total)
        self._progress_bar.set_text(label)
        return GLib.SOURCE_REMOVE

    def _on_stage_failed(self, label: str, error: str) -> bool:
        self._append_log(f"FAILED at: {label}")
        self._append_log(f"  {error}")
        self._failed = True
        if self.request_revalidate:
            self.request_revalidate()
        return GLib.SOURCE_REMOVE

    def _on_all_done(self, state: InstallState) -> bool:
        self._progress_bar.set_fraction(1.0)
        self._progress_bar.set_text(tr(state, "progress.done"))
        self._append_log(tr(state, "progress.complete_log"))
        self._finished = True
        if self.request_revalidate:
            self.request_revalidate()
        return GLib.SOURCE_REMOVE

    def _append_log(self, text: str) -> bool:
        buf = self._log_view.get_buffer()
        buf.insert(buf.get_end_iter(), text + "\n")
        return GLib.SOURCE_REMOVE
