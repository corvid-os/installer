#!/usr/bin/env bash
# Creates the disposable qcow2 disk the test VM installs onto. Safe to
# delete and re-run any time -- this never touches anything outside
# vm-test/.
set -euo pipefail
cd "$(dirname "$0")"

DISK=corvid-test.qcow2
SIZE=20G

if [ -f "$DISK" ]; then
  echo "$DISK already exists -- delete it first if you want a fresh one." >&2
  exit 1
fi

qemu-img create -f qcow2 "$DISK" "$SIZE"
echo "Created $DISK ($SIZE, sparse)"
