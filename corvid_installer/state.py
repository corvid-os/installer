"""Centralny stan wyborów użytkownika. Jedno źródło prawdy dla kroków UI
i (docelowo) dla backendu wykonującego instalację."""

from dataclasses import dataclass


@dataclass
class InstallState:
    # Krok 1-2: język / klawiatura
    language: str = "Polski"
    keyboard_layout: str = "pl"

    # Krok 3: sieć
    wifi_ssid: str | None = None
    network_connected: bool = False

    # Krok 4-5: dysk / szyfrowanie
    disk: str | None = None
    partitioning_mode: str = "auto"  # "auto" | "manual"
    encrypt: bool = False
    encryption_password: str = ""

    # Krok 6: lokalizacja
    timezone: str = "Europe/Warsaw"
    locale: str = "pl_PL.UTF-8"

    # Krok 7-8: środowisko / profil
    desktop_environment: str = "gnome"  # "gnome" | "hyprland"
    profile: str = "minimal"  # "gaming" | "dev" | "both" | "minimal"

    # Krok 9: konto
    full_name: str = ""
    username: str = ""
    password: str = ""
    is_admin: bool = True

    # Krok 10: bootloader
    efi_disk: str | None = None

    # Krok 11: snapshoty (harmonogram snappera, edytowalny)
    snapshots_hourly: int = 5
    snapshots_daily: int = 7
    snapshots_weekly: int = 4
    snapshots_monthly: int = 6
