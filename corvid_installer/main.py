"""Corvid Installer entry point."""

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, Gio, Gtk  # noqa: E402

from corvid_installer.window import CorvidInstallerWindow

APP_ID = "os.corvid.Installer"

# Small extra styling that doesn't map to a stock libadwaita style class --
# a readable scrim + light text for cards that use a screenshot background.
EXTRA_CSS = b"""
.choice-card-scrim {
    background-color: rgba(14, 11, 20, 0.55);
}
.choice-card-on-photo {
    color: #EDEAF6;
}
"""


class CorvidInstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        provider = Gtk.CssProvider()
        provider.load_from_data(EXTRA_CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self):
        window = self.props.active_window
        if not window:
            window = CorvidInstallerWindow(application=self)
        window.present()


def main() -> int:
    app = CorvidInstallerApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
