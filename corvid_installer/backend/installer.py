"""Orchestrates the actual install: partition -> pacstrap -> chroot config
-> bootloader -> snapper. Called from steps/progress.py, in a background
thread so the GTK main loop stays responsive. Nothing here has any GUI
dependency, so it's also directly testable/scriptable on its own."""

from dataclasses import dataclass

from corvid_installer.backend import chroot, disk, pacstrap, snapper
from corvid_installer.state import InstallState

MOUNT_POINT = "/mnt"


@dataclass
class InstallStage:
    key: str  # matches an i18n progress.stage.* key
    run: "callable"  # (state, log) -> None


def _stage_partition(state: InstallState, log) -> None:
    if state.partitioning_mode != "auto":
        log("Manual partitioning selected -- assuming the disk is already "
            "partitioned and mounted at /mnt (via GNOME Disks + manual mount).")
        return
    if state.encrypt:
        log("WARNING: encryption was requested but isn't implemented yet -- "
            "proceeding WITHOUT encryption. Don't rely on this for anything "
            "you actually care about keeping private.")
    efi_part, root_part = disk.partition_disk(state.disk, dry_run=state.dry_run, log=log)
    disk.create_subvolumes(root_part, MOUNT_POINT, dry_run=state.dry_run, log=log)
    disk.mount_layout(root_part, efi_part, MOUNT_POINT, dry_run=state.dry_run, log=log)


def _stage_pacstrap(state: InstallState, log) -> None:
    packages = pacstrap.packages_for(state.desktop_environment)
    pacstrap.pacstrap(MOUNT_POINT, packages, dry_run=state.dry_run, log=log)


def _stage_genfstab(state: InstallState, log) -> None:
    pacstrap.genfstab(MOUNT_POINT, dry_run=state.dry_run, log=log)


def _stage_chroot_config(state: InstallState, log) -> None:
    chroot.set_timezone(MOUNT_POINT, state.timezone, state.dry_run, log)
    chroot.set_locale(MOUNT_POINT, state.locale, state.dry_run, log)
    chroot.set_hostname(MOUNT_POINT, "corvid", state.dry_run, log)
    chroot.create_user(MOUNT_POINT, state.username, state.full_name, state.is_admin, state.dry_run, log)
    if state.password:
        chroot.set_password(MOUNT_POINT, state.username, state.password, state.dry_run, log)
    chroot.enable_services(MOUNT_POINT, ["NetworkManager"], state.dry_run, log)


def _stage_desktop_setup(state: InstallState, log) -> None:
    if state.desktop_environment == "gnome":
        chroot.enable_services(MOUNT_POINT, ["gdm"], state.dry_run, log)
        return

    # Hyprland path: clone minimaLinux and run its own installer as the
    # new user. This is third-party content we haven't audited line by
    # line -- see desktop-hyprland.md. Some of its steps may assume a
    # running live session (dbus/Wayland) that doesn't exist inside a
    # chroot; treat this stage as the most likely thing to need fixing
    # after a real VM run.
    clone_and_install = (
        "git clone https://github.com/Echilonvibin/minimaLinux.git ~/minimaLinux "
        "&& cd ~/minimaLinux "
        "&& chmod +x install.sh "
        "&& sudo ./install.sh"
    )
    chroot.run_as_user(MOUNT_POINT, state.username, clone_and_install, state.dry_run, log)


def _stage_bootloader(state: InstallState, log) -> None:
    chroot.install_bootloader(MOUNT_POINT, state.dry_run, log)


def _stage_snapper(state: InstallState, log) -> None:
    snapper.init_snapper(
        MOUNT_POINT,
        state.snapshots_hourly, state.snapshots_daily, state.snapshots_weekly, state.snapshots_monthly,
        state.dry_run, log,
    )


def _stage_cleanup(state: InstallState, log) -> None:
    disk.unmount_all(MOUNT_POINT, dry_run=state.dry_run, log=log)


STAGES: list[InstallStage] = [
    InstallStage("progress.stage.partition", _stage_partition),
    InstallStage("progress.stage.pacstrap", _stage_pacstrap),
    InstallStage("progress.stage.genfstab", _stage_genfstab),
    InstallStage("progress.stage.chroot", _stage_chroot_config),
    InstallStage("progress.stage.desktop", _stage_desktop_setup),
    InstallStage("progress.stage.grub", _stage_bootloader),
    InstallStage("progress.stage.snapper", _stage_snapper),
    InstallStage("progress.stage.cleanup", _stage_cleanup),
]
