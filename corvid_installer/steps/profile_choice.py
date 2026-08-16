import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

PROFILES = [
    ("gaming", "Gaming", "🎮", "Steam, Proton-GE, gamemode, mangohud"),
    ("dev", "Dev", "💻", "Podman, VSCodium, fish + starship, mise"),
    ("both", "Oba", "🚀", "Gaming + Dev razem"),
    ("minimal", "Minimalny", "🪶", "Tylko podstawa — reszta do doinstalowania"),
]


class ProfileChoiceStep(InstallStep):
    id = "profile_choice"
    title = "Profil"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title="Wybierz profil instalacji")

        first_check = None
        for profile_id, name, emoji, subtitle in PROFILES:
            row = Adw.ActionRow(title=f"{emoji}  {name}", subtitle=subtitle, activatable=True)
            check = Gtk.CheckButton(group=first_check)
            first_check = first_check or check
            row.add_prefix(check)
            row.set_activatable_widget(check)
            if profile_id == state.profile:
                check.set_active(True)

            def on_toggled(button, _pspec, pid=profile_id):
                if button.get_active():
                    state.profile = pid

            check.connect("notify::active", on_toggled)
            group.add(row)

        return build_step_page(
            icon_name="applications-games-symbolic",
            title="Wybierz profil",
            subtitle="Determinuje domyślny zestaw zainstalowanych aplikacji.",
            groups=[group],
        )
