"""Real install commands (parted, mkfs, mount, arch-chroot, pacstrap, ...)
need root. The installer itself runs as a normal desktop user (liveuser on
the live ISO, launched from the desktop icon), so every privileged command
gets prefixed with sudo -- liveuser has passwordless sudo configured in the
live environment (see iso/corvid-overrides/airootfs/root/customize_airootfs.sh),
so this doesn't prompt for anything."""

import os
import subprocess


def as_root(cmd: list[str]) -> list[str]:
    if os.geteuid() == 0:
        return cmd
    return ["sudo", *cmd]


def run_root(cmd: list[str], *, dry_run: bool, log, input: str | None = None) -> None:
    """Runs cmd as root, logging it first. On failure raises with the
    command's actual stderr attached -- plain `subprocess.run(check=True)`
    only gives str(CalledProcessError), i.e. "returned non-zero exit status
    1" with no hint of *why*, which is useless when this only ever shows up
    on a screen you can't copy-paste from."""
    full = as_root(cmd)
    log(f"$ {' '.join(full)}")
    if dry_run:
        return
    result = subprocess.run(full, input=input, text=True, capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit status {result.returncode}"
        raise RuntimeError(f"{' '.join(full)}\n{detail}")
