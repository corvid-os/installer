import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class EncryptionStep(InstallStep):
    id = "encryption"
    title = "Szyfrowanie"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Szyfrowanie dysku (opcjonalne)",
            description="LUKS2 na partycji root. Hasło osobne od hasła konta użytkownika.",
        )

        switch_row = Adw.SwitchRow(
            title="Włącz szyfrowanie dysku",
            active=state.encrypt,
        )
        group.add(switch_row)

        password_row = Adw.PasswordEntryRow(title="Hasło szyfrowania")
        password_row.set_sensitive(state.encrypt)
        group.add(password_row)

        confirm_row = Adw.PasswordEntryRow(title="Potwierdź hasło")
        confirm_row.set_sensitive(state.encrypt)
        group.add(confirm_row)

        def on_toggled(row, _pspec):
            state.encrypt = row.get_active()
            password_row.set_sensitive(state.encrypt)
            confirm_row.set_sensitive(state.encrypt)

        switch_row.connect("notify::active", on_toggled)

        return build_step_page(
            icon_name="channel-secure-symbolic",
            title="Szyfrowanie dysku",
            subtitle="Krok opcjonalny — możesz go pominąć.",
            groups=[group],
        )
