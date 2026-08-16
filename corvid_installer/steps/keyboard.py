import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LAYOUTS = ["us (English US)", "pl (Polski)", "de (Deutsch)", "fr (Français)"]


class KeyboardStep(InstallStep):
    id = "keyboard"
    title = "Keyboard"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Keyboard layout")

        model = Gtk.StringList.new(LAYOUTS)
        layout_row = Adw.ComboRow(title="Layout", model=model)
        group.add(layout_row)

        test_row = Adw.EntryRow(title="Test it here")
        group.add(test_row)

        return build_step_page(
            icon_name="input-keyboard-symbolic",
            title="Keyboard layout",
            subtitle="Pick a layout and check that characters type correctly.",
            groups=[group],
        )
