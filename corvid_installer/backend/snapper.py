"""snapper config + grub-btrfs. snapper's create-config wants to create its
own .snapshots subvolume, so this doesn't try to fight that -- see the note
in backend/disk.py. That means the actual layout is a slight simplification
of design.md's original @snapshots-as-a-top-level-subvolume plan; worth
reconciling once this has been through real VM installs."""

from corvid_installer.backend.chroot import run_in_chroot


def init_snapper(mount_point: str, hourly: int, daily: int, weekly: int, monthly: int, dry_run: bool, log) -> None:
    run_in_chroot(mount_point, ["snapper", "-c", "root", "create-config", "/"], dry_run, log)

    config_path = f"{mount_point}/etc/snapper/configs/root"
    limits = {
        "TIMELINE_LIMIT_HOURLY": hourly,
        "TIMELINE_LIMIT_DAILY": daily,
        "TIMELINE_LIMIT_WEEKLY": weekly,
        "TIMELINE_LIMIT_MONTHLY": monthly,
        "TIMELINE_LIMIT_YEARLY": 0,
    }
    for key, value in limits.items():
        log(f"$ sed -i 's/^{key}=.*/{key}=\"{value}\"/' {config_path}")
        if not dry_run:
            _set_config_value(config_path, key, str(value))

    run_in_chroot(mount_point, ["systemctl", "enable", "grub-btrfsd.service"], dry_run, log)


def _set_config_value(config_path: str, key: str, value: str) -> None:
    with open(config_path) as f:
        lines = f.readlines()
    with open(config_path, "w") as f:
        for line in lines:
            if line.startswith(f"{key}="):
                f.write(f'{key}="{value}"\n')
            else:
                f.write(line)
