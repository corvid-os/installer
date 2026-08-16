import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep, Validation
from corvid_installer.ui.page import build_step_page


class UserAccountStep(InstallStep):
    id = "user_account"
    title = "User account"

    _confirm_password = ""

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title=tr(state, "user_account.group_title"),
            description=tr(state, "user_account.group_desc"),
        )

        full_name_row = Adw.EntryRow(title=tr(state, "user_account.full_name_row"), text=state.full_name)
        full_name_row.connect("changed", lambda row: setattr(state, "full_name", row.get_text()))
        group.add(full_name_row)

        def revalidate() -> None:
            if self.request_revalidate:
                self.request_revalidate()

        username_row = Adw.EntryRow(title=tr(state, "user_account.username_row"), text=state.username)

        def on_username_changed(row):
            state.username = row.get_text()
            revalidate()

        username_row.connect("changed", on_username_changed)
        group.add(username_row)

        password_row = Adw.PasswordEntryRow(title=tr(state, "user_account.password_row"), text=state.password)

        def on_password_changed(row):
            state.password = row.get_text()
            revalidate()

        password_row.connect("changed", on_password_changed)
        group.add(password_row)

        confirm_row = Adw.PasswordEntryRow(title=tr(state, "user_account.confirm_row"), text=self._confirm_password)

        def on_confirm_changed(row):
            self._confirm_password = row.get_text()
            revalidate()

        confirm_row.connect("changed", on_confirm_changed)
        group.add(confirm_row)

        admin_row = Adw.SwitchRow(
            title=tr(state, "user_account.admin_title"),
            subtitle=tr(state, "user_account.admin_subtitle"),
            active=state.is_admin,
        )
        group.add(admin_row)

        def on_admin_toggled(row, _pspec):
            state.is_admin = row.get_active()

        admin_row.connect("notify::active", on_admin_toggled)

        return build_step_page(
            icon_name="avatar-default-symbolic",
            title=tr(state, "user_account.title"),
            subtitle="",
            groups=[group],
        )

    def validate(self, state: InstallState) -> Validation:
        if not state.username.strip():
            return Validation.error("Pick a username.")
        if not state.username.isascii() or not state.username[:1].isalpha() or " " in state.username:
            return Validation.error("Username must start with a letter and contain no spaces.")
        if not state.password:
            return Validation.error("Set a password.")
        if state.password != self._confirm_password:
            return Validation.error("Passwords don't match.")
        return Validation.ok()
