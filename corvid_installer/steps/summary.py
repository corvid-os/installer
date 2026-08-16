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
    "minimal": "Minimal",
}


class SummaryStep(InstallStep):
    id = "summary"
    title = "Summary"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Review your choices before installing",
            description="This is the last chance to go back and change something — "
            "the next step starts writing changes to disk.",
        )

        rows = [
            ("Language", state.language),
            ("Keyboard", state.keyboard_layout),
            ("Network", state.wifi_ssid or ("connected" if state.network_connected else "none")),
            ("Disk", state.disk or "(auto — first one detected)"),
            ("Partitioning mode", state.partitioning_mode),
            ("Encryption", "enabled" if state.encrypt else "disabled"),
            ("Timezone", state.timezone),
            ("Desktop environment", state.desktop_environment.upper()),
            ("Profile", PROFILE_LABELS.get(state.profile, state.profile)),
            ("User", state.username or "(not set)"),
            ("Administrator", "yes" if state.is_admin else "no"),
            (
                "Snapshots",
                f"hourly: {state.snapshots_hourly}, daily: {state.snapshots_daily}, "
                f"weekly: {state.snapshots_weekly}, monthly: {state.snapshots_monthly}",
            ),
        ]

        for label, value in rows:
            row = Adw.ActionRow(title=label, subtitle=str(value))
            group.add(row)

        return build_step_page(
            icon_name="checkbox-checked-symbolic",
            title="Summary",
            subtitle="",
            groups=[group],
        )
