import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

# Placeholder listy sieci — realna implementacja podepnie NetworkManager (M2+)
FAKE_NETWORKS = ["Domowe-WiFi-5G", "Corvid-Guest", "Sasiad_2.4"]


class NetworkStep(InstallStep):
    id = "network"
    title = "Sieć"

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        group = Adw.PreferencesGroup(
            title="Sieci Wi-Fi",
            description="Połączenie z internetem jest wymagane do pobrania pakietów.",
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
            title="Mam już połączenie przewodowe",
            subtitle="Pomiń ten krok",
            activatable=True,
        )

        def on_skip(_row):
            state.network_connected = True

        skip_row.connect("activated", on_skip)
        skip_group.add(skip_row)

        return build_step_page(
            icon_name="network-wireless-symbolic",
            title="Połącz się z siecią",
            subtitle="Wybierz sieć Wi-Fi z listy poniżej.",
            groups=[group, skip_group],
        )
