import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

PROFILE_LABELS = {
    "gaming": "Gaming",
    "dev": "Dev",
    "both": "Gaming + Dev",
    "minimal": "Minimalny",
}


class SummaryStep(InstallStep):
    id = "summary"
    title = "Podsumowanie"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Sprawdź wybory przed instalacją",
            description="To ostatni moment żeby cofnąć się i coś zmienić — "
            "kolejny krok zaczyna zapisywać zmiany na dysku.",
        )

        rows = [
            ("Język", state.language),
            ("Klawiatura", state.keyboard_layout),
            ("Sieć", state.wifi_ssid or ("połączono" if state.network_connected else "brak")),
            ("Dysk", state.disk or "(auto — pierwszy wykryty)"),
            ("Tryb partycjonowania", state.partitioning_mode),
            ("Szyfrowanie", "włączone" if state.encrypt else "wyłączone"),
            ("Strefa czasowa", state.timezone),
            ("Środowisko graficzne", state.desktop_environment.upper()),
            ("Profil", PROFILE_LABELS.get(state.profile, state.profile)),
            ("Użytkownik", state.username or "(nie podano)"),
            ("Administrator", "tak" if state.is_admin else "nie"),
            (
                "Snapshoty",
                f"godzinowe: {state.snapshots_hourly}, dzienne: {state.snapshots_daily}, "
                f"tygodniowe: {state.snapshots_weekly}, miesięczne: {state.snapshots_monthly}",
            ),
        ]

        for label, value in rows:
            row = Adw.ActionRow(title=label, subtitle=str(value))
            group.add(row)

        return build_step_page(
            icon_name="checkbox-checked-symbolic",
            title="Podsumowanie",
            subtitle="",
            groups=[group],
        )
