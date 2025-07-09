qemu-system-riscv64 \
    -machine virt \
    -bios ./bios.bin \
    -serial stdio \
    -device loader,file=./os.bin,addr=0x80200000 \
    -drive  file=./fs.img,if=none,format=raw,id=x0 \
    -device virtio-blk-device,drive=x0 \
    -device virtio-gpu-device \
    -device virtio-keyboard-device \
    -device virtio-mouse-device \
    -device virtio-net-device,netdev=net0 \
    -netdev user,id=net0,hostfwd=udp::6200-:2000,hostfwd=tcp::6201-:80

// The QEMU version must be 7.0.0 or above.