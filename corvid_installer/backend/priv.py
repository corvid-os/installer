"""Real install commands (parted, mkfs, mount, arch-chroot, pacstrap, ...)
need root. The installer itself runs as a normal desktop user (liveuser on
the live ISO, launched from the desktop icon), so every privileged command
gets prefixed with sudo -- liveuser has passwordless sudo configured in the
live environment (see iso/corvid-overrides/airootfs/root/customize_airootfs.sh),
so this doesn't prompt for anything."""

import os


def as_root(cmd: list[str]) -> list[str]:
    if os.geteuid() == 0:
        return cmd
    return ["sudo", *cmd]
