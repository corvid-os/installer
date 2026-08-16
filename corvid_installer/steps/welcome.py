import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LANGUAGES = ["English", "Polski", "Deutsch", "Español", "Français"]


class WelcomeStep(InstallStep):
    id = "welcome"
    title = "Welcome"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Language")

        model = Gtk.StringList.new(LANGUAGES)
        row = Adw.ComboRow(title="Installer and system language", model=model)
        row.set_selected(LANGUAGES.index(state.language))

        def on_selected(combo_row, _pspec):
            state.language = LANGUAGES[combo_row.get_selected()]

        row.connect("notify::selected", on_selected)
        group.add(row)

        return build_step_page(
            icon_name="preferences-desktop-locale-symbolic",
            title="Welcome to Corvid OS",
            subtitle=(
                "This wizard will walk you through the install. "
                "Pick a language to get started."
            ),
            groups=[group],
        )
