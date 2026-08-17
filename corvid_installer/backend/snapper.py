"""snapper config + grub-btrfs. snapper's create-config wants to create its
own .snapshots subvolume, so this doesn't try to fight that -- see the note
in backend/disk.py. That means the actual layout is a slight simplification
of design.md's original @snapshots-as-a-top-level-subvolume plan; worth
reconciling once this has been through real VM installs."""

from corvid_installer.backend.chroot import run_in_chroot


def init_snapper(mount_point: str, hourly: int, daily: int, weekly: int, monthly: int, dry_run: bool, log) -> None:
    # --no-dbus: arch-chroot doesn't run a D-Bus system bus (no systemd
    # inside the chroot), and snapper defaults to talking to snapperd over
    # DBus -- without this it fails with
    # "Failure (org.freedesktop.DBus.Error.ServiceUnknown)". This is the
    # standard fix for running snapper during a chroot install.
    run_in_chroot(mount_point, ["snapper", "--no-dbus", "-c", "root", "create-config", "/"], dry_run, log)

    # /etc/snapper/configs/root is root-owned like anything else under the
    # target root -- run sed *inside* the chroot (as root, via run_in_chroot)
    # rather than editing the file directly from this non-root process.
    limits = {
        "TIMELINE_LIMIT_HOURLY": hourly,
        "TIMELINE_LIMIT_DAILY": daily,
        "TIMELINE_LIMIT_WEEKLY": weekly,
        "TIMELINE_LIMIT_MONTHLY": monthly,
        "TIMELINE_LIMIT_YEARLY": 0,
    }
    for key, value in limits.items():
        run_in_chroot(
            mount_point,
            ["sed", "-i", f's/^{key}=.*/{key}="{value}"/', "/etc/snapper/configs/root"],
            dry_run, log,
        )

    run_in_chroot(mount_point, ["systemctl", "enable", "grub-btrfsd.service"], dry_run, log)
