# Corvid Installer

Własny instalator **Corvid OS** — Python + GTK4/libadwaita, modularny (każdy
krok instalacji to osobny moduł, żeby łatwo dodać kolejny krok bez rozrastania
się jednego pliku do tysięcy linijek).

Powód własnego instalatora zamiast Calamares: dokumentacja Calamares nie
pasuje do tego jak chcemy to rozwijać.

## Status
Wczesna faza — design i lista kroków instalatora jeszcze się ustala.
Pełny design projektu: [`corvid-os/corvid`](https://github.com/corvid-os/corvid)
(patrz `prompt-el/design.md`).

## Stack (ustalone)
- Python
- GTK4 + libadwaita
- Architektura modułowa — kroki instalatora jako osobne pluginy/moduły

## TBD
- Dokładna lista kroków (partycjonowanie, użytkownik, lokalizacja, wybór DE, bootloader...)
- Struktura katalogów modułów
- Integracja z profilem `iso` (jak installer trafia na Live ISO)
