"""Minimal translation table. Only English and Polish for now (see
welcome.py) -- adding a language is one more value per key here, no other
code changes."""

# state.language holds the display name shown in the picker ("English",
# "Polski"); this maps that to the language code used as a STRINGS key.
LANG_CODE = {"English": "en", "Polski": "pl"}

STRINGS: dict[str, dict[str, str]] = {
    # Window chrome
    "nav.window_title": {"en": "Install Corvid OS", "pl": "Zainstaluj Corvid OS"},
    "nav.back": {"en": "Back", "pl": "Wstecz"},
    "nav.next": {"en": "Next", "pl": "Dalej"},
    "nav.finish": {"en": "Finish", "pl": "Zakończ"},
    "nav.step_progress": {"en": "Step {n} of {total} — {title}", "pl": "Krok {n} z {total} — {title}"},
    "nav.fix_fields": {
        "en": "Fix the highlighted fields before continuing",
        "pl": "Popraw zaznaczone pola przed kontynuowaniem",
    },

    # Welcome
    "welcome.step_title": {"en": "Welcome", "pl": "Powitanie"},
    "welcome.language_group": {"en": "Language", "pl": "Język"},
    "welcome.language_row": {"en": "Installer and system language", "pl": "Język instalatora i systemu"},
    "welcome.title": {"en": "Welcome to Corvid OS", "pl": "Witaj w Corvid OS"},
    "welcome.subtitle": {
        "en": "This wizard will walk you through the install. Pick a language to get started.",
        "pl": "Ten kreator przeprowadzi Cię przez instalację. Wybierz język, żeby zacząć.",
    },

    # Keyboard
    "keyboard.step_title": {"en": "Keyboard", "pl": "Klawiatura"},
    "keyboard.group_title": {"en": "Keyboard layout", "pl": "Układ klawiatury"},
    "keyboard.layout_row": {"en": "Layout", "pl": "Układ"},
    "keyboard.test_row": {"en": "Test it here", "pl": "Przetestuj tutaj"},
    "keyboard.title": {"en": "Keyboard layout", "pl": "Układ klawiatury"},
    "keyboard.subtitle": {
        "en": "Pick a layout and check that characters type correctly.",
        "pl": "Wybierz układ i sprawdź, czy znaki wpisują się poprawnie.",
    },

    # Network
    "network.step_title": {"en": "Network", "pl": "Sieć"},
    "network.group_title": {"en": "Wi-Fi networks", "pl": "Sieci Wi-Fi"},
    "network.group_desc": {
        "en": "An internet connection is needed to download packages.",
        "pl": "Połączenie z internetem jest wymagane do pobrania pakietów.",
    },
    "network.skip_title": {"en": "I already have a wired connection", "pl": "Mam już połączenie przewodowe"},
    "network.skip_subtitle": {"en": "Skip this step", "pl": "Pomiń ten krok"},
    "network.title": {"en": "Connect to a network", "pl": "Połącz się z siecią"},
    "network.subtitle": {
        "en": "Pick a Wi-Fi network from the list below.",
        "pl": "Wybierz sieć Wi-Fi z listy poniżej.",
    },

    # Disk
    "disk.step_title": {"en": "Disk", "pl": "Dysk"},
    "disk.mode_group": {"en": "Partitioning mode", "pl": "Tryb partycjonowania"},
    "disk.auto_title": {"en": "Automatic", "pl": "Automatyczny"},
    "disk.auto_subtitle": {
        "en": "Whole disk, Btrfs with subvolumes, snapshots — recommended",
        "pl": "Cały dysk, Btrfs z subwolumenami, snapshoty — zalecane",
    },
    "disk.manual_title": {"en": "Manual", "pl": "Ręczny"},
    "disk.manual_subtitle": {
        "en": "Opens GNOME Disks — for advanced users",
        "pl": "Otwiera GNOME Disks — dla zaawansowanych",
    },
    "disk.disk_group": {"en": "Target disk", "pl": "Docelowy dysk"},
    "disk.disk_row": {"en": "Disk", "pl": "Dysk"},
    "disk.warning_title": {
        "en": "⚠️ The selected disk will be completely wiped",
        "pl": "⚠️ Wybrany dysk zostanie całkowicie wyczyszczony",
    },
    "disk.warning_subtitle": {
        "en": "This step doesn't make any changes yet — it's a UI preview",
        "pl": "Ten krok nie wprowadza jeszcze żadnych zmian — to podgląd interfejsu",
    },
    "disk.accept_title": {
        "en": "I know this will erase everything on the drive, and I accept that I want to do it.",
        "pl": "Wiem, że to usunie wszystko z dysku, i akceptuję, że tego chcę.",
    },
    "disk.accept_subtitle": {"en": "Click this row to accept.", "pl": "Kliknij ten wiersz, żeby zaakceptować."},
    "disk.title": {"en": "Disk and partitioning", "pl": "Dysk i partycjonowanie"},
    "disk.subtitle": {
        "en": "Choose how Corvid OS should prepare the disk.",
        "pl": "Wybierz, jak Corvid OS ma przygotować dysk.",
    },
    "disk.validation_error": {
        "en": "Check the box confirming you understand this will erase the disk.",
        "pl": "Zaznacz pole potwierdzające, że rozumiesz, iż to usunie dysk.",
    },

    # Encryption
    "encryption.step_title": {"en": "Encryption", "pl": "Szyfrowanie"},
    "encryption.group_title": {"en": "Disk encryption (optional)", "pl": "Szyfrowanie dysku (opcjonalne)"},
    "encryption.group_desc": {
        "en": "LUKS2 on the root partition. Separate from your account password.",
        "pl": "LUKS2 na partycji root. Osobne od hasła Twojego konta.",
    },
    "encryption.switch_title": {"en": "Enable disk encryption", "pl": "Włącz szyfrowanie dysku"},
    "encryption.password_row": {"en": "Encryption password", "pl": "Hasło szyfrowania"},
    "encryption.confirm_row": {"en": "Confirm password", "pl": "Potwierdź hasło"},
    "encryption.title": {"en": "Disk encryption", "pl": "Szyfrowanie dysku"},
    "encryption.subtitle": {"en": "Optional step — feel free to skip it.", "pl": "Krok opcjonalny — możesz go pominąć."},

    # Locale
    "locale.step_title": {"en": "Timezone and locale", "pl": "Strefa czasowa i lokalizacja"},
    "locale.group_title": {"en": "Auto-detected", "pl": "Wykryto automatycznie"},
    "locale.group_desc": {
        "en": "Change these if IP-based detection got it wrong.",
        "pl": "Zmień, jeśli wykrywanie po IP się pomyliło.",
    },
    "locale.timezone_row": {"en": "Timezone", "pl": "Strefa czasowa"},
    "locale.locale_row": {"en": "Locale (date/currency format)", "pl": "Lokalizacja (format daty/waluty)"},
    "locale.title": {"en": "Timezone and locale", "pl": "Strefa czasowa i lokalizacja"},

    # Desktop choice
    "desktop_choice.step_title": {"en": "Desktop environment", "pl": "Środowisko graficzne"},
    "desktop_choice.gnome_subtitle": {
        "en": "Consistent, stable, comfortable out of the box",
        "pl": "Spójne, stabilne, wygodne od razu po instalacji",
    },
    "desktop_choice.hyprland_subtitle": {
        "en": "Tiling, Noctalia Shell, fully customizable",
        "pl": "Tiling, Noctalia Shell, w pełni personalizowalne",
    },
    "desktop_choice.title": {"en": "Choose a desktop environment", "pl": "Wybierz środowisko graficzne"},
    "desktop_choice.subtitle": {
        "en": "You can change this later by reinstalling.",
        "pl": "Możesz to zmienić później, przeinstalowując system.",
    },

    # Profile choice
    "profile_choice.step_title": {"en": "Profile", "pl": "Profil"},
    "profile_choice.group_title": {"en": "Choose an install profile", "pl": "Wybierz profil instalacji"},
    "profile_choice.both_name": {"en": "Both", "pl": "Oba"},
    "profile_choice.both_subtitle": {"en": "Gaming and Dev together", "pl": "Gaming i Dev razem"},
    "profile_choice.minimal_name": {"en": "Minimal", "pl": "Minimalny"},
    "profile_choice.minimal_subtitle": {
        "en": "Just the base — add the rest yourself",
        "pl": "Tylko podstawa — resztę doinstalujesz sam",
    },
    "profile_choice.title": {"en": "Choose a profile", "pl": "Wybierz profil"},
    "profile_choice.subtitle": {
        "en": "Determines the default set of installed applications.",
        "pl": "Określa domyślny zestaw instalowanych aplikacji.",
    },

    # User account
    "user_account.step_title": {"en": "User account", "pl": "Konto użytkownika"},
    "user_account.group_title": {"en": "Create an account", "pl": "Utwórz konto"},
    "user_account.group_desc": {
        "en": "Just the first account — password changes and additional users are handled later in system Settings.",
        "pl": "Tylko pierwsze konto — zmianę hasła i kolejnych użytkowników obsłużysz później w Ustawieniach systemu.",
    },
    "user_account.full_name_row": {"en": "Full name", "pl": "Pełna nazwa"},
    "user_account.username_row": {"en": "Username", "pl": "Nazwa użytkownika"},
    "user_account.password_row": {"en": "Password", "pl": "Hasło"},
    "user_account.confirm_row": {"en": "Confirm password", "pl": "Potwierdź hasło"},
    "user_account.admin_title": {
        "en": "This account can administer the system",
        "pl": "To konto może administrować systemem",
    },
    "user_account.admin_subtitle": {"en": "Grants sudo access (wheel group)", "pl": "Daje dostęp sudo (grupa wheel)"},
    "user_account.title": {"en": "User account", "pl": "Konto użytkownika"},

    # Bootloader
    "bootloader.step_title": {"en": "Bootloader", "pl": "Bootloader"},
    "bootloader.group_title": {"en": "Bootloader", "pl": "Bootloader"},
    "bootloader.grub_subtitle": {
        "en": "The only option for now — integrates with grub-btrfs (snapshots in the boot menu)",
        "pl": "Jedyna opcja na razie — integruje się z grub-btrfs (snapshoty w menu rozruchu)",
    },
    "bootloader.efi_row": {"en": "EFI partition", "pl": "Partycja EFI"},
    "bootloader.title": {"en": "Bootloader", "pl": "Bootloader"},
    "bootloader.subtitle": {"en": "UEFI mode detected.", "pl": "Wykryto tryb UEFI."},

    # Snapshots
    "snapshots.step_title": {"en": "Snapshots", "pl": "Snapshoty"},
    "snapshots.group_title": {"en": "Snapshot schedule (snapper)", "pl": "Harmonogram snapshotów (snapper)"},
    "snapshots.group_desc": {
        "en": "Automatic Btrfs snapshots — plus one before and after every package update (snap-pac), "
        "regardless of the schedule below.",
        "pl": "Automatyczne snapshoty Btrfs — dodatkowo jeden przed i po każdej aktualizacji pakietów "
        "(snap-pac), niezależnie od harmonogramu poniżej.",
    },
    "snapshots.hourly": {"en": "Hourly — how many to keep", "pl": "Co godzinę — ile zachować"},
    "snapshots.daily": {"en": "Daily — how many to keep", "pl": "Codziennie — ile zachować"},
    "snapshots.weekly": {"en": "Weekly — how many to keep", "pl": "Co tydzień — ile zachować"},
    "snapshots.monthly": {"en": "Monthly — how many to keep", "pl": "Co miesiąc — ile zachować"},
    "snapshots.title": {"en": "Snapshots", "pl": "Snapshoty"},
    "snapshots.subtitle": {
        "en": "The defaults are sensible — only change these if you know what you want.",
        "pl": "Wartości domyślne są sensowne — zmień je tylko, jeśli wiesz czego chcesz.",
    },

    # Summary
    "summary.step_title": {"en": "Summary", "pl": "Podsumowanie"},
    "summary.group_title": {
        "en": "Review your choices before installing",
        "pl": "Sprawdź swoje wybory przed instalacją",
    },
    "summary.group_desc": {
        "en": "This is the last chance to go back — the next step writes changes to disk.",
        "pl": "To ostatnia szansa, żeby się cofnąć — kolejny krok zapisuje zmiany na dysku.",
    },
    "summary.title": {"en": "Summary", "pl": "Podsumowanie"},
    "summary.label.language": {"en": "Language", "pl": "Język"},
    "summary.label.keyboard": {"en": "Keyboard", "pl": "Klawiatura"},
    "summary.label.network": {"en": "Network", "pl": "Sieć"},
    "summary.label.disk": {"en": "Disk", "pl": "Dysk"},
    "summary.label.partitioning_mode": {"en": "Partitioning mode", "pl": "Tryb partycjonowania"},
    "summary.label.encryption": {"en": "Encryption", "pl": "Szyfrowanie"},
    "summary.label.timezone": {"en": "Timezone", "pl": "Strefa czasowa"},
    "summary.label.desktop_environment": {"en": "Desktop environment", "pl": "Środowisko graficzne"},
    "summary.label.profile": {"en": "Profile", "pl": "Profil"},
    "summary.label.user": {"en": "User", "pl": "Użytkownik"},
    "summary.label.administrator": {"en": "Administrator", "pl": "Administrator"},
    "summary.label.snapshots": {"en": "Snapshots", "pl": "Snapshoty"},
    "summary.value.connected": {"en": "connected", "pl": "połączono"},
    "summary.value.none": {"en": "none", "pl": "brak"},
    "summary.value.auto_disk": {"en": "(auto — first one detected)", "pl": "(auto — pierwszy wykryty)"},
    "summary.value.enabled": {"en": "enabled", "pl": "włączone"},
    "summary.value.disabled": {"en": "disabled", "pl": "wyłączone"},
    "summary.value.not_set": {"en": "(not set)", "pl": "(nie podano)"},
    "summary.value.yes": {"en": "yes", "pl": "tak"},
    "summary.value.no": {"en": "no", "pl": "nie"},
    "summary.value.snapshots_line": {
        "en": "hourly: {hourly}, daily: {daily}, weekly: {weekly}, monthly: {monthly}",
        "pl": "godzinowe: {hourly}, dzienne: {daily}, tygodniowe: {weekly}, miesięczne: {monthly}",
    },
    "profile.gaming": {"en": "Gaming", "pl": "Gaming"},
    "profile.dev": {"en": "Dev", "pl": "Dev"},
    "profile.both": {"en": "Gaming + Dev", "pl": "Gaming + Dev"},
    "profile.minimal": {"en": "Minimal", "pl": "Minimalny"},

    # Progress
    "progress.step_title": {"en": "Installing", "pl": "Instalacja"},
    "progress.title": {"en": "Installing", "pl": "Instalacja"},
    "progress.subtitle": {"en": "Don't turn off your computer.", "pl": "Nie wyłączaj komputera."},
    "progress.done": {"en": "Done", "pl": "Gotowe"},
    "progress.complete_log": {
        "en": "Install (simulated) complete.",
        "pl": "Instalacja (symulowana) zakończona.",
    },
    "progress.not_finished": {
        "en": "Wait for the installation to finish.",
        "pl": "Poczekaj, aż instalacja się zakończy.",
    },
    "progress.stage.partition": {
        "en": "Partitioning the disk and setting up Btrfs…",
        "pl": "Partycjonowanie dysku i konfiguracja Btrfs…",
    },
    "progress.stage.pacstrap": {
        "en": "pacstrap — installing base packages…",
        "pl": "pacstrap — instalacja pakietów bazowych…",
    },
    "progress.stage.genfstab": {"en": "genfstab — writing fstab…", "pl": "genfstab — zapis fstab…"},
    "progress.stage.chroot": {
        "en": "Configuring in chroot (locale, user, network)…",
        "pl": "Konfiguracja w chroot (lokalizacja, użytkownik, sieć)…",
    },
    "progress.stage.desktop": {
        "en": "Setting up the desktop environment…",
        "pl": "Konfiguracja środowiska graficznego…",
    },
    "progress.stage.grub": {"en": "Installing GRUB…", "pl": "Instalacja GRUB…"},
    "progress.stage.snapper": {"en": "Initializing snapper…", "pl": "Inicjalizacja snapper…"},
    "progress.stage.cleanup": {"en": "Cleaning up…", "pl": "Sprzątanie…"},

    # Finish
    "finish.step_title": {"en": "Finish", "pl": "Zakończenie"},
    "finish.restart_title": {"en": "Restart now", "pl": "Uruchom ponownie"},
    "finish.restart_subtitle": {
        "en": "Close the live session and boot into the newly installed Corvid OS",
        "pl": "Zamknij sesję live i uruchom nowo zainstalowany Corvid OS",
    },
    "finish.stay_title": {"en": "Stay in the live session", "pl": "Zostań w sesji live"},
    "finish.stay_subtitle": {"en": "Keep testing before you restart", "pl": "Testuj dalej, zanim zrestartujesz"},
    "finish.title": {"en": "Corvid OS is installed", "pl": "Corvid OS jest zainstalowany"},
    "finish.subtitle_done": {
        "en": "Remove the installation media before restarting.",
        "pl": "Wyjmij nośnik instalacyjny przed ponownym uruchomieniem.",
    },
    "finish.subtitle_dry_run": {
        "en": "(dry run — nothing was actually installed)",
        "pl": "(symulacja — nic nie zostało faktycznie zainstalowane)",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Look up `key` for `lang`, falling back to English, then the key
    itself if it's missing entirely (so a typo shows up as visible text
    instead of crashing)."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", key))
    return text.format(**kwargs) if kwargs else text


def tr(state, key: str, **kwargs) -> str:
    """Same as t(), but reads the language straight off InstallState."""
    return t(key, LANG_CODE.get(state.language, "en"), **kwargs)
