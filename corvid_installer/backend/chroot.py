"""Configuration done inside arch-chroot: locale, hostname, user, bootloader,
enabling services. Encryption (LUKS) isn't wired up yet -- see run_install()
in installer.py, which logs a clear warning and proceeds unencrypted if the
user asked for it. Don't silently pretend it happened."""

import subprocess
from pathlib import Path


def run_in_chroot(mount_point: str, command: list[str], dry_run: bool, log) -> None:
    full = ["arch-chroot", mount_point, *command]
    log(f"$ {' '.join(full)}")
    if dry_run:
        return
    subprocess.run(full, check=True)


def set_timezone(mount_point: str, timezone: str, dry_run: bool, log) -> None:
    run_in_chroot(mount_point, ["ln", "-sf", f"/usr/share/zoneinfo/{timezone}", "/etc/localtime"], dry_run, log)
    run_in_chroot(mount_point, ["hwclock", "--systohc"], dry_run, log)


def set_locale(mount_point: str, locale: str, dry_run: bool, log) -> None:
    log(f"$ echo '{locale} UTF-8' >> {mount_point}/etc/locale.gen")
    if not dry_run:
        with open(f"{mount_point}/etc/locale.gen", "a") as locale_gen:
            locale_gen.write(f"{locale} UTF-8\n")
    run_in_chroot(mount_point, ["locale-gen"], dry_run, log)

    lang = locale.split()[0] if " " in locale else locale
    log(f"$ echo 'LANG={lang}' > {mount_point}/etc/locale.conf")
    if not dry_run:
        Path(f"{mount_point}/etc/locale.conf").write_text(f"LANG={lang}\n")


def set_hostname(mount_point: str, hostname: str, dry_run: bool, log) -> None:
    log(f"$ echo '{hostname}' > {mount_point}/etc/hostname")
    if not dry_run:
        Path(f"{mount_point}/etc/hostname").write_text(f"{hostname}\n")


def create_user(mount_point: str, username: str, full_name: str, is_admin: bool, dry_run: bool, log) -> None:
    cmd = ["useradd", "-m", "-c", full_name, "-s", "/usr/bin/bash"]
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
    if dry_run:
        return
    subprocess.run(
        ["arch-chroot", mount_point, "chpasswd"],
        input=f"{username}:{password}\n", text=True, check=True,
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
