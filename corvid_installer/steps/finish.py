import subprocess

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.backend.priv import as_root
from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class FinishStep(InstallStep):
    id = "finish"
    title = "Finish"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup()

        restart_row = Adw.ActionRow(
            title=tr(state, "finish.restart_title"),
            subtitle=tr(state, "finish.restart_subtitle"),
            activatable=True,
        )
        restart_row.add_suffix(Gtk.Image.new_from_icon_name("system-reboot-symbolic"))
        restart_row.connect("activated", self._on_restart, state)
        group.add(restart_row)

        stay_row = Adw.ActionRow(
            title=tr(state, "finish.stay_title"),
            subtitle=tr(state, "finish.stay_subtitle"),
            activatable=True,
        )
        stay_row.connect("activated", self._on_stay)
        group.add(stay_row)

        subtitle_key = "finish.subtitle_dry_run" if state.dry_run else "finish.subtitle_done"
        return build_step_page(
            icon_name="emblem-ok-symbolic",
            title=tr(state, "finish.title"),
            subtitle=tr(state, subtitle_key),
            groups=[group],
        )

    def _on_restart(self, _row, state: InstallState) -> None:
        if state.dry_run:
            # Dry run also covers "just poking at the UI outside a VM" (see
            # main.py) -- never actually reboot the machine running this.
            print("[dry-run] would run: reboot")
            return
        # Fire-and-forget: don't block the GTK main loop waiting on a
        # command whose whole point is to end this session.
        subprocess.Popen(as_root(["reboot"]))

    def _on_stay(self, _row) -> None:
        if self.request_close:
            self.request_close()
