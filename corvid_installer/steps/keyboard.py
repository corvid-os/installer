import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LAYOUTS = ["us (English US)", "pl (Polski)", "de (Deutsch)", "fr (Français)"]


class KeyboardStep(InstallStep):
    id = "keyboard"
    title = "Keyboard"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title=tr(state, "keyboard.group_title"))

        model = Gtk.StringList.new(LAYOUTS)
        layout_row = Adw.ComboRow(title=tr(state, "keyboard.layout_row"), model=model)
        group.add(layout_row)

        test_row = Adw.EntryRow(title=tr(state, "keyboard.test_row"))
        group.add(test_row)

        return build_step_page(
            icon_name="input-keyboard-symbolic",
            title=tr(state, "keyboard.title"),
            subtitle=tr(state, "keyboard.subtitle"),
            groups=[group],
        )
