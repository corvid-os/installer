#!/usr/bin/env bash
# Boots the Corvid test VM. UEFI (OVMF), 4G RAM, 4 cores, KVM acceleration,
# the qcow2 disk as /dev/vda. Pass --boot-iso to boot the Arch install ISO
# instead of the disk (first run, to install); omit it to boot the
# already-installed system (subsequent runs).
set -euo pipefail
cd "$(dirname "$0")"

DISK=corvid-test.qcow2
ISO=archlinux-x86_64.iso

if [ ! -f "$DISK" ]; then
  echo "No $DISK yet -- run ./create-vm-disk.sh first." >&2
  exit 1
fi

# Locate OVMF firmware -- path differs slightly across distros.
OVMF_CODE=""
for candidate in \
  /usr/share/edk2/x64/OVMF_CODE.4m.fd \
  /usr/share/edk2-ovmf/x64/OVMF_CODE.fd \
  /usr/share/OVMF/OVMF_CODE.fd
do
  if [ -f "$candidate" ]; then
    OVMF_CODE="$candidate"
    break
  fi
done
if [ -z "$OVMF_CODE" ]; then
  echo "Couldn't find OVMF firmware. Install edk2-ovmf (pacman -S edk2-ovmf)." >&2
  exit 1
fi

QEMU_ARGS=(
  -enable-kvm
  -m 4096
  -smp 4
  -cpu host
  -drive "if=pflash,format=raw,readonly=on,file=$OVMF_CODE"
  -drive "file=$DISK,if=virtio,format=qcow2"
  -netdev user,id=net0
  -device virtio-net-pci,netdev=net0
  -vga virtio
  -display gtk
)

if [ "${1:-}" = "--boot-iso" ]; then
  if [ ! -f "$ISO" ]; then
    echo "No $ISO -- download it first, see vm-test/README.md." >&2
    exit 1
  fi
  QEMU_ARGS+=(-drive "file=$ISO,media=cdrom" -boot d)
fi

qemu-system-x86_64 "${QEMU_ARGS[@]}"
