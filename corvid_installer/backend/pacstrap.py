"""pacstrap + genfstab. Package sets are deliberately minimal right now --
"basics" scope per design.md: vanilla GNOME, or Hyprland + minimaLinux
(see backend/hyprland_setup.py). Gaming/dev profile packages, GPU driver
detection, etc. come later (roadmap M4/M5)."""

from corvid_installer.backend.priv import run_root

BASE_PACKAGES = [
    "base", "base-devel", "linux-zen", "linux-zen-headers", "linux-firmware",
    "networkmanager", "sudo", "git", "reflector",
    "btrfs-progs", "snapper", "snap-pac", "grub-btrfs", "grub", "efibootmgr",
]

# Vanilla -- no Corvid-specific extensions/theme yet (that's corvid-gnome
# in package-management.md, not written yet).
GNOME_PACKAGES = ["gnome", "gnome-tweaks", "gdm"]

# minimaLinux's own package list (github.com/Echilonvibin/minimaLinux
# install.sh), minus the ~5 entries that turned out to be AUR/chaotic-aur
# only (update-grub, bibata-cursor-theme, yaru-icon-theme,
# humanity-icon-theme, ttf-symbola -- all cosmetic: cursor/icon theme, one
# font). Notably `noctalia` -- the panel/shell minimaLinux's install.sh
# still builds from AUR as `noctalia-git` via yay -- has since landed in
# Arch's official [extra] repo as a stable package, so the whole desktop
# environment installs through plain pacstrap now: no AUR, no yay, no
# build-from-source, no interactive-sudo problem (see installer.py's
# _stage_desktop_setup, which just copies minimaLinux's dotfiles on top).
HYPRLAND_PACKAGES = [
    "hyprland", "xdg-desktop-portal-hyprland", "hyprland-protocols", "hyprlock", "hypridle",
    "kitty", "kitty-shell-integration", "kitty-terminfo",
    "fish", "starship", "fastfetch",
    "noctalia", "polkit-gnome", "gnome-keyring", "xdg-desktop-portal-gtk", "xdg-user-dirs",
    "thunar", "thunar-media-tags-plugin", "thunar-shares-plugin", "thunar-vcs-plugin",
    "thunar-volman", "thunar-archive-plugin", "tumbler", "gvfs", "gvfs-afc", "gvfs-mtp", "gvfs-smb",
    "ntfs-3g", "dosfstools", "exfatprogs",
    "pavucontrol", "playerctl", "wlsunset", "cava",
    "satty", "grim", "slurp", "hyprshot", "loupe", "gcolor3",
    "gedit", "gnome-calculator", "gnome-disk-utility", "file-roller", "flatpak",
    "nwg-look", "nwg-displays", "adw-gtk-theme",
    "power-profiles-daemon", "cpupower", "upower", "gpu-screen-recorder",
    "qt6-base", "qt6ct", "qt6-websockets",
    "noto-fonts-emoji", "ttf-dejavu",
    "gst-plugins-good", "gst-plugins-ugly", "gst-libav",
    "unrar", "unzip", "7zip",
    "libopenraw", "libgsf", "poppler-glib", "ffmpegthumbnailer", "freetype2", "libgepub",
    "base-devel", "clang", "cmake", "go", "rust", "pkgconf", "meson", "ninja", "stb", "matugen",
    "os-prober",
]


def _run(cmd: list[str], dry_run: bool, log) -> None:
    run_root(cmd, dry_run=dry_run, log=log)


def packages_for(desktop_environment: str) -> list[str]:
    de_packages = GNOME_PACKAGES if desktop_environment == "gnome" else HYPRLAND_PACKAGES
    return [*BASE_PACKAGES, *de_packages]


SHIPPED_CACHE_DIR = "/opt/corvid-pkg-cache"


def _seed_target_cache(mount_point: str, dry_run: bool, log) -> None:
    """Copies the ISO's pre-downloaded packages (see
    iso/scripts/cache-target-packages.sh + seed_package_cache() in
    test-corvidos.sh) onto the *target* disk's own pacman cache, before
    pacstrap runs.

    Deliberately NOT using pacstrap -c (host cache): the live session's own
    root ("/") is a tmpfs overlay capped at 256MB by default
    (cow_spacesize) -- nowhere near enough for a real package set, and
    mkarchiso's build process (_cleanup_pacstrap_dir) unconditionally wipes
    /var/cache/pacman/pkg before packing the squashfs anyway, so anything
    shipped there never survives to boot. SHIPPED_CACHE_DIR is a path
    mkarchiso doesn't touch, and copying its contents onto the target's
    huge disk (not the tiny live overlay) means pacman's own free-space
    check runs against gigabytes of headroom instead of megabytes."""
    cache_target = f"{mount_point}/var/cache/pacman/pkg"
    shell_cmd = (
        f"mkdir -p {cache_target} && "
        f"if [ -d {SHIPPED_CACHE_DIR} ]; then cp -n {SHIPPED_CACHE_DIR}/*.pkg.tar.* {cache_target}/ 2>/dev/null || true; fi"
    )
    run_root(["sh", "-c", shell_cmd], dry_run=dry_run, log=log)


def pacstrap(mount_point: str, packages: list[str], dry_run: bool = False, log=print) -> None:
    _seed_target_cache(mount_point, dry_run, log)
    # No -c here on purpose -- see _seed_target_cache(). Default (target)
    # cache dir is $mount_point/var/cache/pacman/pkg, which we just
    # pre-populated; pacman only downloads whatever's missing/mismatched,
    # and even that download lands on the target disk, not the live "/".
    _run(["pacstrap", "-K", mount_point, *packages], dry_run, log)


def genfstab(mount_point: str, dry_run: bool = False, log=print) -> None:
    # Redirection has to happen *inside* the privileged process -- `sudo cmd
    # >> file` still tries to open `file` as the invoking (non-root) user
    # before exec'ing cmd, and fails the same way a plain open() would.
    shell_cmd = f"genfstab -U {mount_point} >> {mount_point}/etc/fstab"
    run_root(["sh", "-c", shell_cmd], dry_run=dry_run, log=log)
