# Corvid Installer

Własny instalator **Corvid OS** — Python + GTK4/libadwaita, modularny (każdy
krok instalacji to osobny moduł, żeby łatwo dodać kolejny krok bez rozrastania
się jednego pliku do tysięcy linijek).

Powód własnego instalatora zamiast Calamares: dokumentacja Calamares nie
pasuje do tego jak chcemy to rozwijać.

## Status: szkielet UI (M1)

✅ Wszystkie **14 kroków** z designu mają działający, klikalny UI — nawigacja
Wstecz/Dalej, walidacja, wypełniony `InstallState`. ⚠️ **Żadnej realnej logiki
instalacyjnej jeszcze nie ma** — `validate()`/`apply()` w krokach to w
większości no-opy, krok "Instalacja" tylko **symuluje** postęp (animacja,
zero wywołań `pacstrap`/`parted`/itd.). To świadomy, pierwszy krok zgodnie z
roadmapą (M1 → M2 → M3 w pełnym designie).

Pełny design projektu: [`corvid-os/corvid`](https://github.com/corvid-os/corvid)
→ prywatne repo `corvid-os/prompt-el` (`design.md`, `code.md`).

## Uruchomienie

```bash
pip install -e .
corvid-installer
# albo bez instalacji:
python3 -m corvid_installer.main
```

Wymaga GTK4 + libadwaita + PyGObject (na Arch: `gtk4`, `libadwaita`, `python-gobject`).

## Struktura

```
corvid_installer/
├── main.py           # entry point (Adw.Application)
├── window.py         # wizard: nawigacja między krokami, InstallState
├── state.py          # InstallState — centralny stan wyborów
├── steps/            # jeden plik = jeden krok, patrz steps/__init__.py (ALL_STEPS)
│   └── base.py        # InstallStep — wspólny interfejs (build_widget/validate/apply)
└── ui/page.py         # wspólny szkielet strony (ikona/tytuł/podtytuł + grupy)
```

Dodanie nowego kroku: nowy plik w `steps/`, klasa dziedzicząca po `InstallStep`,
wpis na liście `ALL_STEPS` w `steps/__init__.py`. Zero zmian w `window.py`.

## Co dalej (M2+)
- Prawdziwy backend: `backend/disk.py`, `backend/btrfs.py`, `backend/pacstrap.py`,
  `backend/chroot.py`, `backend/hardware.py`, `backend/snapper.py`
- Tryb `--dry-run` w backendzie (loguje komendy zamiast je wykonywać)
- Realna detekcja sieci (NetworkManager), dysków (`lsblk`), GPU (`lspci`)
- Testy jednostkowe backendu (bez potrzeby realnego dysku — mock)
