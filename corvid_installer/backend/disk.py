"""Partitioning and Btrfs subvolume setup. GPT + one EFI partition + one
Btrfs root partition filling the rest -- this is the "Auto" mode from
disk.py (the UI step); "Manual" mode hands off to GNOME Disks instead and
never calls anything here."""

import subprocess
from pathlib import Path

MOUNT_OPTS = "noatime,compress=zstd:1,space_cache=v2"

# @snapshots is deliberately not created here -- see backend/snapper.py for
# why (snapper wants to create its own .snapshots subvolume, and fighting
# that during the first real implementation isn't worth the risk of getting
# the remount dance subtly wrong on an untested path). This is a simplification
# vs. design.md's original subvolume table; worth reconciling once this has
# actually been through a few VM installs.
SUBVOLUMES = ["@", "@home", "@var_log", "@var_cache_pacman_pkg"]
SUBVOLUME_MOUNTS = {
    "@": "",  # root itself
    "@home": "home",
    "@var_log": "var/log",
    "@var_cache_pacman_pkg": "var/cache/pacman/pkg",
}


def _run(cmd: list[str], dry_run: bool, log) -> None:
    log(f"$ {' '.join(cmd)}")
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def partition_path(disk: str, index: int) -> str:
    # /dev/nvme0n1 -> /dev/nvme0n1p1, /dev/sda -> /dev/sda1
    return f"{disk}p{index}" if disk[-1].isdigit() else f"{disk}{index}"


def partition_disk(disk: str, efi_size_mib: int = 512, dry_run: bool = False, log=print) -> tuple[str, str]:
    """Wipes `disk` and lays down GPT + EFI partition + Btrfs root
    partition. Returns (efi_partition, root_partition)."""
    _run(["parted", "-s", disk, "mklabel", "gpt"], dry_run, log)
    _run(["parted", "-s", disk, "mkpart", "ESP", "fat32", "1MiB", f"{efi_size_mib}MiB"], dry_run, log)
    _run(["parted", "-s", disk, "set", "1", "esp", "on"], dry_run, log)
    _run(["parted", "-s", disk, "mkpart", "root", "btrfs", f"{efi_size_mib}MiB", "100%"], dry_run, log)

    efi_part = partition_path(disk, 1)
    root_part = partition_path(disk, 2)

    _run(["mkfs.fat", "-F32", efi_part], dry_run, log)
    _run(["mkfs.btrfs", "-f", root_part], dry_run, log)
    return efi_part, root_part


def create_subvolumes(root_part: str, mount_point: str = "/mnt", dry_run: bool = False, log=print) -> None:
    _run(["mount", root_part, mount_point], dry_run, log)
    for subvol in SUBVOLUMES:
        _run(["btrfs", "subvolume", "create", f"{mount_point}/{subvol}"], dry_run, log)
    _run(["umount", mount_point], dry_run, log)


def mount_layout(root_part: str, efi_part: str, mount_point: str = "/mnt", dry_run: bool = False, log=print) -> None:
    _run(["mount", "-o", f"subvol=@,{MOUNT_OPTS}", root_part, mount_point], dry_run, log)
    for subvol, rel_path in SUBVOLUME_MOUNTS.items():
        if subvol == "@":
            continue
        full_path = f"{mount_point}/{rel_path}"
        _run(["mkdir", "-p", full_path], dry_run, log)
        _run(["mount", "-o", f"subvol={subvol},{MOUNT_OPTS}", root_part, full_path], dry_run, log)
    _run(["mkdir", "-p", f"{mount_point}/boot"], dry_run, log)
    _run(["mount", efi_part, f"{mount_point}/boot"], dry_run, log)


def unmount_all(mount_point: str = "/mnt", dry_run: bool = False, log=print) -> None:
    _run(["umount", "-R", mount_point], dry_run, log)


def list_disks() -> list[str]:
    """Real disks from lsblk, formatted like 'Disk step' expects:
    '/dev/vda — 20G'. Empty list (not an exception) if lsblk isn't around --
    e.g. when just poking at the UI outside a live/VM environment."""
    try:
        out = subprocess.run(
            ["lsblk", "-d", "-n", "-o", "PATH,SIZE,TYPE"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []
    # lsblk reports floppy drives, zram, and other junk as TYPE=disk too --
    # a QEMU machine has a virtual floppy controller by default even though
    # nothing is attached to it, and it was silently picked as the "first"
    # disk here, so the installer tried to partition /dev/fd0 instead of the
    # real virtio disk. Filter those out by name, not just by TYPE.
    _EXCLUDED_NAME_PREFIXES = ("fd", "sr", "loop", "zram")

    disks = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) != 3 or parts[2] != "disk":
            continue
        name = Path(parts[0]).name
        if name.startswith(_EXCLUDED_NAME_PREFIXES):
            continue
        disks.append(f"{parts[0]} — {parts[1]}")
    return disks


def is_uefi() -> bool:
    return Path("/sys/firmware/efi").exists()
