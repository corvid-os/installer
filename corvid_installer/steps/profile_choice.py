import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# (profile id, emoji, name key, subtitle key or literal)
PROFILES = [
    ("gaming", "🎮", "profile.gaming", "Steam, Proton-GE, gamemode, mangohud"),
    ("dev", "💻", "profile.dev", "Podman, VSCodium, fish + starship, mise"),
    ("both", "🚀", "profile_choice.both_name", "profile_choice.both_subtitle"),
    ("minimal", "🪶", "profile_choice.minimal_name", "profile_choice.minimal_subtitle"),
]
# Subtitles that are just technical package lists read the same in every
# language, so they're not routed through tr() -- only the two keys below are.
TRANSLATED_SUBTITLES = {"profile_choice.both_subtitle", "profile_choice.minimal_subtitle"}


class ProfileChoiceStep(InstallStep):
    id = "profile_choice"
    title = "Profile"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(title=tr(state, "profile_choice.group_title"))

        first_check = None
        for profile_id, emoji, name_key, subtitle_key in PROFILES:
            name = tr(state, name_key)
            subtitle = tr(state, subtitle_key) if subtitle_key in TRANSLATED_SUBTITLES else subtitle_key
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
            title=tr(state, "profile_choice.title"),
            subtitle=tr(state, "profile_choice.subtitle"),
            groups=[group],
        )
