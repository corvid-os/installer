import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LAYOUTS = ["pl (Polski)", "us (English US)", "de (Deutsch)", "fr (Français)"]


class KeyboardStep(InstallStep):
    id = "keyboard"
    title = "Klawiatura"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Układ klawiatury")

        model = Gtk.StringList.new(LAYOUTS)
        layout_row = Adw.ComboRow(title="Układ", model=model)
        group.add(layout_row)

        test_row = Adw.EntryRow(title="Przetestuj tutaj")
        group.add(test_row)

        return build_step_page(
            icon_name="input-keyboard-symbolic",
            title="Układ klawiatury",
            subtitle="Wybierz układ i sprawdź czy znaki wpisują się poprawnie.",
            groups=[group],
        )
