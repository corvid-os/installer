import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep, Validation
from corvid_installer.ui.page import build_step_page

# Placeholder -- a real implementation reads from lsblk (M2+)
FAKE_DISKS = ["/dev/nvme0n1 — 1 TB", "/dev/sda — 512 GB"]


class DiskStep(InstallStep):
    id = "disk"
    title = "Disk"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        mode_group = Adw.PreferencesGroup(title="Partitioning mode")

        auto_row = Adw.ActionRow(
            title="Automatic",
            subtitle="Whole disk, Btrfs with subvolumes, snapshots — recommended",
        )
        auto_check = Gtk.CheckButton()
        auto_row.add_prefix(auto_check)
        auto_row.set_activatable_widget(auto_check)
        mode_group.add(auto_row)

        manual_row = Adw.ActionRow(
            title="Manual",
            subtitle="Opens GNOME Disks — for advanced users",
        )
        manual_check = Gtk.CheckButton(group=auto_check)
        manual_row.add_prefix(manual_check)
        manual_row.set_activatable_widget(manual_check)
        mode_group.add(manual_row)

        auto_check.set_active(state.partitioning_mode == "auto")
        manual_check.set_active(state.partitioning_mode == "manual")

        def on_mode_toggled(button, _pspec):
            if button.get_active():
                state.partitioning_mode = "auto" if button is auto_check else "manual"
                if self.request_revalidate:
                    self.request_revalidate()

        auto_check.connect("notify::active", on_mode_toggled)
        manual_check.connect("notify::active", on_mode_toggled)

        disk_group = Adw.PreferencesGroup(title="Target disk")
        model = Gtk.StringList.new(FAKE_DISKS)
        disk_row = Adw.ComboRow(title="Disk", model=model)
        disk_group.add(disk_row)

        warning_group = Adw.PreferencesGroup()
        warning_row = Adw.ActionRow(
            title="⚠️ The selected disk will be completely wiped",
            subtitle="This step doesn't make any changes yet — it's a UI preview",
        )
        warning_row.add_css_class("warning")
        warning_group.add(warning_row)

        accept_row = Adw.ActionRow(
            title="I know this will erase everything on the drive, and I accept that I want to do it.",
            subtitle="Click this row to accept.",
            activatable=True,
        )
        accept_row.add_css_class("warning")
        accept_check = Gtk.CheckButton()
        accept_check.set_active(state.accepted_wipe)
        accept_row.add_prefix(accept_check)
        accept_row.set_activatable_widget(accept_check)

        def on_accept_toggled(button, _pspec):
            state.accepted_wipe = button.get_active()
            if self.request_revalidate:
                self.request_revalidate()

        accept_check.connect("notify::active", on_accept_toggled)
        warning_group.add(accept_row)

        return build_step_page(
            icon_name="drive-harddisk-symbolic",
            title="Disk and partitioning",
            subtitle="Choose how Corvid OS should prepare the disk.",
            groups=[mode_group, disk_group, warning_group],
        )

    def validate(self, state: InstallState) -> Validation:
        if state.partitioning_mode == "auto" and not state.accepted_wipe:
            return Validation.error(
                "Check the box confirming you understand this will erase the disk."
            )
        return Validation.ok()
