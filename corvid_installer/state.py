"""Central state for every choice made in the wizard. One source of truth
for the UI steps and, eventually, for the backend that runs the install."""

from dataclasses import dataclass


@dataclass
class InstallState:
    # Step 1-2: language / keyboard
    language: str = "English"
    keyboard_layout: str = "us"

    # Step 3: network
    wifi_ssid: str | None = None
    network_connected: bool = False

    # Step 4-5: disk / encryption
    disk: str | None = None
    partitioning_mode: str = "auto"  # "auto" | "manual"
    encrypt: bool = False
    encryption_password: str = ""

    # Step 6: locale
    timezone: str = "UTC"
    locale: str = "en_US.UTF-8"

    # Step 7-8: desktop environment / profile
    desktop_environment: str = "gnome"  # "gnome" | "hyprland"
    profile: str = "minimal"  # "gaming" | "dev" | "both" | "minimal"

    # Step 9: account
    full_name: str = ""
    username: str = ""
    password: str = ""
    is_admin: bool = True

    # Step 10: bootloader
    efi_disk: str | None = None

    # Step 11: snapshots (snapper schedule, editable)
    snapshots_hourly: int = 5
    snapshots_daily: int = 7
    snapshots_weekly: int = 4
    snapshots_monthly: int = 6
