import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page


def _choice_card(icon_name: str, title: str, subtitle: str) -> Gtk.ToggleButton:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin_top=16,
                   margin_bottom=16, margin_start=16, margin_end=16)
    icon = Gtk.Image.new_from_icon_name(icon_name)
    icon.set_pixel_size(40)
    box.append(icon)
    title_label = Gtk.Label(label=title)
    title_label.add_css_class("heading")
    box.append(title_label)
    subtitle_label = Gtk.Label(label=subtitle)
    subtitle_label.add_css_class("dim-label")
    subtitle_label.set_wrap(True)
    subtitle_label.set_justify(Gtk.Justification.CENTER)
    box.append(subtitle_label)

    button = Gtk.ToggleButton()
    button.set_child(box)
    button.add_css_class("card")
    button.set_size_request(200, 160)
    return button


class DesktopChoiceStep(InstallStep):
    id = "desktop_choice"
    title = "Środowisko graficzne"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        gnome_btn = _choice_card(
            "video-display-symbolic",
            "GNOME",
            "Spójne, stabilne, wygodne z pudełka",
        )
        hypr_btn = _choice_card(
            "video-display-symbolic",
            "Hyprland",
            "Tiling, Noctalia Shell, w pełni personalizowalny",
        )
        hypr_btn.set_group(gnome_btn)
        (gnome_btn if state.desktop_environment == "gnome" else hypr_btn).set_active(True)

        def on_toggle(button, _pspec, de_id):
            if button.get_active():
                state.desktop_environment = de_id

        gnome_btn.connect("notify::active", on_toggle, "gnome")
        hypr_btn.connect("notify::active", on_toggle, "hyprland")

        cards_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=16,
            halign=Gtk.Align.CENTER,
            margin_top=8,
            margin_bottom=8,
        )
        cards_box.append(gnome_btn)
        cards_box.append(hypr_btn)

        group = Adw.PreferencesGroup()
        group.add(cards_box)

        return build_step_page(
            icon_name="video-display-symbolic",
            title="Wybierz środowisko graficzne",
            subtitle="Możesz to zmienić przeinstalowując system później.",
            groups=[group],
        )
