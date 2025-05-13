import aes

BITS = list(bin(int.from_bytes(bytes(aes.s_box), "big"))[2:].rjust(256 * 8, '0'))

for bit in range(256 * 8):
    bits = BITS.copy()
    bits[bit] = "1" if bits[bit] == "0" else "0"
    s_box = int(''.join(bits), 2).to_bytes(256, "big")
    if s_box.count(b'\x01') == 2 and s_box.count(b'\x00') == 0:
        print(bit, s_box.count(b'\x01'))