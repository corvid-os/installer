import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LANGUAGES = ["English", "Polski", "Deutsch", "Español", "Français"]

# Purely decorative -- cycles on the welcome screen while the real language
# picker below is a static, functioning-looking dropdown (no logic behind it
# yet, per the M1 skeleton).
HELLOS = [
    "Hello", "Cześć", "Hola", "Bonjour", "Hallo",
    "Ciao", "Olá", "Привет", "こんにちは", "你好", "안녕하세요",
]


class WelcomeStep(InstallStep):
    id = "welcome"
    title = "Welcome"

    _hello_timeout_id = None
    _hello_index = 0

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        if self._hello_timeout_id is not None:
            GLib.source_remove(self._hello_timeout_id)
            self._hello_timeout_id = None

        group = Adw.PreferencesGroup(title="Language")

        model = Gtk.StringList.new(LANGUAGES)
        row = Adw.ComboRow(title="Installer and system language", model=model)
        row.set_selected(LANGUAGES.index(state.language))

        def on_selected(combo_row, _pspec):
            state.language = LANGUAGES[combo_row.get_selected()]

        row.connect("notify::selected", on_selected)
        group.add(row)

        hello_label = Gtk.Label(label=HELLOS[0])
        hello_label.add_css_class("title-1")
        hello_label.add_css_class("accent")

        self._hello_index = 0

        def cycle_hello():
            self._hello_index = (self._hello_index + 1) % len(HELLOS)
            hello_label.set_label(HELLOS[self._hello_index])
            return GLib.SOURCE_CONTINUE

        self._hello_timeout_id = GLib.timeout_add(1100, cycle_hello)
        hello_label.connect("unrealize", lambda *_: self._stop_hello())

        return build_step_page(
            icon_name="preferences-desktop-locale-symbolic",
            title="Welcome to Corvid OS",
            subtitle=(
                "This wizard will walk you through the install. "
                "Pick a language to get started."
            ),
            groups=[group],
            hero_widget=hello_label,
        )

    def _stop_hello(self) -> None:
        if self._hello_timeout_id is not None:
            GLib.source_remove(self._hello_timeout_id)
            self._hello_timeout_id = None
