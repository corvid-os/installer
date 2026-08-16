import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# Placeholder network list -- a real implementation hooks into NetworkManager (M2+)
FAKE_NETWORKS = ["Home-WiFi-5G", "Corvid-Guest", "Neighbour_2.4"]


class NetworkStep(InstallStep):
    id = "network"
    title = "Network"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title=tr(state, "network.group_title"),
            description=tr(state, "network.group_desc"),
        )
        for ssid in FAKE_NETWORKS:
            row = Adw.ActionRow(title=ssid, activatable=True)
            row.add_prefix(Gtk.Image.new_from_icon_name("network-wireless-symbolic"))
            row.add_suffix(Gtk.Image.new_from_icon_name("go-next-symbolic"))

            def on_activate(_row, ssid=ssid):
                state.wifi_ssid = ssid
                state.network_connected = True

            row.connect("activated", on_activate)
            group.add(row)

        skip_group = Adw.PreferencesGroup()
        skip_row = Adw.ActionRow(
            title=tr(state, "network.skip_title"),
            subtitle=tr(state, "network.skip_subtitle"),
            activatable=True,
        )

        def on_skip(_row):
            state.network_connected = True

        skip_row.connect("activated", on_skip)
        skip_group.add(skip_row)

        return build_step_page(
            icon_name="network-wireless-symbolic",
            title=tr(state, "network.title"),
            subtitle=tr(state, "network.subtitle"),
            groups=[group, skip_group],
        )
