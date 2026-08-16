"""Corvid Installer entry point.

By default this never touches a real disk -- every backend command is
logged instead of run (state.dry_run defaults to True). Pass --execute to
actually install. Only ever do that inside a VM or a live environment you
don't mind wiping; see installer/vm-test/README.md."""

import argparse
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
    def __init__(self, execute: bool):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.execute = execute
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
            window.state.dry_run = not self.execute
        window.present()


def main() -> int:
    parser = argparse.ArgumentParser(prog="corvid-installer", description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually run install commands instead of just logging them. "
        "Only pass this inside a VM/live environment -- see vm-test/README.md.",
    )
    args, remaining = parser.parse_known_args()

    app = CorvidInstallerApp(execute=args.execute)
    return app.run([sys.argv[0], *remaining])


if __name__ == "__main__":
    sys.exit(main())
