import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

FAKE_EFI_PARTITIONS = ["/dev/nvme0n1p1 — 512 MB (EFI)"]


class BootloaderStep(InstallStep):
    id = "bootloader"
    title = "Bootloader"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Bootloader")

        bootloader_row = Adw.ActionRow(
            title="GRUB",
            subtitle="Jedyna opcja na start — integruje się z grub-btrfs (snapshoty w menu boot)",
        )
        bootloader_row.add_prefix(Gtk.Image.new_from_icon_name("system-reboot-symbolic"))
        group.add(bootloader_row)

        efi_model = Gtk.StringList.new(FAKE_EFI_PARTITIONS)
        efi_row = Adw.ComboRow(title="Partycja EFI", model=efi_model)
        group.add(efi_row)

        return build_step_page(
            icon_name="system-reboot-symbolic",
            title="Bootloader",
            subtitle="Wykryto tryb UEFI.",
            groups=[group],
        )
