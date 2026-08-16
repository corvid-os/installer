import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

TIMEZONES = ["UTC", "Europe/London", "Europe/Berlin", "Europe/Warsaw", "America/New_York"]
LOCALES = ["en_US.UTF-8", "en_GB.UTF-8", "de_DE.UTF-8", "pl_PL.UTF-8"]


class LocaleStep(InstallStep):
    id = "locale"
    title = "Timezone and locale"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title=tr(state, "locale.group_title"),
            description=tr(state, "locale.group_desc"),
        )

        tz_model = Gtk.StringList.new(TIMEZONES)
        tz_row = Adw.ComboRow(title=tr(state, "locale.timezone_row"), model=tz_model)
        group.add(tz_row)

        locale_model = Gtk.StringList.new(LOCALES)
        locale_row = Adw.ComboRow(title=tr(state, "locale.locale_row"), model=locale_model)
        group.add(locale_row)

        return build_step_page(
            icon_name="preferences-system-time-symbolic",
            title=tr(state, "locale.title"),
            subtitle="",
            groups=[group],
        )
