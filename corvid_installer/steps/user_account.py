import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class UserAccountStep(InstallStep):
    id = "user_account"
    title = "User account"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Create an account",
            description="Just the first account — password changes and "
            "additional users are handled later in system Settings.",
        )

        full_name_row = Adw.EntryRow(title="Full name")
        group.add(full_name_row)

        username_row = Adw.EntryRow(title="Username")
        group.add(username_row)

        password_row = Adw.PasswordEntryRow(title="Password")
        group.add(password_row)

        confirm_row = Adw.PasswordEntryRow(title="Confirm password")
        group.add(confirm_row)

        admin_row = Adw.SwitchRow(
            title="This account can administer the system",
            subtitle="Grants sudo access (wheel group)",
            active=state.is_admin,
        )
        group.add(admin_row)

        def on_admin_toggled(row, _pspec):
            state.is_admin = row.get_active()

        admin_row.connect("notify::active", on_admin_toggled)

        return build_step_page(
            icon_name="avatar-default-symbolic",
            title="User account",
            subtitle="",
            groups=[group],
        )
