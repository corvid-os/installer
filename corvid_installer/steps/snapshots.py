import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


def _spin_row(title: str, value: int, upper: int) -> tuple[Adw.SpinRow, Gtk.Adjustment]:
    adjustment = Gtk.Adjustment(value=value, lower=0, upper=upper, step_increment=1)
    row = Adw.SpinRow(title=title, adjustment=adjustment)
    return row, adjustment


class SnapshotsStep(InstallStep):
    id = "snapshots"
    title = "Snapshots"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Snapshot schedule (snapper)",
            description="Automatic Btrfs snapshots — plus one before and after "
            "every package update (snap-pac), regardless of the schedule below.",
        )

        hourly_row, hourly_adj = _spin_row("Hourly — how many to keep", state.snapshots_hourly, 24)
        daily_row, daily_adj = _spin_row("Daily — how many to keep", state.snapshots_daily, 30)
        weekly_row, weekly_adj = _spin_row("Weekly — how many to keep", state.snapshots_weekly, 12)
        monthly_row, monthly_adj = _spin_row("Monthly — how many to keep", state.snapshots_monthly, 24)

        for row in (hourly_row, daily_row, weekly_row, monthly_row):
            group.add(row)

        hourly_adj.connect("value-changed", lambda a: setattr(state, "snapshots_hourly", int(a.get_value())))
        daily_adj.connect("value-changed", lambda a: setattr(state, "snapshots_daily", int(a.get_value())))
        weekly_adj.connect("value-changed", lambda a: setattr(state, "snapshots_weekly", int(a.get_value())))
        monthly_adj.connect("value-changed", lambda a: setattr(state, "snapshots_monthly", int(a.get_value())))

        return build_step_page(
            icon_name="edit-undo-symbolic",
            title="Snapshots",
            subtitle="The defaults are sensible — only change these if you know what you want.",
            groups=[group],
        )
