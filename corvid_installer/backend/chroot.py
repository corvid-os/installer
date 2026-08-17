"""Configuration done inside arch-chroot: locale, hostname, user, bootloader,
enabling services. Encryption (LUKS) isn't wired up yet -- see run_install()
in installer.py, which logs a clear warning and proceeds unencrypted if the
user asked for it. Don't silently pretend it happened."""

from corvid_installer.backend.priv import run_root


def run_in_chroot(mount_point: str, command: list[str], dry_run: bool, log) -> None:
    run_root(["arch-chroot", mount_point, *command], dry_run=dry_run, log=log)


def _write_file(path: str, content: str, mode: str, dry_run: bool, log) -> None:
    """Files under the target root (mount_point/etc/...) are root-owned like
    any fresh pacstrap'd filesystem -- a plain Python open()/write_text()
    from the (non-root) installer process fails with PermissionError. Route
    writes through `sudo tee` instead, same reasoning as as_root() for
    subprocess calls."""
    verb = "appending to" if mode == "a" else "writing to"
    log(f"$ ({verb} {path})")
    tee_args = ["tee", "-a", path] if mode == "a" else ["tee", path]
    run_root(tee_args, dry_run=dry_run, log=lambda _msg: None, input=content)


def set_timezone(mount_point: str, timezone: str, dry_run: bool, log) -> None:
    run_in_chroot(mount_point, ["ln", "-sf", f"/usr/share/zoneinfo/{timezone}", "/etc/localtime"], dry_run, log)
    run_in_chroot(mount_point, ["hwclock", "--systohc"], dry_run, log)


def set_locale(mount_point: str, locale: str, dry_run: bool, log) -> None:
    _write_file(f"{mount_point}/etc/locale.gen", f"{locale} UTF-8\n", "a", dry_run, log)
    run_in_chroot(mount_point, ["locale-gen"], dry_run, log)

    lang = locale.split()[0] if " " in locale else locale
    _write_file(f"{mount_point}/etc/locale.conf", f"LANG={lang}\n", "w", dry_run, log)


def set_hostname(mount_point: str, hostname: str, dry_run: bool, log) -> None:
    _write_file(f"{mount_point}/etc/hostname", f"{hostname}\n", "w", dry_run, log)


def create_user(mount_point: str, username: str, full_name: str, is_admin: bool, dry_run: bool, log, shell: str = "/usr/bin/bash") -> None:
    cmd = ["useradd", "-m", "-c", full_name, "-s", shell]
    if is_admin:
        cmd += ["-G", "wheel"]
    cmd.append(username)
    run_in_chroot(mount_point, cmd, dry_run, log)

    if is_admin:
        run_in_chroot(
            mount_point,
            ["sed", "-i", "s/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/", "/etc/sudoers"],
            dry_run, log,
        )


def set_password(mount_point: str, username: str, password: str, dry_run: bool, log) -> None:
    log(f"$ echo '{username}:***' | arch-chroot {mount_point} chpasswd")
    run_root(
        ["arch-chroot", mount_point, "chpasswd"],
        dry_run=dry_run, log=lambda _msg: None,
        input=f"{username}:{password}\n",
    )


def install_bootloader(mount_point: str, dry_run: bool, log) -> None:
    run_in_chroot(
        mount_point,
        ["grub-install", "--target=x86_64-efi", "--efi-directory=/boot", "--bootloader-id=Corvid"],
        dry_run, log,
    )
    run_in_chroot(mount_point, ["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], dry_run, log)


def enable_services(mount_point: str, services: list[str], dry_run: bool, log) -> None:
    for service in services:
        run_in_chroot(mount_point, ["systemctl", "enable", service], dry_run, log)


def run_as_user(mount_point: str, username: str, shell_command: str, dry_run: bool, log) -> None:
    """Runs `shell_command` inside the chroot as `username` (not root) --
    used for the minimaLinux clone+install, which expects to run as a
    normal user. arch-chroot bind-mounts resolv.conf automatically, so
    networking works here as long as the host has it."""
    run_in_chroot(mount_point, ["runuser", "-u", username, "--", "bash", "-c", shell_command], dry_run, log)
