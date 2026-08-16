import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.backend.disk import is_uefi, partition_path
from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class BootloaderStep(InstallStep):
    id = "bootloader"
    title = "Bootloader"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title=tr(state, "bootloader.group_title"))

        bootloader_row = Adw.ActionRow(
            title="GRUB",
            subtitle=tr(state, "bootloader.grub_subtitle"),
        )
        bootloader_row.add_prefix(Gtk.Image.new_from_icon_name("system-reboot-symbolic"))
        group.add(bootloader_row)

        # In "auto" mode we create the EFI partition ourselves (step 4) --
        # nothing to pick here, just show where it'll end up.
        if state.disk and state.partitioning_mode == "auto":
            efi_path = partition_path(state.disk, 1)
            efi_row = Adw.ActionRow(title=tr(state, "bootloader.efi_row"), subtitle=efi_path)
            group.add(efi_row)

        return build_step_page(
            icon_name="system-reboot-symbolic",
            title=tr(state, "bootloader.title"),
            subtitle=tr(state, "bootloader.subtitle") if is_uefi() else "BIOS mode detected -- not supported yet.",
            groups=[group],
        )
