"""Wspólny szkielet strony kroku — nagłówek (ikona/tytuł/podtytuł) +
Adw.PreferencesGroup(y) przekazane przez konkretny krok. Trzyma wygląd
wszystkich kroków spójny bez powtarzania tego samego kodu w każdym z nich."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402


def build_step_page(
    icon_name: str,
    title: str,
    subtitle: str,
    groups: list[Adw.PreferencesGroup],
) -> Gtk.Widget:
    page = Adw.PreferencesPage()

    header_group = Adw.PreferencesGroup()
    header_box = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=12,
        halign=Gtk.Align.CENTER,
        margin_top=12,
        margin_bottom=12,
    )
    icon = Gtk.Image.new_from_icon_name(icon_name)
    icon.set_pixel_size(48)
    icon.add_css_class("accent")
    header_box.append(icon)

    title_label = Gtk.Label(label=title)
    title_label.add_css_class("title-1")
    header_box.append(title_label)

    if subtitle:
        subtitle_label = Gtk.Label(label=subtitle)
        subtitle_label.add_css_class("dim-label")
        subtitle_label.set_wrap(True)
        subtitle_label.set_justify(Gtk.Justification.CENTER)
        subtitle_label.set_max_width_chars(60)
        header_box.append(subtitle_label)

    header_group.add(header_box)
    page.add(header_group)

    for group in groups:
        page.add(group)

    return page
