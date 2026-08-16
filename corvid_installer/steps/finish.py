import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class FinishStep(InstallStep):
    id = "finish"
    title = "Finish"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup()

        restart_row = Adw.ActionRow(
            title="Restart now",
            subtitle="Close the live session and boot into the newly installed Corvid OS",
            activatable=True,
        )
        restart_row.add_suffix(Gtk.Image.new_from_icon_name("system-reboot-symbolic"))
        group.add(restart_row)

        stay_row = Adw.ActionRow(
            title="Stay in the live session",
            subtitle="Keep testing before you restart",
            activatable=True,
        )
        group.add(stay_row)

        return build_step_page(
            icon_name="emblem-ok-symbolic",
            title="Corvid OS is installed",
            subtitle="(simulated — this skeleton doesn't actually restart anything)",
            groups=[group],
        )
