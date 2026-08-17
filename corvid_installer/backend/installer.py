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
    # Normally already done -- the Disk step (step 4) now partitions
    # immediately (auto) or launches GNOME Disks (manual) as soon as you
    # click Next, instead of waiting for this stage. See disk.py's apply()
    # and state.disk_prepared. This stays as a fallback for anything that
    # calls STAGES directly without going through the wizard (dry-run
    # scripting, tests).
    if state.disk_prepared:
        log("Disk already prepared in step 4 -- skipping.")
        return
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
    # minimaLinux's dotfiles (_stage_desktop_setup) assume fish + starship,
    # not bash -- fish is in HYPRLAND_PACKAGES, so it's already on disk by
    # the time useradd runs here (pacstrap is an earlier stage).
    shell = "/usr/bin/fish" if state.desktop_environment == "hyprland" else "/usr/bin/bash"
    chroot.create_user(MOUNT_POINT, state.username, state.full_name, state.is_admin, state.dry_run, log, shell=shell)
    if state.password:
        chroot.set_password(MOUNT_POINT, state.username, state.password, state.dry_run, log)
    chroot.enable_services(MOUNT_POINT, ["NetworkManager"], state.dry_run, log)


def _stage_desktop_setup(state: InstallState, log) -> None:
    if state.desktop_environment == "gnome":
        chroot.enable_services(MOUNT_POINT, ["gdm"], state.dry_run, log)
        return

    # Hyprland path: clone minimaLinux and copy its dotfiles into place --
    # NOT run its own install.sh. Confirmed on real VM runs that install.sh
    # can't work here: it does `sudo ./install.sh` internally, which needs
    # an interactive terminal for the password prompt that doesn't exist in
    # this non-interactive chroot step ("sudo: a terminal is required").
    #
    # install.sh's own package list is otherwise reproduced in full in
    # HYPRLAND_PACKAGES (pacstrap.py) via plain pacstrap -- including
    # `noctalia`, the panel/shell those dotfiles expect, which install.sh
    # still builds from AUR as `noctalia-git` via yay but which has since
    # landed in Arch's official [extra] repo as a stable package. So no
    # AUR helper, no build-from-source, no separate privilege dance: this
    # step is just "drop the dotfiles in place", same as picking any
    # dotfiles repo by hand. The 5 packages that are still AUR/chaotic-aur
    # only (update-grub, bibata-cursor-theme, yaru-icon-theme,
    # humanity-icon-theme, ttf-symbola) are dropped -- all cosmetic
    # (cursor/icon theme, one font).
    # No display manager for the Hyprland path (GNOME gets gdm above;
    # minimaLinux's own dotfiles don't set one up either -- checked, its
    # fish config is just fastfetch + starship, nothing session-related).
    # Without this, the installed system boots to a bare tty login and the
    # user has to type `Hyprland` by hand every time. This is the standard
    # Arch Wiki "start Hyprland on login, no DM" pattern instead of pulling
    # in a whole greeter stack: exec Hyprland from the login shell, but
    # only for an actual login on tty1 that isn't already inside a Wayland
    # session (so e.g. `fish` opened in a Hyprland terminal later doesn't
    # also try to exec it).
    clone_and_copy_dotfiles = (
        "git clone https://github.com/Echilonvibin/minimaLinux.git ~/minimaLinux "
        "&& mkdir -p ~/.config "
        "&& cp -r ~/minimaLinux/.config/. ~/.config/ "
        "&& rm -rf ~/minimaLinux "
        "&& xdg-user-dirs-update "
        "&& mkdir -p ~/.config/fish "
        "&& cat >> ~/.config/fish/config.fish <<'FISHEOF'\n"
        "\n"
        "if status is-login\n"
        "    if test -z \"$WAYLAND_DISPLAY\"; and test \"$XDG_VTNR\" = 1\n"
        "        exec Hyprland\n"
        "    end\n"
        "end\n"
        "FISHEOF"
    )
    chroot.run_as_user(MOUNT_POINT, state.username, clone_and_copy_dotfiles, state.dry_run, log)


def _stage_bootloader(state: InstallState, log) -> None:
    chroot.install_bootloader(MOUNT_POINT, state.dry_run, log)


def _stage_snapper(state: InstallState, log) -> None:
    snapper.init_snapper(
        MOUNT_POINT,
        state.snapshots_hourly, state.snapshots_daily, state.snapshots_weekly, state.snapshots_monthly,
        state.dry_run, log,
    )


def _stage_cleanup(state: InstallState, log) -> None:
    # pacstrap -K initializes the target's pacman keyring via pacman-key,
    # which spawns a gpg-agent daemon inside the chroot -- it keeps running
    # (socket/cwd under the target root) after the chroot session ends,
    # which alone is enough for `umount -R` to fail with "target is busy"
    # even though nothing else is using the mount. gpgconf --kill all is
    # GnuPG's own documented way to stop it. Best-effort: this is cleanup,
    # not worth failing the whole install over if the agent's already gone.
    try:
        chroot.run_in_chroot(MOUNT_POINT, ["gpgconf", "--kill", "all"], state.dry_run, log)
    except Exception as exc:  # noqa: BLE001
        log(f"(gpgconf --kill all failed, continuing anyway: {exc})")
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
