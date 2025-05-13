#!/bin/bash

qemu-system-x86_64 \
    -m 128M \
    -kernel bzImage \
    -initrd initramfs.cpio.gz \
    -append "console=ttyS0 loglevel=3 oops=panic panic=1 pti=off nokaslr quiet" \
    -cpu qemu64,+smep,+smap \
    -monitor /dev/null \
    -nographic \
    -no-reboot -s