"""Entry point Corvid Installera."""

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio  # noqa: E402

from corvid_installer.window import CorvidInstallerWindow

APP_ID = "os.corvid.Installer"


class CorvidInstallerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)

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
