"""pacstrap + genfstab. Package sets are deliberately minimal right now --
"basics" scope per design.md: vanilla GNOME, or Hyprland + minimaLinux
(see backend/hyprland_setup.py). Gaming/dev profile packages, GPU driver
detection, etc. come later (roadmap M4/M5)."""

import subprocess

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
    log(f"$ genfstab -U {mount_point} >> {mount_point}/etc/fstab")
    if dry_run:
        return
    with open(f"{mount_point}/etc/fstab", "a") as fstab_file:
        subprocess.run(["genfstab", "-U", mount_point], check=True, stdout=fstab_file)
