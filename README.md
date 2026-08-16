# Corvid Installer

The installer for Corvid OS — Python and GTK4/libadwaita, built so each
install step is its own module rather than one file that grows into
thousands of lines. We're not using Calamares here because its documentation
didn't fit how we wanted to build and extend this.

Right now this is a UI skeleton. All fourteen steps from the design have a
working, clickable interface — back/forward navigation, validation,
`InstallState` getting filled in as you go — but there's no real install
logic behind any of it yet. `validate()`/`apply()` are mostly no-ops, and the
"install" step just simulates progress with a timer rather than calling
`pacstrap`, `parted`, or anything else that touches a disk. That's
deliberate, matching the M1 → M2 → M3 progression in the full design (see
`design.md` and `code.md` in the private `corvid-os/prompt-el` repo).

Running it:

```bash
pip install -e .
corvid-installer
# or without installing:
python3 -m corvid_installer.main
```

Needs GTK4, libadwaita, and PyGObject (on Arch: `gtk4`, `libadwaita`,
`python-gobject`).

The layout: `main.py` is the entry point, `window.py` handles the wizard
navigation and holds the shared `InstallState`, `steps/` has one file per
step (see `steps/__init__.py` for the full list) plus `base.py` for the
shared `InstallStep` interface, and `ui/page.py` has the shared page layout
helper. Adding a step means one new file under `steps/`, a class that
inherits `InstallStep`, and a line added to the list in
`steps/__init__.py` — nothing in `window.py` needs to change.

What comes next, roughly M2 and on: a real backend under `backend/` —
`disk.py`, `btrfs.py`, `pacstrap.py`, `chroot.py`, `hardware.py`,
`snapper.py` — a `--dry-run` mode that logs commands instead of running
them, real Wi-Fi/disk/GPU detection through NetworkManager, `lsblk`, and
`lspci`, and unit tests for the backend that don't need a real disk.
