import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

import subprocess

from corvid_installer.backend import disk as disk_backend
from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep, Validation
from corvid_installer.ui.page import build_step_page

FALLBACK_DISKS = ["/dev/vda — 20G"]  # shown only if lsblk isn't available at all


class DiskStep(InstallStep):
    id = "disk"
    title = "Disk"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        error_group = None
        if self._error:
            error_group = Adw.PreferencesGroup()
            error_row = Adw.ActionRow(title="Partitioning failed", subtitle=self._error)
            error_row.add_css_class("error")
            error_group.add(error_row)

        mode_group = Adw.PreferencesGroup(title=tr(state, "disk.mode_group"))

        auto_row = Adw.ActionRow(
            title=tr(state, "disk.auto_title"),
            subtitle=tr(state, "disk.auto_subtitle"),
        )
        auto_check = Gtk.CheckButton()
        auto_row.add_prefix(auto_check)
        auto_row.set_activatable_widget(auto_check)
        mode_group.add(auto_row)

        manual_row = Adw.ActionRow(
            title=tr(state, "disk.manual_title"),
            subtitle=tr(state, "disk.manual_subtitle"),
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
                state.disk_prepared = False  # mode changed -- redo whichever action applies on Next
                if self.request_revalidate:
                    self.request_revalidate()

        auto_check.connect("notify::active", on_mode_toggled)
        manual_check.connect("notify::active", on_mode_toggled)

        disk_group = Adw.PreferencesGroup(title=tr(state, "disk.disk_group"))
        disks = disk_backend.list_disks() or FALLBACK_DISKS
        disk_paths = [entry.split(" — ")[0] for entry in disks]
        model = Gtk.StringList.new(disks)
        disk_row = Adw.ComboRow(title=tr(state, "disk.disk_row"), model=model)
        if state.disk in disk_paths:
            disk_row.set_selected(disk_paths.index(state.disk))
        else:
            state.disk = disk_paths[0]

        def on_disk_selected(combo_row, _pspec):
            state.disk = disk_paths[combo_row.get_selected()]

        disk_row.connect("notify::selected", on_disk_selected)
        disk_group.add(disk_row)

        warning_group = Adw.PreferencesGroup()
        warning_row = Adw.ActionRow(
            title=tr(state, "disk.warning_title"),
            subtitle=tr(state, "disk.warning_subtitle"),
        )
        warning_row.add_css_class("warning")
        warning_group.add(warning_row)

        accept_row = Adw.ActionRow(
            title=tr(state, "disk.accept_title"),
            subtitle=tr(state, "disk.accept_subtitle"),
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

        groups = [mode_group, disk_group, warning_group]
        if error_group is not None:
            groups = [error_group, *groups]

        return build_step_page(
            icon_name="drive-harddisk-symbolic",
            title=tr(state, "disk.title"),
            subtitle=tr(state, "disk.subtitle"),
            groups=groups,
        )

    _error: str | None = None

    def validate(self, state: InstallState) -> Validation:
        if self._error:
            return Validation.error(f"Partitioning failed: {self._error}")
        if state.partitioning_mode == "auto" and not state.accepted_wipe:
            return Validation.error(tr(state, "disk.validation_error"))
        return Validation.ok()

    def apply(self, state: InstallState) -> None:
        """Deliberately acts immediately, on leaving this step, instead of
        waiting for the final install step -- see state.disk_prepared. Auto
        mode partitions right now; manual mode just opens GNOME Disks and
        leaves the actual work to the user."""
        if state.disk_prepared:
            return
        self._error = None

        if state.partitioning_mode == "manual":
            try:
                subprocess.Popen(["gnome-disks"])
            except FileNotFoundError:
                pass  # not installed/available -- nothing more we can do here
            state.disk_prepared = True
            return

        log_lines: list[str] = []
        try:
            # Defensive: a previous attempt in this same session may have
            # left /mnt mounted, which makes parted/mkfs fail with "device
            # busy" -- ignore failure here, there's just nothing to unmount.
            try:
                disk_backend.unmount_all(dry_run=state.dry_run, log=log_lines.append)
            except Exception:
                pass

            efi_part, root_part = disk_backend.partition_disk(
                state.disk, dry_run=state.dry_run, log=log_lines.append
            )
            disk_backend.create_subvolumes(root_part, dry_run=state.dry_run, log=log_lines.append)
            disk_backend.mount_layout(root_part, efi_part, dry_run=state.dry_run, log=log_lines.append)
            state.disk_prepared = True
        except Exception as exc:  # noqa: BLE001 -- surfaced via validate(), never swallowed silently
            self._error = str(exc)
        finally:
            for line in log_lines:
                print(line)
