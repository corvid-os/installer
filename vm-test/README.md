# Testing Corvid Installer in a VM

This tests the real backend (`--execute`, actually partitions/pacstraps/
chroots) against a disposable QEMU VM instead of your real machine. Nothing
here touches your host disk -- the VM's disk is a single file
(`corvid-test.qcow2`) you can delete any time.

## One-time setup

Install QEMU + UEFI firmware (OVMF) + an Arch ISO downloader:

```bash
sudo pacman -S --needed qemu-desktop edk2-ovmf
```

Grab the current Arch Linux ISO (any mirror works; this uses the
geo-redirected one):

```bash
cd vm-test
curl -LO https://geo.mirror.pkgbuild.com/iso/latest/archlinux-x86_64.iso
```

## Create the VM disk

```bash
./create-vm-disk.sh
```

Creates `corvid-test.qcow2`, a 20G sparse disk image (real size on disk
starts near 0, grows as the install writes to it).

## Boot the Arch ISO to install Corvid inside the VM

```bash
./run-vm.sh --boot-iso
```

This boots the VM from `archlinux-x86_64.iso` with the test disk attached
as `/dev/vda`. Once it's up (you'll get a root shell), inside the VM:

```bash
# get the installer's code into the VM
pacman -Sy --noconfirm git python-gobject gtk4 libadwaita
git clone https://github.com/corvid-os/installer.git
cd installer
pip install -e . --break-system-packages   # archiso's environment is externally managed

# GUI won't display without a Wayland/X session in the live ISO's TTY --
# run the installer over the VM's virtual display instead:
Xvfb :1 -screen 0 1024x768x24 &
DISPLAY=:1 corvid-installer --execute
```

Walk through all 14 steps as normal. On the Disk step, pick `/dev/vda` --
that's the qcow2 file you created, not your real disk. Since you're inside
the VM's isolated ISO environment, there's no live GUI attached by default;
either VNC into the Xvfb display (`x11vnc -display :1`, connect from the
host) or, simpler, just watch the log lines the installer prints as it
runs `pacstrap`/`arch-chroot`/etc. -- that output alone tells you whether
each stage succeeded.

## Boot the installed system

Once the install finishes and you shut the VM down:

```bash
./run-vm.sh
```

(No `--boot-iso` this time -- boots straight from the qcow2 disk, GRUB
menu, into whatever you installed: GNOME or Hyprland+minimaLinux.)

## What to actually check

- Does GRUB show up and boot into the installed system at all?
- GNOME path: does GDM show a login screen, does the desktop come up?
- Hyprland path: did minimaLinux's `install.sh` actually complete inside
  the chroot (check its log output during the install step) -- this is
  the part most likely to need fixes, since minimaLinux assumes a running
  session with dbus/Wayland that a chroot doesn't have. If it fails here,
  that's expected on the first pass; it's the next thing to debug.
- `btrfs subvolume list /` after boot -- should show `@`, `@home`,
  `@var_log`, `@var_cache_pacman_pkg`.
- `snapper list` -- should show at least the config, even with 0 snapshots
  yet.

## Cleaning up

```bash
rm vm-test/corvid-test.qcow2
```

Nothing outside this file was ever touched.
