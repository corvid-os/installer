import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

TIMEZONES = ["Europe/Warsaw", "Europe/Berlin", "Europe/London", "America/New_York"]
LOCALES = ["pl_PL.UTF-8", "en_US.UTF-8", "de_DE.UTF-8"]


class LocaleStep(InstallStep):
    id = "locale"
    title = "Strefa czasowa i lokalizacja"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Wykryto automatycznie",
            description="Możesz zmienić, jeśli wykrywanie po IP się pomyliło.",
        )

        tz_model = Gtk.StringList.new(TIMEZONES)
        tz_row = Adw.ComboRow(title="Strefa czasowa", model=tz_model)
        group.add(tz_row)

        locale_model = Gtk.StringList.new(LOCALES)
        locale_row = Adw.ComboRow(title="Lokalizacja (format daty/waluty)", model=locale_model)
        group.add(locale_row)

        return build_step_page(
            icon_name="preferences-system-time-symbolic",
            title="Strefa czasowa i lokalizacja",
            subtitle="",
            groups=[group],
        )
