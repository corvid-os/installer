from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Adw, GdkPixbuf, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# Placeholder assets for the demo -- real branding assets live in the
# `branding` repo; these are just what's on hand right now (see design.md,
# Infrastructure and licensing: images don't get committed into `iso`).
PICTURES_DIR = Path(__file__).resolve().parent.parent.parent / "pictures"

BLUR_DOWNSCALE = 12  # bigger = blurrier (poor man's gaussian: shrink, then blow back up)


def _load_sharp_and_blurred(path: Path) -> tuple[GdkPixbuf.Pixbuf, GdkPixbuf.Pixbuf] | None:
    if not path.exists():
        return None
    sharp = GdkPixbuf.Pixbuf.new_from_file(str(path))
    w, h = sharp.get_width(), sharp.get_height()
    small = sharp.scale_simple(
        max(1, w // BLUR_DOWNSCALE), max(1, h // BLUR_DOWNSCALE), GdkPixbuf.InterpType.BILINEAR
    )
    blurred = small.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
    return sharp, blurred


def _choice_card(logo_path: Path, title: str, subtitle: str, screenshot_path: Path | None):
    """Returns (button, set_selected) -- set_selected(bool) toggles the
    background between blurred (not picked) and sharp (picked), when a
    screenshot is available."""
    button = Gtk.ToggleButton()
    button.add_css_class("card")
    button.set_size_request(220, 170)
    button.set_overflow(Gtk.Overflow.HIDDEN)

    overlay = Gtk.Overlay()
    set_selected = lambda _is_selected: None  # noqa: E731 -- default no-op, overridden below

    pixbufs = _load_sharp_and_blurred(screenshot_path) if screenshot_path else None
    if pixbufs:
        sharp_pixbuf, blurred_pixbuf = pixbufs
        photo_stack = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.CROSSFADE, transition_duration=300
        )
        blurred_picture = Gtk.Picture.new_for_pixbuf(blurred_pixbuf)
        blurred_picture.set_content_fit(Gtk.ContentFit.COVER)
        sharp_picture = Gtk.Picture.new_for_pixbuf(sharp_pixbuf)
        sharp_picture.set_content_fit(Gtk.ContentFit.COVER)
        photo_stack.add_named(blurred_picture, "blurred")
        photo_stack.add_named(sharp_picture, "sharp")
        photo_stack.set_visible_child_name("blurred")
        overlay.set_child(photo_stack)

        scrim = Gtk.Box(hexpand=True, vexpand=True)
        scrim.add_css_class("choice-card-scrim")
        overlay.add_overlay(scrim)

        def set_selected(is_selected: bool) -> None:  # noqa: F811
            photo_stack.set_visible_child_name("sharp" if is_selected else "blurred")
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
    if pixbufs:
        title_label.add_css_class("choice-card-on-photo")
    content.append(title_label)

    subtitle_label = Gtk.Label(label=subtitle)
    subtitle_label.add_css_class("dim-label")
    subtitle_label.set_wrap(True)
    subtitle_label.set_justify(Gtk.Justification.CENTER)
    content.append(subtitle_label)

    overlay.add_overlay(content)
    button.set_child(overlay)
    return button, set_selected


class DesktopChoiceStep(InstallStep):
    id = "desktop_choice"
    title = "Desktop environment"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        gnome_btn, gnome_set_selected = _choice_card(
            PICTURES_DIR / "gnome-logo.svg",
            "GNOME",
            tr(state, "desktop_choice.gnome_subtitle"),
            screenshot_path=None,  # no GNOME screenshot yet -- flat card for now
        )
        hypr_btn, hypr_set_selected = _choice_card(
            PICTURES_DIR / "hyprland-logo.svg",
            "Hyprland",
            tr(state, "desktop_choice.hyprland_subtitle"),
            screenshot_path=PICTURES_DIR / "hyprland-screen.png",
        )
        hypr_btn.set_group(gnome_btn)
        gnome_selected = state.desktop_environment == "gnome"
        gnome_btn.set_active(gnome_selected)
        hypr_btn.set_active(not gnome_selected)
        gnome_set_selected(gnome_selected)
        hypr_set_selected(not gnome_selected)

        def on_toggle(button, _pspec, de_id, set_selected):
            is_active = button.get_active()
            set_selected(is_active)
            if is_active:
                state.desktop_environment = de_id

        gnome_btn.connect("notify::active", on_toggle, "gnome", gnome_set_selected)
        hypr_btn.connect("notify::active", on_toggle, "hyprland", hypr_set_selected)

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
            title=tr(state, "desktop_choice.title"),
            subtitle=tr(state, "desktop_choice.subtitle"),
            groups=[group],
        )
