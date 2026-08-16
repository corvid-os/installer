"""pacstrap + genfstab. Package sets are deliberately minimal right now --
"basics" scope per design.md: vanilla GNOME, or Hyprland + minimaLinux
(see backend/hyprland_setup.py). Gaming/dev profile packages, GPU driver
detection, etc. come later (roadmap M4/M5)."""

import subprocess

from corvid_installer.backend.priv import as_root

BASE_PACKAGES = [
    "base", "base-devel", "linux-zen", "linux-zen-headers", "linux-firmware",
    "networkmanager", "sudo", "git", "reflector",
    "btrfs-progs", "snapper", "snap-pac", "grub-btrfs", "grub", "efibootmgr",
]

# Vanilla -- no Corvid-specific extensions/theme yet (that's corvid-gnome
# in package-management.md, not written yet).
GNOME_PACKAGES = ["gnome", "gnome-tweaks", "gdm"]

# Just the compositor + a terminal + a file manager; minimaLinux (installed
# post-pacstrap, see hyprland_setup.py) brings the rest (Noctalia, configs).
HYPRLAND_PACKAGES = ["hyprland", "kitty", "thunar", "xdg-desktop-portal-hyprland"]


def _run(cmd: list[str], dry_run: bool, log) -> None:
    cmd = as_root(cmd)
    log(f"$ {' '.join(cmd)}")
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def packages_for(desktop_environment: str) -> list[str]:
    de_packages = GNOME_PACKAGES if desktop_environment == "gnome" else HYPRLAND_PACKAGES
    return [*BASE_PACKAGES, *de_packages]


def pacstrap(mount_point: str, packages: list[str], dry_run: bool = False, log=print) -> None:
    _run(["pacstrap", "-K", mount_point, *packages], dry_run, log)


def genfstab(mount_point: str, dry_run: bool = False, log=print) -> None:
    # Redirection has to happen *inside* the privileged process -- `sudo cmd
    # >> file` still tries to open `file` as the invoking (non-root) user
    # before exec'ing cmd, and fails the same way a plain open() would.
    shell_cmd = f"genfstab -U {mount_point} >> {mount_point}/etc/fstab"
    cmd = as_root(["sh", "-c", shell_cmd])
    log(f"$ {shell_cmd}")
    if dry_run:
        return
    subprocess.run(cmd, check=True)
