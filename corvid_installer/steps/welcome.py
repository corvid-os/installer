import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LANGUAGES = ["Polski", "English", "Deutsch", "Español", "Français"]


class WelcomeStep(InstallStep):
    id = "welcome"
    title = "Powitanie"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Język")

        model = Gtk.StringList.new(LANGUAGES)
        row = Adw.ComboRow(title="Język instalatora i systemu", model=model)
        row.set_selected(LANGUAGES.index(state.language))

        def on_selected(combo_row, _pspec):
            state.language = LANGUAGES[combo_row.get_selected()]

        row.connect("notify::selected", on_selected)
        group.add(row)

        return build_step_page(
            icon_name="preferences-desktop-locale-symbolic",
            title="Witaj w Corvid OS",
            subtitle=(
                "Ten kreator przeprowadzi Cię przez instalację. "
                "Wybierz język, żeby zacząć."
            ),
            groups=[group],
        )
