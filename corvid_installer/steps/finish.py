import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

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
        group.add(restart_row)

        stay_row = Adw.ActionRow(
            title=tr(state, "finish.stay_title"),
            subtitle=tr(state, "finish.stay_subtitle"),
            activatable=True,
        )
        group.add(stay_row)

        return build_step_page(
            icon_name="emblem-ok-symbolic",
            title=tr(state, "finish.title"),
            subtitle=tr(state, "finish.subtitle"),
            groups=[group],
        )
