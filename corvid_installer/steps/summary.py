import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

PROFILE_KEYS = {
    "gaming": "profile.gaming",
    "dev": "profile.dev",
    "both": "profile.both",
    "minimal": "profile.minimal",
}


class SummaryStep(InstallStep):
    id = "summary"
    title = "Summary"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title=tr(state, "summary.group_title"),
            description=tr(state, "summary.group_desc"),
        )

        network_value = state.wifi_ssid or (
            tr(state, "summary.value.connected") if state.network_connected else tr(state, "summary.value.none")
        )
        rows = [
            (tr(state, "summary.label.language"), state.language),
            (tr(state, "summary.label.keyboard"), state.keyboard_layout),
            (tr(state, "summary.label.network"), network_value),
            (tr(state, "summary.label.disk"), state.disk or tr(state, "summary.value.auto_disk")),
            (tr(state, "summary.label.partitioning_mode"), state.partitioning_mode),
            (
                tr(state, "summary.label.encryption"),
                tr(state, "summary.value.enabled") if state.encrypt else tr(state, "summary.value.disabled"),
            ),
            (tr(state, "summary.label.timezone"), state.timezone),
            (tr(state, "summary.label.desktop_environment"), state.desktop_environment.upper()),
            (tr(state, "summary.label.profile"), tr(state, PROFILE_KEYS.get(state.profile, "profile.minimal"))),
            (tr(state, "summary.label.user"), state.username or tr(state, "summary.value.not_set")),
            (
                tr(state, "summary.label.administrator"),
                tr(state, "summary.value.yes") if state.is_admin else tr(state, "summary.value.no"),
            ),
            (
                tr(state, "summary.label.snapshots"),
                tr(
                    state,
                    "summary.value.snapshots_line",
                    hourly=state.snapshots_hourly,
                    daily=state.snapshots_daily,
                    weekly=state.snapshots_weekly,
                    monthly=state.snapshots_monthly,
                ),
            ),
        ]

        for label, value in rows:
            row = Adw.ActionRow(title=label, subtitle=str(value))
            group.add(row)

        return build_step_page(
            icon_name="checkbox-checked-symbolic",
            title=tr(state, "summary.title"),
            subtitle="",
            groups=[group],
        )
