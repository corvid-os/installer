import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


class EncryptionStep(InstallStep):
    id = "encryption"
    title = "Encryption"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title=tr(state, "encryption.group_title"),
            description=tr(state, "encryption.group_desc"),
        )

        switch_row = Adw.SwitchRow(
            title=tr(state, "encryption.switch_title"),
            active=state.encrypt,
        )
        group.add(switch_row)

        password_row = Adw.PasswordEntryRow(title=tr(state, "encryption.password_row"))
        password_row.set_sensitive(state.encrypt)
        group.add(password_row)

        confirm_row = Adw.PasswordEntryRow(title=tr(state, "encryption.confirm_row"))
        confirm_row.set_sensitive(state.encrypt)
        group.add(confirm_row)

        def on_toggled(row, _pspec):
            state.encrypt = row.get_active()
            password_row.set_sensitive(state.encrypt)
            confirm_row.set_sensitive(state.encrypt)

        switch_row.connect("notify::active", on_toggled)

        return build_step_page(
            icon_name="channel-secure-symbolic",
            title=tr(state, "encryption.title"),
            subtitle=tr(state, "encryption.subtitle"),
            groups=[group],
        )
