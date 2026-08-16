import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# Placeholder — realna implementacja czyta z lsblk (M2+)
FAKE_DISKS = ["/dev/nvme0n1 — 1 TB", "/dev/sda — 512 GB"]


class DiskStep(InstallStep):
    id = "disk"
    title = "Dysk"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        mode_group = Adw.PreferencesGroup(title="Tryb partycjonowania")

        auto_row = Adw.ActionRow(
            title="Automatyczny",
            subtitle="Cały dysk, Btrfs + subwolumeny, snapshoty — zalecane",
        )
        auto_check = Gtk.CheckButton()
        auto_row.add_prefix(auto_check)
        auto_row.set_activatable_widget(auto_check)
        mode_group.add(auto_row)

        manual_row = Adw.ActionRow(
            title="Ręczny",
            subtitle="Otwiera GNOME Disks — dla zaawansowanych",
        )
        manual_check = Gtk.CheckButton(group=auto_check)
        manual_row.add_prefix(manual_check)
        manual_row.set_activatable_widget(manual_check)
        mode_group.add(manual_row)

        auto_check.set_active(True)

        def on_mode_toggled(button, _pspec):
            if button.get_active():
                state.partitioning_mode = "auto" if button is auto_check else "manual"

        auto_check.connect("notify::active", on_mode_toggled)
        manual_check.connect("notify::active", on_mode_toggled)

        disk_group = Adw.PreferencesGroup(title="Docelowy dysk")
        model = Gtk.StringList.new(FAKE_DISKS)
        disk_row = Adw.ComboRow(title="Dysk", model=model)
        disk_group.add(disk_row)

        warning_group = Adw.PreferencesGroup()
        warning_row = Adw.ActionRow(
            title="⚠️ Wybrany dysk zostanie całkowicie wyczyszczony",
            subtitle="Ten krok nie wykonuje jeszcze żadnych zmian — to podgląd UI",
        )
        warning_row.add_css_class("warning")
        warning_group.add(warning_row)

        return build_step_page(
            icon_name="drive-harddisk-symbolic",
            title="Dysk i partycjonowanie",
            subtitle="Wybierz jak Corvid OS ma przygotować dysk.",
            groups=[mode_group, disk_group, warning_group],
        )
