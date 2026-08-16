import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class UserAccountStep(InstallStep):
    id = "user_account"
    title = "Konto użytkownika"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Utwórz konto",
            description="Tylko pierwsze konto — resztą (zmiana hasła, kolejni "
            "użytkownicy) zajmiesz się później w Ustawieniach systemu.",
        )

        full_name_row = Adw.EntryRow(title="Pełna nazwa")
        group.add(full_name_row)

        username_row = Adw.EntryRow(title="Nazwa użytkownika")
        group.add(username_row)

        password_row = Adw.PasswordEntryRow(title="Hasło")
        group.add(password_row)

        confirm_row = Adw.PasswordEntryRow(title="Potwierdź hasło")
        group.add(confirm_row)

        admin_row = Adw.SwitchRow(
            title="To konto może administrować systemem",
            subtitle="Dostęp do sudo (grupa wheel)",
            active=state.is_admin,
        )
        group.add(admin_row)

        def on_admin_toggled(row, _pspec):
            state.is_admin = row.get_active()

        admin_row.connect("notify::active", on_admin_toggled)

        return build_step_page(
            icon_name="avatar-default-symbolic",
            title="Konto użytkownika",
            subtitle="",
            groups=[group],
        )
