from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# Placeholder assets for the demo -- real branding assets live in the
# `branding` repo; these are just what's on hand right now (see design.md,
# Infrastructure and licensing: images don't get committed into `iso`).
PICTURES_DIR = Path(__file__).resolve().parent.parent.parent / "pictures"


def _choice_card(logo_path: Path, title: str, subtitle: str, screenshot_path: Path | None) -> Gtk.ToggleButton:
    button = Gtk.ToggleButton()
    button.add_css_class("card")
    button.set_size_request(220, 170)
    button.set_overflow(Gtk.Overflow.HIDDEN)

    overlay = Gtk.Overlay()

    if screenshot_path and screenshot_path.exists():
        picture = Gtk.Picture.new_for_filename(str(screenshot_path))
        picture.set_content_fit(Gtk.ContentFit.COVER)
        overlay.set_child(picture)

        scrim = Gtk.Box(hexpand=True, vexpand=True)
        scrim.add_css_class("choice-card-scrim")
        overlay.add_overlay(scrim)
    else:
        # No screenshot for this DE yet -- flat card, matches the rest of
        # the UI until a real one is added (design.md still has GNOME's TBD).
        placeholder = Gtk.Box()
        placeholder.add_css_class("card")
        overlay.set_child(placeholder)

    content = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=8,
        halign=Gtk.Align.CENTER,
        valign=Gtk.Align.CENTER,
        margin_top=16, margin_bottom=16, margin_start=16, margin_end=16,
    )

    if logo_path.exists():
        logo = Gtk.Picture.new_for_filename(str(logo_path))
        logo.set_content_fit(Gtk.ContentFit.CONTAIN)
        logo.set_size_request(48, 48)
        logo.set_can_shrink(True)
        content.append(logo)
    else:
        icon = Gtk.Image.new_from_icon_name("video-display-symbolic")
        icon.set_pixel_size(40)
        content.append(icon)

    title_label = Gtk.Label(label=title)
    title_label.add_css_class("heading")
    if screenshot_path and screenshot_path.exists():
        title_label.add_css_class("choice-card-on-photo")
    content.append(title_label)

    subtitle_label = Gtk.Label(label=subtitle)
    subtitle_label.add_css_class("dim-label")
    subtitle_label.set_wrap(True)
    subtitle_label.set_justify(Gtk.Justification.CENTER)
    content.append(subtitle_label)

    overlay.add_overlay(content)
    button.set_child(overlay)
    return button


class DesktopChoiceStep(InstallStep):
    id = "desktop_choice"
    title = "Desktop environment"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        gnome_btn = _choice_card(
            PICTURES_DIR / "gnome-logo.svg",
            "GNOME",
            "Consistent, stable, comfortable out of the box",
            screenshot_path=None,  # no GNOME screenshot yet -- flat card for now
        )
        hypr_btn = _choice_card(
            PICTURES_DIR / "hyprland-logo.svg",
            "Hyprland",
            "Tiling, Noctalia Shell, fully customizable",
            screenshot_path=PICTURES_DIR / "hyprland-screen.png",
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
            title="Choose a desktop environment",
            subtitle="You can change this later by reinstalling.",
            groups=[group],
        )
